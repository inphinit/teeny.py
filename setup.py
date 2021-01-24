from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="teeny-pkg-inphinit",
    version="0.0.1",
    author="Guilherme Nascimento",
    author_email="brcontainer@yahoo.com.br",
    description="A teeny route system for Python, with WSGI for production or http.server (Lib/http/server.py) for development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inphinit/teeny.py",
    packages=["teeny"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
