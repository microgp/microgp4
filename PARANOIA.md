# PARANOIA MODE

In **production**, MicroGP is typically run from a non-interactive script, for example on a server with ssh access. In this context, performance is critical, while verbosity should be minimal. During the **setup**, on the other hand, the user needs to check the various parameters and the coherence of the constraints. Here, speed is not essential, while warnings and hints can be quite useful. 

MicroGP's *paranoia checks* are computationally intensive routines  that thoroughly analyze and verify both the integrity of the internal data structures and the  parameter values, providing error messages and hints. *Paranoia checks* are supposed to be used only during the setup phase: they are automatically removed when an optimization flag is used.

## Terminal

If *paranoia checks* are active, the user is warned of the potential, indeed almost certain, loss in performance:

> Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'

And the user may disable them simply by using an optimization flag:

```sh
$ python -O ./my-fuzzer.py
```

## Jupyter Notebooks

MicroGP should detect when it is within a Jupyter Notebook:

> Paranoia checks are always enabled in notebooks: performances can be significantly impaired  
> See https://github.com/squillero/microgp4/blob/pre-alpha/PARANOIA.md for details

However, differently from scripts, it may not be easy to specify the `-O` flag. We suggest three possible solutions:

### Export to Script

:+1: The suggested method, as simple as:

* From menu `File`, choose `Save and Export Notebook As...`, and then `Executable Script`.
* Run it with `python -O ./my-exported-fuzzer.py`

Usually no editing is needed.

### Cell Magic

IPython has a system of commands known as *cell magic* (see: [built-in magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html) in IPython documentation).

`%%python -O` can be used to execute a whole cell in a Python interpreter with optimization flag

```jupyterpython
%%python -O

import microgp4 as ugp

"""My whole fuzzer here"""
```

Problems:

* **All** the code must be inside this single cell
* MicroGP does not detect Jupyter anymore

### Tamper with `__pycache__`

:warning: This hack may cause the system to become unstable, to provide incorrect results, or to stop functioning completely. You acknowledge that you are solely responsible for any harm or damage that may result.

Someone may want to try:

* Generate the optimized bytecode, e.g., running `python -OO -m pytest` 
* Locate the `__pycache__` directory
* Substitute the unoptimized bytecode files (`*.pyc` on my computer) with their optimized version (`*.opt-2.pyc` on my computer)
