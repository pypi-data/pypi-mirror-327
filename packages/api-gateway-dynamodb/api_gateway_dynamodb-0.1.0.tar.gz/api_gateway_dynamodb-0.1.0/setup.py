from setuptools import setup, find_packages

setup(
    name="api-gateway-dynamodb",  # Your package name
    version="0.1.0",  # Update as needed
    author="Msizi Gumede",
    author_email="msizi@cyberneticbg.com",
    description="Library for interacting with API Gateway and DynamoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MsiziGCBG/api-gateway-dynamodb",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
