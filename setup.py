from setuptools import setup, find_packages

setup(
    name="pykoppu",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "networkx",
        "brian2",
        "mkdocs",
    ],
    author="KOPPU Team",
    description="SDK for KOPPU (K-dimensional Organoid Probabilistic Processing Unit)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
