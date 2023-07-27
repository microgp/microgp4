# PARANOIA MODE

In **production phase**, MicroGP is typically run from a non-interactive script, for example on a server with ssh access. In this context, performance is critical, while verbosity should be minimal. During the **setup phase**, on the other hand, the user needs to check the various parameters and the coherence of the constraints. Here, speed is not essential, while any warnings and hints can be quite useful. 

MicroGP's *paranoia checks* are computationally intensive routines  that thoroughly analyze and verify both the integrity of the internal data structures and the  parameter values, providing error messages and hints. *Paranoia checks* are supposed to be used only during the setup phase: they are all automatically removed when an optimization flag is used.

## Terminal

If *paranoia checks* are active, the user is warned of the potential, indeed almost certain, loss in performance:

> Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'

And the user may disable them simply by using an optimization flag:

```sh
$ python -O ./my-fuzzer.py
```

## Jupyter Notebooks

MicroGP should detect when it is imported from a Jupyter Notebook:

```jupyter
Paranoia checks are always enabled in notebooks: performances can be significantly impaired
See https://github.com/squillero/microgp4/blob/pre-alpha/PARANOIA.md for details
```

However, it may not be easy to specify the `-O` flag. We suggest three possible solutions:

### Export to Script :+1: 

The is the suggested method, as simple as:

* From menu `File`, choose `Save and Export Notebook As...`, and then `Executable Script`.
* If needed, edit the file
* Run it with `python -OO`

### Cell Magic

IPython has a system of commands we call *magics*; cell magics use two percent characters as a marker `%%` and receive as argument both the current line where they are declared and the whole body of the cell (see: [Built-in magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html) in IPython).

The cell magic `%%python -O` can be used to execute the cell in a python interpreter with optimization flag

```jupyterpython
%%python -O

import microgp4 as ugp

"""My whole fuzzer here"""
```

Caveats:

* All the code must be put inside the same cell, all names defined in the cell are lost.
* MicroGP does not detect Jupyter anymore

### Tamper with `__pycache__` :-1:

Terrible, but you may want to try:

* Run some script with an optimized python `python -OO some-test.py` 
* Locate `__pycache__` dir
* Rename optimized bytecode (extension `.opt-2.pyc` on my computer) as common bytecode (extension `.pyc` on my computer)

Have fun