from setuptools import setup, find_packages

setup(
    name="pybotforge",
    version="0.1.0",
    author="Your Name",
    description="A simplified framework for creating Discord bots in Python.",
    packages=find_packages(),
    install_requires=["discord.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)