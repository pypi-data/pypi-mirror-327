from setuptools import setup, find_packages

setup(
    name="yteva",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyrogram"
    ],
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple library to fetch and download audio using Pyrogram.",
    url="https://github.com/yourusername/yteva",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
