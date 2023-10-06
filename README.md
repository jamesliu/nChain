# nanoChain

[![PyPI](https://img.shields.io/pypi/v/nanoChain.svg)](https://pypi.org/project/nanoChain/)
[![Changelog](https://img.shields.io/github/v/release/jamesliu/nanoChain?include_prereleases&label=changelog)](https://github.com/jamesliu/nanoChain/releases)
[![Tests](https://github.com/jamesliu/nanoChain/workflows/Test/badge.svg)](https://github.com/jamesliu/nanoChain/actions?query=workflow%3ATest)
[![Documentation Status](https://readthedocs.org/projects/nanoChain/badge/?version=stable)](http://nanoChain.readthedocs.org/en/stable/?badge=stable)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jamesliu/nanoChain/blob/main/LICENSE)

nanoChain is a Python package that provides a simple and efficient implementation of 

## Installation

You can install nanoChain directly from PyPI using pip:

```bash
pip install nanoChain
```

Alternatively, you can clone the repository and install from source:

```bash
git clone https://github.com/jamesliu/nanoChain.git
cd nanoChain
pip install .
```

## Usage

Here are examples of how to use nanoChain to search ArXiv paper using embedding.

```bash
nchain add https://arxiv.org/abs/2010.14701
nchain add https://arxiv.org/abs/2302.01318v1
nchain add https://arxiv.org/abs/2309.17453

nchain query "Show me the Scaling Laws for Autoregressive Generative Modeling."
nchain query "Show me the algorithm about Large Lanuage Model Decoding with Speculative Sampling."
nchain query "How to handle streaming apps efficiently in LLM?"
```

## Examples
See the [examples](./examples) directory for more comprehensive usage examples.

## Documentation

Full documentation is available [here](https://nanochain.readthedocs.io/en/latest/).

## Contributing

We welcome contributions to nanoChain! If you're interested in contributing, please see our [contribution guidelines](./CONTRIBUTING.md) and [code of conduct](./CODE_OF_CONDUCT.md).

## License

nanoChain is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for more details.

## Support

For support, questions, or feature requests, please open an issue on our [GitHub repository](https://github.com/jamesliu/nanoChain/issues) or contact the maintainers.

## Changelog

See the [releases](https://github.com/jamesliu/nanoChain/releases) page for a detailed changelog of each version.


