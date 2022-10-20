from setuptools import setup, find_packages

VERSION = "0.1.3"
DESCRIPTION = 'This module allows for accessing the current state of a connected Xbox controller on Windows via the XInput library(https://learn.microsoft.com/en-gb/windows/win32/xinput/getting-started-with-xinput).'

setup(name='pyxboxcontroller',
    version = VERSION,
    description = DESCRIPTION,
    license = "MIT",
    author = 'Dan Forbes',
    author_email = 'danielforbes.123412@gmai.com',
    url = 'https://github.com/SimpleHydrogen/pyxboxcontroller',
    packages = find_packages(),
    keywords = ["xbox controller", "XInput", "xbox", "controller"],
    long_description = "See github for more details: (https://github.com/SimpleHydrogen/pyxboxcontroller)",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    ]
)