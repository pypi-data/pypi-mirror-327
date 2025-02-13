import typing
import torch
import torch.nn as nn


class LossAdaptedPlasticity(nn.Module):
    """
    This class calculates the loss weighting for each source
    based on the loss history of each source. 

    Examples
    ---------

    It's usage is as follows:

    .. code-block::

        >>> loss_weighting = LossAdaptedPlasticity()

    During the training loop:

    .. code-block::

        >>> outputs = model(inputs)
        >>> # get loss values for each sample
        >>> losses = loss_fn(outputs, targets, reduction="none")
        >>> # reweight the loss using LAP
        >>> losses = loss_weighting(losses=losses, sources=sources)
        >>> # get mean loss and backpropagate
        >>> loss = torch.mean(losses)
        >>> optimizer.zero_grad()
        >>> loss.backward()
        >>> optimizer.step()

    Arguments
    ---------
    - history_length: int, optional:
        The number of previous loss values for each source
        to be used in the loss adapted plasticity
        calculations.
        Defaults to :code:`10`.

    - warmup_iters: int, optional:
        The number of iterations before the loss weighting
        starts to be applied.
        Defaults to :code:`100`.

    - depression_strength: float, optional:
        This float determines the strength of the depression
        applied to the gradients. It is the value of :code:`m` in
        :code:`dep = 1-tanh(m*d)**2`.
        Defaults to :code:`1`.

    - discrete_amount: float, optional:
        The step size used when calculating the depression.
        Defaults to :code:`0.005`.

    - leniency: float, optional:
        The number of standard deviations away from the
        mean loss a mean source loss has to be
        before depression is applied.
        Defaults to :code:`1.0`.

    - device: str, optional:
        The device to use for the calculations.
        If this is a different device to the one
        which the model is on, the loss values will be
        moved to the device specified here and returned
        to the original device afterwards.
        Defaults to :code:`"cpu"`.

    """

    def __init__(
        self,
        history_length: int = 50,
        warmup_iters: int = 100,
        depression_strength: float = 1,
        discrete_amount: float = 0.005,
        leniency: float = 1.0,
        device="cpu",
    ):
        super().__init__()

        # options

        self.history_length = nn.Parameter(
            torch.tensor(history_length), requires_grad=False
        )
        self.warmup_iters = nn.Parameter(
            torch.tensor(warmup_iters), requires_grad=False
        )
        self.depression_strength = nn.Parameter(
            torch.tensor(depression_strength), requires_grad=False
        )
        self.discrete_amount = nn.Parameter(
            torch.tensor(discrete_amount), requires_grad=False
        )
        self.leniency = nn.Parameter(torch.tensor(leniency), requires_grad=False)

        # tracked values
        self.step_count = nn.Parameter(torch.tensor(0), requires_grad=False)
        self.n_sources = nn.Parameter(torch.tensor(0), requires_grad=False)
        self.source_order = nn.ParameterDict({})
        self.loss_history = nn.Parameter(
            torch.full((1, self.history_length + 1), float("nan")), requires_grad=False
        )
        self.sum_of_values = nn.Parameter(
            torch.full((1,), float("nan")), requires_grad=False
        )
        self.squared_sum_of_values = nn.Parameter(
            torch.full((1,), float("nan")), requires_grad=False
        )
        self.source_unreliability = nn.Parameter(
            torch.full((1,), 0.0), requires_grad=False
        )

        self.to(device)

    @staticmethod
    def shift_array_values(inputs, shifts: torch.LongTensor):
        n_rows, n_cols = inputs.shape
        arange_original = (
            torch.arange(n_cols, device=shifts.device)
            .view((1, n_cols))
            .repeat((n_rows, 1))
        )
        arange_new = (arange_original - shifts.reshape(-1, 1)) % n_cols

        return inputs[torch.arange(n_rows).reshape(-1, 1), arange_new]

    @staticmethod
    def _has_complete_history(loss_history):
        """
        Returns True if the history for at least two sources is complete.
        """
        return ~torch.isnan(loss_history[:, 1:]).any(dim=1)

    def _update_source_unreliability(
        self,
        sources_update_idx,
        sum_of_values,
        squared_sum_of_values,
        N,
        source_unreliability,
    ):
        """
        Updates the unreliability of the source with the given index and
        array of loss history sums and squarred sums.
        """

        # make sure new tensors are on the same device
        device = sum_of_values.device

        # get the indices of the sources that are updated
        source_update_bool = torch.arange(
            sum_of_values.shape[0], device=device
        ) == sources_update_idx.reshape(-1, 1)
        source_update_bool = source_update_bool[source_update_bool.any(dim=1)]

        # expand the weights and the sum of values to the same shape
        weights_expanded = torch.reshape(
            (
                1
                - torch.pow(
                    torch.tanh(
                        self.discrete_amount
                        * self.depression_strength
                        * source_unreliability
                    ),
                    2,
                )
            ).expand(source_update_bool.shape[0], source_unreliability.shape[0])[
                ~source_update_bool
            ],
            (source_update_bool.shape[0], source_unreliability.shape[0] - 1),
        )
        sum_of_values_expanded = torch.reshape(
            (sum_of_values).expand(source_update_bool.shape[0], sum_of_values.shape[0])[
                ~source_update_bool
            ],
            (source_update_bool.shape[0], sum_of_values.shape[0] - 1),
        )
        squared_sum_of_values_expanded = torch.reshape(
            (squared_sum_of_values).expand(
                source_update_bool.shape[0], squared_sum_of_values.shape[0]
            )[~source_update_bool],
            (source_update_bool.shape[0], squared_sum_of_values.shape[0] - 1),
        )

        # calculate the mean and std
        mean_source_loss = sum_of_values[sources_update_idx] / N
        mean_not_source_loss = torch.sum(
            sum_of_values_expanded * weights_expanded, axis=1
        ) / (torch.sum(weights_expanded, axis=1) * N)
        std_not_source_loss = torch.sqrt(
            torch.sum(squared_sum_of_values_expanded * weights_expanded, axis=1)
            / (torch.sum(weights_expanded, axis=1) * N)
            - mean_not_source_loss**2
        )

        stable_source = ~torch.isclose(
            std_not_source_loss, torch.tensor(0, device=device).float()
        )

        movement = torch.zeros_like(stable_source).float()

        movement[stable_source] = torch.where(
            mean_source_loss[stable_source]
            < mean_not_source_loss[stable_source]
            + self.leniency * std_not_source_loss[stable_source],
            -1,
            +1,
        ).float()

        source_unreliability[sources_update_idx] += movement
        source_unreliability = torch.clamp(source_unreliability, min=0.0)

        return source_unreliability

    def _get_source_unrelaibility(self):
        """
        The calculated unreliability of each source.
        The larger the value, the less reliable the source.
        """
        source_list = list(self.source_order.keys())
        # sorted source list
        source_list = sorted(source_list)
        source_idx = []
        for source in source_list:
            source_idx.append(self.source_order[source])

        return [self.source_unreliability[s_i].item() for s_i in source_idx]

    def _get_source_order(self):
        """
        The order of the sources in the source unreliability.
        This is because sources are ordered by their appearance
        during training.
        """
        source_list = list(self.source_order.keys())
        # sorted source list
        source_list = sorted(source_list)
        return source_list

    @property
    def source_unreliability_(self):
        return {
            s: u
            for s, u in zip(
                self._get_source_order(),
                self._get_source_unrelaibility(),
            )
        }

    def forward(
        self,
        losses: torch.tensor,
        sources: torch.tensor,
        writer=None,
        writer_prefix: typing.Optional[str] = None,
    ) -> torch.tensor:
        """
        Arguments
        ----------

        - losses: torch.Tensor of shape (batch_size,):
            The losses for each example in the batch.

        - sources: torch.Tensor of shape (batch_size,):
            The source for each example in the batch.

        - writer: torch.utils.tensorboard.SummaryWriter, optional:
            A tensorboard writer can be passed into this function to track metrics.
            Defaults to :code:`None`.

        - writer_prefix: str, optional:
            A prefix to add to the writer metrics.
            Defaults to :code:`None`.

        Returns
        --------

        - output: torch.Tensor of shape (batch_size,):
            The weighted losses for each example in the batch.


        """

        input_device = losses.device

        device = self.loss_history.device

        losses = losses.to(device)
        sources = sources.to(device)

        unique_sources = torch.unique(sources)
        to_sum = (sources == unique_sources.reshape(-1, 1)).float()
        mean_source_loss = to_sum @ losses / to_sum.sum(dim=1)

        # update the source_order dict
        for source in unique_sources:
            source = str(source.item())
            # adding new sources to the tracker, row to the loss history,
            # and a new entry to the source_unreliability tensor
            # and sum_of_values and squared_sum_of_values
            if source not in self.source_order:
                self.source_order[source] = self.n_sources.item()
                self.n_sources += 1
                self.loss_history = nn.Parameter(
                    torch.cat(
                        (
                            self.loss_history,
                            torch.full(
                                (1, self.history_length + 1),
                                float("nan"),
                                device=device,
                            ),
                        ),
                        dim=0,
                    ),
                    requires_grad=False,
                )
                self.source_unreliability = nn.Parameter(
                    torch.cat(
                        (self.source_unreliability, torch.zeros(1, device=device)),
                        dim=0,
                    ),
                    requires_grad=False,
                )
                self.sum_of_values = nn.Parameter(
                    torch.cat(
                        (
                            self.sum_of_values,
                            torch.full((1,), float("nan"), device=device),
                        ),
                        dim=0,
                    ),
                    requires_grad=False,
                )
                self.squared_sum_of_values = nn.Parameter(
                    torch.cat(
                        (
                            self.squared_sum_of_values,
                            torch.full((1,), float("nan"), device=device),
                        ),
                        dim=0,
                    ),
                    requires_grad=False,
                )

        source_idx = torch.tensor(
            [self.source_order[str(s.item())] for s in unique_sources]
        )

        # update the loss history
        shifts = torch.zeros(self.loss_history.shape[0]).long()
        shifts[source_idx] = -1

        # shift the loss history
        self.loss_history = nn.Parameter(
            self.shift_array_values(self.loss_history, shifts=shifts),
            requires_grad=False,
        )

        # update the loss history with the mean loss for each source given
        self.loss_history[source_idx, -1] = mean_source_loss

        # get the loss history for the sources with complete history
        complete_history = self._has_complete_history(self.loss_history)

        source_idx_to_update = torch.tensor(
            [
                self.source_order[str(s.item())]
                for s in unique_sources
                if complete_history[self.source_order[str(s.item())]]
            ]
        )

        depression_values = torch.zeros(
            self.loss_history.shape[0], device=device
        ).float()

        if (
            (sum(complete_history) >= 2)
            and (self.step_count >= self.warmup_iters)
            and len(source_idx_to_update) > 0
        ):
            loss_history_full = self.loss_history[complete_history]
            source_unreliability_full = self.source_unreliability[complete_history]

            sum_of_values = self.sum_of_values[complete_history]
            squared_sum_of_values = self.squared_sum_of_values[complete_history]

            # if the sum_of_values and squared_sum_of_values is nan
            # at a given index, set it to the sum of the loss history from [1:]
            # and the squared sum of the loss history from [1:]
            # if not nan, then take away the first value and add the last value
            nan_idx = torch.isnan(sum_of_values)
            sum_of_values = torch.where(
                nan_idx, loss_history_full[:, 1:].sum(axis=1), sum_of_values
            )
            squared_sum_of_values = torch.where(
                nan_idx,
                (loss_history_full[:, 1:] ** 2).sum(axis=1),
                squared_sum_of_values,
            )

            sources_complete_idx_to_update = (
                torch.cumsum(complete_history, dim=0)[source_idx_to_update] - 1
            )

            # but we do not want to update the sums if there was no
            # change in the loss history or if we just summed them
            # above
            sums_idx_to_update = sources_complete_idx_to_update[
                ~nan_idx[sources_complete_idx_to_update]
            ]

            sum_of_values[sums_idx_to_update] = (
                sum_of_values[sums_idx_to_update]
                - loss_history_full[sums_idx_to_update, 0]
                + loss_history_full[sums_idx_to_update, -1]
            )
            squared_sum_of_values[sums_idx_to_update] = (
                squared_sum_of_values[sums_idx_to_update]
                - loss_history_full[sums_idx_to_update, 0] ** 2
                + loss_history_full[sums_idx_to_update, -1] ** 2
            )

            source_unreliability_full = self._update_source_unreliability(
                sources_complete_idx_to_update,
                sum_of_values,
                squared_sum_of_values,
                self.history_length,
                source_unreliability_full,
            )

            source_unreliability_full_to_update = source_unreliability_full[
                sources_complete_idx_to_update
            ]

            self.sum_of_values[complete_history] = sum_of_values
            self.squared_sum_of_values[complete_history] = squared_sum_of_values

            self.source_unreliability[source_idx_to_update] = (
                source_unreliability_full_to_update
            )
            depression = self.discrete_amount * source_unreliability_full_to_update

            depression_values[source_idx_to_update] = depression

        multiplier = 1 - torch.pow(
            torch.tanh(depression_values * self.depression_strength), 2
        )

        multiplier_out = torch.zeros_like(losses)
        for s, s_idx in zip(unique_sources, source_idx):
            multiplier_out[sources == s] = multiplier[s_idx]

        # logging the unreliability of each source
        if writer is not None:
            for source in unique_sources:
                source = source.item()
                source_idx = self.source_order[str(source)]
                # write the reliability of the source to tensorboard
                writer.add_scalar(
                    (
                        f"unreliability/source_{source}"
                        if writer_prefix is None
                        else f"{writer_prefix}/unreliability/source_{source}"
                    ),
                    self.source_unreliability[source_idx].cpu().item(),
                    self.step_count.cpu().item(),
                )
                # write the loss of the source to tensorboard
                writer.add_scalar(
                    (
                        f"depression_multiplier/source_{source}"
                        if writer_prefix is None
                        else f"{writer_prefix}/depression_multiplier/source_{source}"
                    ),
                    multiplier[self.source_order[str(source)]].cpu().item(),
                    self.step_count.cpu().item(),
                )
                # write the loss of the source to tensorboard
                writer.add_scalar(
                    (
                        f"loss/source_{source}"
                        if writer_prefix is None
                        else f"{writer_prefix}/loss/source_{source}"
                    ),
                    torch.mean(losses[sources == source]).cpu().cpu().item(),
                    self.step_count.cpu().item(),
                )

        self.step_count += 1

        output = losses * multiplier_out

        self.sum_of_values = nn.Parameter(self.sum_of_values, requires_grad=False)
        self.squared_sum_of_values = nn.Parameter(
            self.squared_sum_of_values, requires_grad=False
        )
        self.source_unreliability = nn.Parameter(
            self.source_unreliability, requires_grad=False
        )
        self.loss_history = nn.Parameter(self.loss_history, requires_grad=False)

        return output.to(input_device)
