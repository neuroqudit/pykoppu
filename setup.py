from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pykoppu",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "networkx",
        "brian2",
        "mkdocs",
        "matplotlib",
    ],
    author="KOPPU Team",
    author_email="contact@koppu.io",
    description="SDK for KOPPU (K-dimensional Organoid Probabilistic Processing Unit)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koppu/pykoppu",
    project_urls={
        "Bug Tracker": "https://github.com/koppu/pykoppu/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3.8',
)
