"""Setup file for Python lib."""
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="cloud_storage_manager",
    version="1.0",
    description="Codebase for Cloud Storage operations",
    url="https://github.com/mr-strawberry66/cloud-storage-manager",
    author="Sam Kenney",
    author_email="sam.kenney@me.com",
    license="MIT",
    long_description=long_description,
    platforms=[],
    install_requires=[
        "google-cloud-storage==1.42.3",
    ],
    packages=["cloud_storage_manager"]
    + [
        "cloud_storage_manager." + pkg for pkg in find_packages("cloud_storage_manager")
    ],
)
