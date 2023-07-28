# PARANOIA MODE

In **production**, MicroGP is typically run from a non-interactive script, for example on a server with ssh access. In this context, performance is critical, while verbosity should be minimal. During the **setup**, on the other hand, the user needs to check the various parameters and the coherence of the constraints. Here, speed is not essential, while warnings and hints can be quite useful. 

MicroGP's *paranoia checks* are computationally intensive routines  that thoroughly analyze and verify both the integrity of the internal data structures and the  parameter values, providing error messages and hints. *Paranoia checks* are supposed to be used only during the setup phase, and they are automatically removed when an optimization flag is used.

## Terminal

If *paranoia checks* are enabled, the user is warned of the potential, indeed almost certain, loss in performance:

> Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'

And the user may disable them by using an optimization flag:

```sh
$ python -O ./my-fuzzer.py
```

## Jupyter Notebooks

MicroGP detects when it is within a Jupyter Notebook and shows a warning:

> Paranoia checks are always enabled in notebooks: performances can be significantly impaired  
> See https://github.com/squillero/microgp4/blob/pre-alpha/PARANOIA.md for details

In Jupyter it is not possible to specify an optimization flag for the imported modules, but there are possible workarounds.

### Set `PYTHONOPTIMIZE`

According to the [documentation](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE): Setting the environment variable `PYTHONOPTIMIZE` to a non-empty string it is equivalent to specifying the `-O` option. 

Thus, it may be enough to start Jupyter with:

```shell
$ PYTHONOPTIMIZE=1 jupyter-notebook
```

### Export to Script

* In Jupyter, from menu `File`, choose `Save and Export Notebook As...`, and then `Executable Script`.
* Run the script from the terminal with `python -O ./my-exported-fuzzer.py`

Usually no editing is needed.

### Cell Magic

Jupyter allows some of the IPython's [magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html), and a *cell magic* (`%%`) can be used to start a Python interpreter with optimization flags:

```jupyterpython
%%python -O

import microgp4 as ugp

# My fuzzer goes here
```

* :+1: May be used in remote Notebooks (e.g., [Google's Colab](https://colab.research.google.com/))
* :-1: All the user code must be packed into one single cell
* :-1: MicroGP will not detect Jupyter anymore

### Tamper with bytecode cache

:warning: This hack may cause the system to become unstable, to provide incorrect results, to stop functioning, or to explode. You acknowledge that you are solely responsible for any harm or damage that may result.

* Generate the optimized bytecode (e.g., run `python -O -m pytest`)
* Locate all the folders that contain compiled bytecode (e.g., `**/__pycache__`)
* Substitute all bytecode-compiled files (e.g., `*.pyc`) with their optimized versions (e.g., `*.opt-1.pyc`)
* Stop updating MicroGP files
