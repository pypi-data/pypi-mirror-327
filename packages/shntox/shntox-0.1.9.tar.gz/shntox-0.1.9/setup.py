from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name="shntox",
    version="0.1.9",
    packages=find_packages(),
    include_package_data=True,  # Bu satırı ekleyin
    author="sahin",
    description="Algebra library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires=">=3.6",
)
