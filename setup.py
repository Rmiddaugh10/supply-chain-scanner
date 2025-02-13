from setuptools import setup, find_packages

setup(
    name="supply-chain-scanner",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
        "typing-extensions>=4.7.1",
        "pyyaml>=6.0.1",
        "dataclasses-json>=0.5.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.4.1",
        ]
    },
    author="Robert Lee Middaugh II",
    author_email="hguaddim@gmail.com",
    description="A security scanner for supply chain systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="security, supply-chain, scanner, container-security",
    url="https://github.com/Rmiddaugh10/supply-chain-scanner",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
