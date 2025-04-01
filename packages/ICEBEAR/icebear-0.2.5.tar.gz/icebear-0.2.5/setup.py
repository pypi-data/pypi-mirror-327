from setuptools import setup, find_packages

setup(
    name="ICEBEAR",
    version="0.2.5",
    packages=find_packages(),
    description="ENOTION",
    author="Chione Raphael",
    author_email="toan.nt@enotion.io",
    license="MIT",
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
