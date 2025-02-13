__version__ = "2.0a4"

# Available at setup time due to pyproject.toml
from setuptools import setup

setup(
    name="casm-bset",
    version=__version__,
    packages=[
        "casm",
        "casm.bset",
        "casm.bset.clexwriter",
        "casm.bset.cluster_functions",
        "casm.bset.polynomial_functions",
    ],
    install_requires=[],
)
