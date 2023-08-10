MicroGP4
========

[![License: Apache 2.0](https://img.shields.io/badge/license-apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Status: Actrive](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/squillero/microgp3)
![Language: Python](https://img.shields.io/badge/language-python-blue.svg)
![Version: 4!2](https://img.shields.io/badge/version-4!2-orange.svg)
![Codename: Meaning of Liff](https://img.shields.io/badge/codename-Meaning_of_Liff-orange.svg)
[![Documentation Status](https://readthedocs.org/projects/microgp4/badge/?version=pre-alpha)](https://microgp4.readthedocs.io/en/pre-alpha/?badge=pre-alpha)


MicroGP (µGP, `ugp`)  is an [evolutionary tool](https://squillero.github.io/microgp4/evolution.html) created around 2001. Over the years it has been exploited as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing), as a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization), and as a framework for prototyping and testing new ideas. [Some hundreds documents](https://scholar.google.com/scholar?q=%28+MicroGP+OR+%C2%B5GP+OR+ugp3+OR+ugp2+%29+AND+%28+Squillero+OR+Tonda+OR+Sanchez+OR+Schillaci+%29) discussing it and possible application can be found in the scientific literature. [**[read more]**](https://microgp4.readthedocs.io/en/pre-alpha/summary.html)

### ⚠️ MicroGP4 v2.0 is currently in [pre-alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Pre-alpha) and under active development

## Installation

MicroGP4 is available in PyPi

```shell
pip install -U psutils matplotlib joblib
pip install -U microgp4
```

This repo is only useful if you want to hack the code (see: [CONTRIBUTING](CONTRIBUTING.md)). 

**TL;DR**

* The default branch is always the more stable
* Do not clone experimental branches `exp/*` unless you know what you are doing
* Follow this [style guide](https://github.com/squillero/style/blob/master/python.md) and keep the code formatted with [Black](https://black.readthedocs.io/en/stable/)
* Write as few lines of code and as much line of comments as possible (ie. use builtins, exploit generators and list comprehension)
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (ie. `coverage run -m pytest`)
* Use [pylint](https://mypy-lang.org/) for basic linting and [mypy](https://mypy-lang.org/) for additional type checking
* Be [paranoid](./PARANOIA.md) (cit. *"I need someone to show me the things"*)
* It may be wise to contact Alberto or Giovanni before trying to change anything

### Contacts

* [Alberto](https://github.com/albertotonda/) [:email:](mailto:alberto.tonda@inra.fr) [:house:](https://www.researchgate.net/profile/Alberto_Tonda)
* [Giovanni](https://github.com/squillero) [:email:](mailto:squillero@polito.it) [:house:](https://staff.polito.it/giovanni.squillero/)

### Licence
Copyright © 2022-23 Giovanni Squillero and Alberto Tonda  
MicroGP4 is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
