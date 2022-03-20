from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name="dojogame",
    version="0.1.2",
    description="wrapper for pygame",
    long_description="WIP",
    long_description_content_type="text/markdown",
    url="https://github.com/Dojopy2D/Dojopy2D",
    author="Miguel González",
    author_email="migouche.g.r@gmail.com",
    license="GPL",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: Games/Entertainment"
    ],
    packages=["dojogame"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["pygame"]
)
