from setuptools import setup, find_packages

VERSION = "0.7.1"
DESCRIPTION = 'Allows simple access to the current state of connected Xbox controllers on Windows.'

setup(name='pyxboxcontroller',
    version = VERSION,
    description = DESCRIPTION,
    license = "MIT",
    author = 'Dan Forbes',
    author_email = 'danielforbes.123412@gmail.com',
    url = 'https://github.com/SimpleHydrogen/pyxboxcontroller',
    packages = find_packages(),
    keywords = ["xbox controller",
                "XInput",
                "xbox",
                "controller",
                "python",
                "xbox-controller",
                "xboxcontroller"],
    long_description = """
    Utilises the XInput library(https://learn.microsoft.com/en-gb/windows/win32/xinput/getting-started-with-xinput).
    See github for more details: (https://github.com/SimpleHydrogen/pyxboxcontroller)
    """,
    classifiers = [
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    ]
)
