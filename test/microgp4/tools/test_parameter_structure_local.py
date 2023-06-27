from abc import ABCMeta
from microgp4.classes.node_reference import NodeReference
from microgp4.framework.parameter_structural_global import _global_reference
from microgp4.framework.parameter_structural_global import *
from microgp4.framework.parameter_structural_local import *
from microgp4.user_messages.exception import MicroGPInvalidIndividual
from microgp4.tools.graph import get_siblings
import pytest
from typing import Type, List
from microgp4.framework.parameter_structural_local import _local_reference
