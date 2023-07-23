Contribute to MicroGP
=====================

First off all, thank you! :+1:

* [Join the team](#join-the-team)
* Use the tool and [report a success story](#report)
* Fail to use the tool and [submit a bug report](#report)
* [Fix a bug](#coding)
* [Add a brand new feature](#coding)
* [Improve an existing feature](#coding)
* Extend/update/proofread the documentation
* Draw logo/icons
* [~~Donate money~~](#money-donations)

### Join the team

Please, contact Alberto or Giovanni directly:

* If you enjoy playing with Python and Evolutionary Computation, and you are looking for a 6-month master thesis. Note: We are **always** looking for valuable students, even when there are no theses posted on the official channels.
* If you have a great idea for an improvement, but you are not sure how to hack it.
* If you feel like doing it.

### Reports

We use [GitHub's issues](https://github.com/squillero/microgp4/issues) for bug reporting. 

If you have published a paper using any version of MicroGP, please let us know.

Anyhow, feel free to send us an email describing your story. 

### Coding

This section contains notes for programmers interested in modifying μGP⁴.

#### TL;DR

* Write as few lines of code and as much line of comments as possible
* Use builtins whenever possible
* Exploit generators and list comprehension
* Follow this Python [style guide](https://github.com/squillero/style/blob/master/python.md).
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (i.e., `coverage run -m pytest`).
* Use [pylint](https://mypy-lang.org/) for linting (and possibly use also [mypy](https://mypy-lang.org/) for additional type checking.)

#### Asserts

Describe the error, do not state the correct alternative. Example:

> TypeError: unhashable type: 'list'

Have fun! And contact us if you want your code to be included in the next release.

## Money Donations

Thanks for trying, but we do not accept monetary donations:

* Alberto and Giovanni are working on MicroGP as an integral part of their research activities. Therefore, they are already paid by their institutions, namely: *Politecnico di Torino* (Italy); *INRAE — AgroParisTech* (France) and *Institut des Systèmes Complexes de Paris Île-de-France* (France).
* Students have worked, are working, and will work on MicroGP as part of their academic curricula, either for Master's theses or Ph.D. programs.
* A few volunteers did excellent work on specific topics, but as volunteers they did not ask for payment.

So, why not donating [**time**](#join-the-team) instead of money?
