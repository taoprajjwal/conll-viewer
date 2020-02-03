import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README=(HERE/"README.md").read_text()

setup(
    name="ColnnViewer",
    version="1.0.0",
    description="Visually representing a COLNN 2009 files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/taoprajjwal/conll-viewer/",
    author="Prajjwal Bhattarai",
    author_email="taoprajjwal@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["colnnviewer"],
    install_requires=["Pillow"],
)