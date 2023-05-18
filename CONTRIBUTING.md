Contributing to MicroGP
=======================

First off all, thanks! :+1:

* [Join the team](#join-the-team)
* Use the tool and [report a success story](#report)
* Fail to use the tool and [submit a bug report](#report)
* [Fix a bug](#coding)
* [Add a brand new functionality](#coding)
* [Improve an existing functionality](#coding)
* Extend/update/proofread the documentation
* Draw logo/icons
* [~~Donate money~~](#money-donations)

### Join the team

Please, contact directly Alberto or Giovanni:

* If you enjoy playing with Python and Evolutionary Computation, and you are looking for a 6-month master thesis. Note: We are **always** looking for valuable students, even when there are no theses advertised on the official channels.
* If you have a great idea about an improvement, but you are not sure how to hack it.
* If you feel like doing it.

### Reports

We use [GitHub's issues](https://github.com/squillero/microgp4/issues) for reporting bugs. 

If you published a papers using any version of MicroGP, please let us know.

Anyhow, feel free to write us an email describing your story. 

### Coding

This sections contains notes for programmers interested in modifying μGP⁴.

#### TL;DR

* Write as few lines of code as possible
* Use builtins
* Exploit generators and list comprehensions
* Follow this Python [style guide](https://github.com/squillero/style/blob/master/python.md).
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (i.e., `coverage run -m pytest`).
* Use [pylint](https://mypy-lang.org/) for linting (and possibly use also [mypy](https://mypy-lang.org/) for additional type checking.)

#### Asserts

Describe the error, do not state the correct. Example:

> TypeError: unhashable type: 'list'

Have fun! And contact us if you want your code to be included in the next release.

## Money Donations

Thanks for trying, but we do not accept money donations:

* Alberto and Giovanni are working on MicroGP as an integral part of their research activities. Thus, they are already paid by their institutions, namely: *Politecnico di Torino* (Italy) and *French National Institute for Agricultural Research* (France).
* Students worked, are working, and will work on MicroGP for their academic curricula, either master theses or Ph.D. programs.
* A few volunteers did a terrific job on specific topics, but, being volunteers, they did not ask for a wage.

So, why not donating [**time**](#join-the-team) instead of money?