from setuptools import setup, find_packages

setup(
    name="cert-coordination-observability",
    version="0.1.0",
    description="Mathematical framework for AI coordination observability",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "numpy>=1.24.3",
        "scipy>=1.11.1",
        "sentence-transformers>=2.2.2",
        "pydantic>=2.4.2",
    ],
    python_requires=">=3.8",
)