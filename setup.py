from setuptools import find_packages, setup
from distutils.core import setup
from os.path import join as pjoin

exec(open(pjoin("bytes32", "version.py")).read())
setup(
    name="bytes32",
    author="Ruoyao Wang, Graham Todd, Eric Yuan, Ziang Xiao, Marc-Alexandre Côté, Peter Jansen",
    version=__version__,
    install_requires=open('requirements.txt').readlines(),
    url="https://github.com/cognitiveailab/BYTESIZED32",
    description="Byte-sized text games for code generation tasks on virtual environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ]
)
