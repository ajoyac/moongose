import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moongose",
    version="0.0.24",
    author="Alejandro Joya",
    author_email="joya.a.cruz@gmail.com",
    description="python sdk to interact with Basilisk Challenges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajoyac/moongose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'requests'
    ]
)