from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='zeusai',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Hugo Santos',
    author_email='contato@hugosantos.lol',
    description='Uma biblioteca simples para interagir com a API ZeusAI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
