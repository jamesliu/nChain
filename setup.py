from setuptools import setup, find_packages

setup(
    name="nanochain",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "annoy"
        # ... other dependencies
    ],
    entry_points="""
        [console_scripts]
        nchain=nanochain.cli:cli
    """,
)


