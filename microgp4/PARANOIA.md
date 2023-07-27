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

 and it is not easy to specify the `-O` flag.