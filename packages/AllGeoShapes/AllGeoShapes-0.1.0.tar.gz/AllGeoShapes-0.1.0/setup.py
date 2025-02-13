from setuptools import setup, find_packages

setup(
    name="AllGeoShapes",  
    version="0.1.0",  
    packages=find_packages(),  
    install_requires=[],  
    author="Your Name",
    author_email="24b81a62e9@cvr.ac.in",
    description="A Python module for geometric shape calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shapemodule",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
