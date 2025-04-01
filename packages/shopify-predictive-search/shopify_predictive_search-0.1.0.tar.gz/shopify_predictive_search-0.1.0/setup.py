from setuptools import setup, find_packages

# Try to read README.md, but use a default description if file is not found
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A Shopify search product using the Storefront API"

setup(
    name="shopify-predictive-search",  
    version="0.1.0",
    author="Truenary",
    author_email="marga.ghale@truenary.com",
    description="A Shopify search product using the Storefront API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ysuren/pl9-tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "pydantic==2.5.3",
    ],
    entry_points={
        'console_scripts': [
            'shopify-search=src.main:main',  # Adjust this based on your actual module structure
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)