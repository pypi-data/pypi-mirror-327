from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="loss_adapted_plasticity",
    version="0.1.8",
    description="A python package for training neural networks on noisy data sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexcapstick/loss_adapted_plasticity",
    author="Alexander Capstick",
    author_email="alexander.capstick19@imperial.ac.uk",
    license="MIT",
    packages=["loss_adapted_plasticity"],
    install_requires=[
        "numpy",
        "torch",
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
