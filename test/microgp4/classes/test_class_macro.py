import pytest
from collections import defaultdict
from microgp4.classes.checkable import Checkable
from microgp4.classes.evolvable import EvolvableABC
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.node_view import NodeView
from microgp4.classes.parameter import ParameterABC
from microgp4.classes.macro import Macro 


@pytest.fixture
def macro():
    class TestMacro(Macro):
        TEXT = 'test'
        PARAMETERS = {}
        EXTRA_PARAMETERS = {}

    return TestMacro()


@pytest.fixture
def parameter_abc():
    class TestParameterABC(ParameterABC):
        def mutate(self, strength: float = 1., **kwargs) -> None:
            pass

    return TestParameterABC()


@pytest.fixture
def node_view():
    class TestNodeView(NodeView):
        def __init__(self):
            pass

    return TestNodeView()


def test_macro_initialization(macro):
    assert isinstance(macro, Macro)
    assert isinstance(macro, EvolvableABC)
    assert isinstance(macro, Checkable)
    assert macro.parameters == {}


def test_macro_eq(macro):
    same_macro = macro
    assert macro == same_macro

    different_macro = Macro()
    assert macro != different_macro


def test_macro_is_valid(macro, node_view):
    assert macro.is_valid(node_view)


def test_macro_text(macro):
    assert macro.text == 'test'


def test_macro_extra_parameters(macro):
    assert macro.extra_parameters == {}


def test_macro_parameter_types(macro):
    assert macro.parameter_types == {}


def test_macro_str(macro):
    assert str(macro) == 'TestMacro'


def test_macro_dump(macro):
    extra_parameters = ValueBag({'test': 'value'})
    assert macro.dump(extra_parameters) == 'test'


def test_macro_mutate(macro, parameter_abc):
    macro.parameters = {'test': parameter_abc}
    macro.mutate(0.5)  

def test_macro_is_name_valid():
    assert Macro.is_name_valid('test') 
    assert not Macro.is_name_valid(123)
