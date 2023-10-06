from setuptools import setup, find_packages

setup(
    name="nchain",
    version="0.11",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "annoy",
        "arxiv"
        # ... other dependencies
    ],
    entry_points="""
        [console_scripts]
        nchain=nchain.cli:cli
    """
)
