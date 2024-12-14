from setuptools import setup, find_packages

setup(
    name="Weather",
    version="1.0.0",
    author="David Rose",
    description="A Python application for weather tracking using PyQt5.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidrose07/Weather",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt5>=5.15.0",
        "requests>=2.31.0",
        "geopy>=2.3.0",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "weather=main:main",
        ],
    },
)
