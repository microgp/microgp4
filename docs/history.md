# The story so far...

## MicroGP1

> Unreleased

The study of an evolutionary tool for generating *real* assembly programs started around 2000. The first operational version dates back to 2001: it was composed of a few hundred lines of C code, plus a collection of scripts hacked together to test the feasibility of the idea (DOI: [10.1109/CEC.2002.1004462](http://dx.doi.org/10.1109/CEC.2002.1004462)). It has been retroactively labelled *MicroGP1*, although no specific name was used at the time.

MicroGP1 internally stores an assembly program as a directed acyclic graphs, where  each node encodes a fragment of code with some parameters. Evolution proceeds by tweaking the topology of the graph_manager and modifying the parameters
inside the nodes. The graph_manager is eventually transformed into a valid assembly-language program in order to be evaluated, that is, assembled, linked and executed.

## MicroGP2

> Copyright © 2002-2006 Giovanni Squillero; distributed under 
[GPL2](https://www.tldrlegal.com/l/gpl2);
available on [GitHub](https://github.com/squillero/microgp2).

As its predecessor, MicroGP2 internally encodes programs as graphs (directed multigraphs, this time), but it allows to load the list of the parametric code fragments (*macros*) from a file, targeting a specific microprocessor (hence the micro in the name). The evolutionary core has been completely re-designed looking at the *Genetic Programming* paradigm (hence the GP in the name). 

MicroGP2 was originally coded in C in a frenzy week while recovering from [varicella](https://en.wikipedia.org/wiki/Chickenpox), and the first release was named *Chicken Pox*. The initial development has been supported by Intel through a grant named *"GP Based Test Program generation"*; the final release (*April Fool*) consists of about 15,000 lines. It is described in the paper *MicroGP — An Evolutionary Assembly Program Generator* (DOI: [10.1007/s10710-005-2985-x](http://dx.doi.org/10.1007/s10710-005-2985-x)). 

Over the years, MicroGP2 was mainly exploited by engineers for the test and verification of small microprocessors, but it was also able to scale up tackling the post-silicon validation of a real Pentium 4 (DOI: [10.1109/MTV.2004.5](http://dx.doi.org/10.1109/MTV.2004.5)). In a far less mundane research, it created the first *machine-written programs* ever able to become *King of the Hill* in all the main international *core-war* competitions (DOI: [10.1109/TEVC.2005.856207](http://dx.doi.org/10.1109/TEVC.2005.856207)).

With time, MicroGP2 has been coerced into solving problems it was not meant for, such as design of the bayesian networks, the creation of mathematical functions represented as trees, integer and combinatorial optimization, real-value parameter optimization. Ultimately it was re-implemented from scratch in C++.

## MicroGP3

> Copyright © 2006-2016 Giovanni Squillero; distributed under 
[GPL3](https://www.tldrlegal.com/l/gpl-3.0);
available on both [GitHub](https://github.com/squillero/microgp3) 
and [Sourceforge](https://sourceforge.net/projects/ugp3/).

MicroGP3 brought a complete change of paradigm: the focus goes from the problem to the tool, and the main design goal shifts from the solution of a specific class of problems to the development of a tool that can tackle a wide range of possible applications.

The development of the third version started in 2006 (release: *Noodle Soup*) with the intent to provide a clean implementation able to replicate the behavior of the previous version. The subsequent releases were *Bluebell* (2010), discribed in the book *Evolutionary Optimization: the µGP toolkit* (DOI: [10.1007/978-0-387-09426-7](https://www.doi.org/10.1007/978-0-387-09426-7)); *Mistletoe* (2012); *PalmTree* (2014); and *Camellia* (2015). The coding of *Thuban* was eventually discontinued in 2016.

## MicroGP4

> Copyright © 2022 Giovanni Squillero and Alberto Tonda; distributed under [Apache-2.0](https://www.tldrlegal.com/l/apache2); available on [GitHub](https://github.com/squillero/microgp4).

MicroGP4 has been re-designed in Python to take advantage of the peculiar features of the language and of its huge standard library. It further increases usability thanks to state-of-the-art cooperative platforms: the tool is available as a [PyPi package](https://en.wikipedia.org/wiki/Python_Package_Index), and the full documentation is going to be hosted on [Read the Docs](https://en.wikipedia.org/wiki/Read_the_Docs). 

**Notez Bien**: MicroGP4 is an active project and it is currently in [pre-alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Pre-alpha).