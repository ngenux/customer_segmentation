import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="customer_segmentation",
    version="0.1.4",
    description="Util files to regularize the date formats",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Dayananda Challa",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    #packages=["regularizer"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["kneed"],
)