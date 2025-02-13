import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ADPOSPythonSDK",
    version="1.0.0",
    author="Adrian Albrecht",
    author_email="adriandevprojects@gmail.com",
    packages=setuptools.find_packages(),
    url="https://github.com/adriandevprojects/ADPOSPythonSDK",
    license="GPL-3.0",
    description="AdrianDevProjects Online Services Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
)