from setuptools import find_packages, setup

# Read the contents of README.md for the long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-linkup",
    version="0.1.6",
    author="LINKUP TECHNOLOGIES",
    author_email="contact@linkup.so",
    description="A Langchain integration for the Linkup API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LinkupPlatform/langchain-linkup",
    project_urls={
        "Documentation": "https://github.com/LinkupPlatform/langchain-linkup#readme",
        "Source Code": "https://github.com/LinkupPlatform/langchain-linkup",
        "Issue Tracker": "https://github.com/LinkupPlatform/langchain-linkup/issues",
    },
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="linkup api langchain integration search retriever",
    packages=find_packages(),
    package_data={"langchain_linkup": ["py.typed"]},
    python_requires=">=3.9,<4.0",  # Like langchain
    install_requires=[
        "langchain-core",
        "linkup-sdk>=0.2.8",
    ],
)
