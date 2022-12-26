import setuptools

from json_urley.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-urley",
    version=__version__,
    author="Tim O'Farrell",
    author_email="tofarr@gmail.com",
    description="A tight standard for converting json objects to and from URL parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofarr/json-urley",
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
