from setuptools import setup, find_packages

VERSION = "0.5"
DESCRIPTION = 'This module allow simple access to the current state of connected Xbox controllers on Windows via the XInput library(https://learn.microsoft.com/en-gb/windows/win32/xinput/getting-started-with-xinput).'

setup(name='pyxboxcontroller',
    version = VERSION,
    description = DESCRIPTION,
    license = "MIT",
    author = 'Dan Forbes',
    author_email = 'danielforbes.123412@gmail.com',
    url = 'https://github.com/SimpleHydrogen/pyxboxcontroller',
    packages = find_packages(),
    keywords = ["xbox controller", "XInput", "xbox", "controller", "python", "xbox-controller", "xboxcontroller"],
    long_description = "See github for more details: (https://github.com/SimpleHydrogen/pyxboxcontroller)",
    classifiers = [
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    ]
)