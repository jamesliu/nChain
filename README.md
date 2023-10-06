# nChain

[![PyPI](https://img.shields.io/pypi/v/nChain.svg)](https://pypi.org/project/nChain/)
[![Changelog](https://img.shields.io/github/v/release/jamesliu/nChain?include_prereleases&label=changelog)](https://github.com/jamesliu/nChain/releases)
[![Tests](https://github.com/jamesliu/nChain/workflows/Test/badge.svg)](https://github.com/jamesliu/nChain/actions?query=workflow%3ATest)
[![Documentation Status](https://readthedocs.org/projects/nChain/badge/?version=stable)](http://nChain.readthedocs.org/en/stable/?badge=stable)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jamesliu/nChain/blob/main/LICENSE)

nChain is a Python package that provides a flexible and efficient implementation to create LLM bots over extensible dataset. 

## Installation

You can install nChain directly from PyPI using pip:

```bash
pip install nChain
```

Alternatively, you can clone the repository and install from source:

```bash
git clone https://github.com/jamesliu/nChain.git
cd nChain
pip install .
```

## Usage

Here are examples of how to use nChain to search ArXiv paper using embedding.

```bash
nchain add https://arxiv.org/abs/1409.0473
nchain add https://arxiv.org/abs/2010.14701
nchain add https://arxiv.org/abs/2203.02155
nchain add https://arxiv.org/abs/2302.01318v1
nchain add https://arxiv.org/abs/2309.17453
nchain add https://arxiv.org/abs/2310.02304

nchain query "Show me the Scaling Laws for Autoregressive Generative Modeling."
nchain query "Show me the algorithm about Large Lanuage Model Decoding with Speculative Sampling."
nchain query "How to handle streaming apps efficiently in LLM?"
```

## Documentation

Full documentation is available [here](https://nchain.readthedocs.io/en/latest/).

## Contributing

We welcome contributions to nChain! If you're interested in contributing, please see our [contribution guidelines](./CONTRIBUTING.md) and [code of conduct](./CODE_OF_CONDUCT.md).

## License

nChain is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for more details.

## Support

For support, questions, or feature requests, please open an issue on our [GitHub repository](https://github.com/jamesliu/nChain/issues) or contact the maintainers.

## Changelog

See the [releases](https://github.com/jamesliu/nChain/releases) page for a detailed changelog of each version.


