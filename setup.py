import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="govee-api-ble",
    version="0.0.3",
    author="Leah Snodgrass",
    author_email="soft@null.net",
    description="Python API for Govee H6127 RGB lighting strips ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/softgrass/govee-api-ble",
    project_urls={
        "Bug Tracker": "https://github.com/softgrass/govee-api-ble/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
