import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-urley",
    author="Tim O'Farrell",
    author_email="tofarr@gmail.com",
    description="A tight standard for converting json objects to and from URL parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofarr/json-urley",
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=[],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "black~=23.3",
            "pytest~=7.2",
            "pytest-cov~=4.0",
            "pytest-xdist~=3.2",
            "pylint~=3.0",
        ],
    },
    setup_requires=["setuptools-git-versioning"],
    setuptools_git_versioning={"enabled": True, "dirty_template": "{tag}"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
