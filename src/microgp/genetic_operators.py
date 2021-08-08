# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0 "Kiwi"     #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2020 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple
from .constraints import SubsectionsSequence, SubsectionsAlternative
from .individual import *
from .macro import Macro
from . import parameter
from .parameter import Information
from .utils import logging
from microgp import random_generator
import microgp as ugp4

# TODO: Add comments!
try:
    import matplotlib.cbook
    import matplotlib.pyplot as plt
except:
    plt = None


# TODO: Not here!
# TODO: Check. Urgent. (fall 2020)
def print_individual(individuals: Union[Individual, List[Individual]], msg: str = '', plot=False, score=False):
    # TODO: Double Check
    # TODO: Refactor
    """Prints one or more individuals and plots their graphs

    Args:
        individuals (Individual or List(Individual): individual/s to print/plot
        msg (str): message to print in the first line
        plot (bool): if True -> plot the graph_manager
        score (bool): if True -> Print fitness score after the printing phenotype
    """
    if isinstance(individuals, set):
        individuals = list(individuals)
    if not isinstance(individuals, list):
        individuals = [individuals]
    logging.bare(msg)
    for individual in individuals:
        for line in str(individual).splitlines():
            logging.bare(str(line))
        if plot:
            if not plt:
                import warnings
                WARN_PLT = "Can't plot individual without ``matplotlib''"
                warnings.warn(WARN_PLT, RuntimeWarning)
            else:
                individual.draw()
                if matplotlib.is_interactive():
                    plt.show()
                else:
                    plt.savefig(str(individual.id))
                    plt.close()

        if score:
            ugp4.logging.bare(f"Fitness score: {individual.fitness}\n")


# TODO: Check. Urgent. (fall 2020)
# TODO: Make private?
def unroll_macro_list(individual: Individual, section_name: str, frame_path: Sequence[Frame] = None) \
        -> List[Tuple[Macro, Tuple[Frame]]]:
    # TODO: Double Check
    """Generate a list of (macro, frame_path) from a given section (=section_name).

    Args:
        individual (Individual): individual that contains the Constraints and the frame_tree.
        section_name (str): name of the section from which to take the macro.
        frame_path (Sequence[Frame]): frame path of the section.

    Returns:
        List of all {Macro, Frame} of the selected section.
    """
    # ...from all possible sections (see __getitem__ in Constraints class)
    section = individual.constraints[section_name]
    if frame_path is None:
        # Take the first frame of the tree
        frame_path = [individual.frame_tree.root.frame]
    frame_path = tuple(frame_path) + (Frame(individual.get_unique_frame_name(section), section),)

    nodes = list()
    if isinstance(section, MacroPool):
        # if section.size[0] == section.size[1]:
        #     x = range(section.size[0])
        # else:
        #     x = range(rnd.randint(section.size[0], section.size[1]))
        # for _ in x:
        for i in range(random_generator.randint(*section.size)):
            # Create and append a node that contains of the macros in the list of macros
            #       (returned by section.macro_pool method)
            chosen_macro = random_generator.choice(section.macro_pool)
            # logging.bare(chosen_macro)
            nodes.append((chosen_macro, frame_path))
    elif isinstance(section, SubsectionsSequence):
        # For each section in the SubsectionSequence...
        for seq in section.sub_sections:
            nodes += unroll_macro_list(individual, seq.name, frame_path)
    elif isinstance(section, SubsectionsAlternative):
        seq = random_generator.choice(section.sub_sections)
        nodes += unroll_macro_list(individual, seq.name, frame_path)
    else:
        raise TypeError("Unknown section type")
    return nodes


# TODO: Check. Urgent. (fall 2020)
# TODO: Refactor. Move to population?
def order_by_fitness(individuals_pool: Union[Set[Individual], List[Individual]]) -> List[Individual]:
    # TODO: Double Check
    """Sort individuals based on the fitness.

    Args:
        individuals_pool (Set(Individual) or List(Individual): individuals to order by fitness.

    Returns:
        Ordered list of individuals.
    """
    individuals_pool = list(individuals_pool)
    first_fitness = individuals_pool[0].fitness
    i_f_list = [(i, i.fitness) for i in individuals_pool]
    ordered_i_f_list = first_fitness.sort(i_f_list)
    return [i for i, f in ordered_i_f_list]


# INITIALIZATION________________________________________________________________________________________________________
# TODO: Separate the 'create_random_individual -> Individual' from an 'init_random_individual -> [Individual]'
# TODO: Check. Urgent. (fall 2020)
def create_random_individual(constraints: Constraints, max_retries: Optional[int] = 100, **kwargs) -> \
        List[Optional[Individual]]:
    # TODO: Double Check
    """Creates a random individual.

    Individuals are created starting from section `main`. The new individual is
    eventually checked using `is_valid`. If invalid it is discarded and the
    generation process starts over. The function eventually gives up after a
    number of tries and rises an exception.

    Args:
        constraints (Constraints): the constraints to be used for generating the individual
        max_retries (int): maximum number of attempts before giving up and return None

    Raise:
        RuntimeError: if the function has not been able to generate a valid individual

    Returns:
        A list with a valid MicroGP Individual or None
    """
    assert isinstance(constraints, Constraints), \
        "constraints should be of type Constraints, found %s" % (type(constraints),)

    is_valid = False
    tries = 0
    # Loop until the individual is valid or you tried enough
    while not is_valid and (max_retries is None or tries < max_retries):
        # Generate a warning
        constraints.stats['random_individuals'] += 1
        if (1 + constraints.stats['valid_individuals']) / constraints.stats['random_individuals'] \
                < constraints.stats['valid_individuals_warn_threshold']:
            num = constraints.stats['valid_individuals_warn_threshold']
            WARN_EFFORT = f"{tries:,} failed attempts to create a random individual (success rate < {num:0.3g})"
            warnings.warn(WARN_EFFORT, RuntimeWarning)
            constraints.stats['valid_individuals_warn_threshold'] /= 10
        tries += 1

        # Create empty individual with library constraints
        individual = Individual(constraints)

        # Get the list of all possible nodes -> list of tuples(node, frame_path)
        nodes = unroll_macro_list(individual, 'main')

        # Take each macro of all nodes and add it in the node set of the individual
        parent = None
        for macro, frame_path in nodes:
            parent = individual.add_node(parent_node=parent, macro=macro, frame_path=frame_path)

        individual.parents = list()
        individual.operator = create_random_individual
        individual.randomize_macros()
        individual.finalize()
        is_valid = individual.valid

    if not is_valid:
        logging.warning(f"create_random_individual: Unable to create a valid random individual in {tries} attempts")
        return [None]
    else:
        constraints.stats['valid_individuals'] += 1
        return [individual]


# CROSSOVERS____________________________________________________________________________________________________________
# TODO: Rewrite!
# TODO: Check. Urgent. (fall 2020)
def switch_proc_crossover(parentA: Individual, parentB: Individual, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """Let's consider a sequence of nodes connected through edges with label=
    'next', we will call this sequence `next-chain`. This operator selects
    the `next-chains` belonging to the common sections between the two parents
    (excluding the `main` section) and link a random node with
    ExternalReference parameter in it, to the selected `next-chain` after
    copying it from the source to the destination individual.
    The word 'proc' in method name refers to the `next-chains` that are not
    'main' sections. The destination individual is a copy of a parent chosen
    randomly and then modified with the new cloned `next-chain`.

    Args:
        parentA (Individual): First individual
        parentB (Individual): Second individual

    Returns:
        A list with the new individual or None if it is not valid
    """
    assert all([parentA, parentB]), f"Arity of switch_proc_crossover is 2"

    # Select the primary parent that will give to the son the greatest number of genes (nodes and their parameters)_____
    primary_parent = random_generator.choice([parentA, parentB])
    source_individual = parentA if primary_parent == parentB else parentB
    # Copy all the genes from the primary parent and set internal creation characteristics______________________________
    individual = clone_individual(primary_parent)
    individual.parents = {parentA, parentB}
    individual.operator = switch_proc_crossover

    root_frames_in_primary_parent = set(
        f.frame for f in primary_parent.frame_tree.root.children if f.frame.section.name != 'main')
    root_sections_frames_in_primary_parent = set((f.section, f) for f in root_frames_in_primary_parent)
    root_frames_in_source_individual = set(
        f.frame for f in source_individual.frame_tree.root.children if f.frame.section.name != 'main')
    root_sections_frames_in_source_individual = set((f.section, f) for f in root_frames_in_source_individual)
    candidates = list()
    for section_frame_source_individual in root_sections_frames_in_source_individual:
        if section_frame_source_individual[0] in set(t2[0] for t2 in root_sections_frames_in_primary_parent):
            candidates.append(section_frame_source_individual)

    if not candidates:
        return [None]

    chosen_section, chosen_frame = random_generator.choice(candidates)

    from .parameter import ExternalReference

    candidates = list()
    for node_id, parameters in individual.nodes(data='parameters').items():
        candidates = candidates + [(node_id, p) for p in parameters if isinstance(parameters[p], ExternalReference)]

    chosen_node_id, chosen_parameter_name = random_generator.choice(candidates)
    # Copy the structure of the selected frame and its parameters___________________________________________________
    nodes_to_copy_from = source_individual.nodes(frame_selector=chosen_frame)
    assert len(nodes_to_copy_from) > 0, "No nodes to copy from"

    # Create movable nodes of the selected proc
    first_movable_node = individual.create_movable_nodes(source_individual, nodes_to_copy_from, is_new_proc=True)
    assert first_movable_node, "Ops, something went wrong in creation of movable nodes"

    individual.arrange_movable_proc(nodes_to_copy_from, source_individual, first_movable_node)

    # Change the destination of the external reference of the selected node_____________________________________________
    original_node = individual.nodes[chosen_node_id]
    from microgp.parameter import ExternalReference
    for parameter_name, parameter in original_node['parameters'].items():
        if parameter.name == chosen_parameter_name and isinstance(parameter, ExternalReference):
            parameter.value = first_movable_node

    individual.finalize()
    is_valid = individual.valid
    individual = None if not is_valid else individual
    # if is_valid:
    #     print_individual(primary_parent, 'switch_proc crossover: primary parent', plot=True)
    #     print_individual(source_individual, 'switch_proc crossover: source individual', plot=True)
    #     print_individual(individual, 'switch_proc crossover: individual', plot=True)
    return [individual]

# TODO: Check. Urgent. (fall 2020)
def macro_pool_one_cut_point_crossover(parentA: Individual, parentB: Individual,
                                       **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """This crossover builds two lists of MacroPools in parentA and parentB
    belonging to common sections, chooses one element for each list and
    chooses one node (called cut_node). parentA and parentB are cloned and
    subsequently modified (in individualC, individualD); each individual will
    have the chosen MacroPool with an half copied from the other individual.

    **Examples**:

    - parentA has a MacroPool with nodes: [A, B, C, D, E]

    - parentB has a MacroPool with nodes: [F, G, H, I, L]

    - the chosen cut_node are B and G

    - individualC will have a MacroPool with nodes: [A, B, H, I, L]

    - individualD will have a MacroPool with nodes: [F, G, C, D, E]

    If the chosen MacroPools has a different number of nodes, then two cut
    point will be chosen:

    **Examples**:

    - parentA has a MacroPool with nodes: [A, B, C, D, E, F, G]

    - parentB has a MacroPool with nodes: [H, I, L]

    - the chosen cut_node are F and H

    - individualC will have a MacroPool with nodes: [A, B, C, D, E, F, I, L]

    - individualD will have a MacroPool with nodes: [H, G]

    Args:
        parentA (Individual): First individual
        parentB (Individual): Second individual

    Returns:
        A list with the new individuals or None if it is not valid
    """
    assert all([parentA, parentB]), f"Arity of macro_pool_one_cut_point_crossover is 2"

    assert all(parentA.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"
    assert all(parentB.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"

    # Copy all the genes from the primary parent and set internal creation characteristics______________________________
    # Initialize first son (individualC)
    individualC = clone_individual(parentA)
    # TODO: Merge (operaor, (parents)) in a single field
    individualC.parents = {parentA, parentB}
    individualC.operator = macro_pool_one_cut_point_crossover
    # Initialize second son (individualD)
    individualD = clone_individual(parentB)
    individualD.parents = {parentA, parentB}
    individualD.operator = macro_pool_one_cut_point_crossover

    assert all(individualC.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"
    assert all(individualD.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"

    if parentA == parentB:
        individualC.finalize()
        individualD.finalize()
        return [individualC, individualD]

    # Manipulate sections and frames in order to choose the frame that will be copied into the son______________________
    # common_sections = get_common_sections(parentA, parentB)

    candidates = list()
    for frame_C in parentA.frame_tree.node_dict:
        if isinstance(frame_C.section, MacroPool):
            for frame_D in parentB.frame_tree.node_dict:
                if frame_C.section == frame_D.section \
                        and len(parentA.nodes(frame_selector=frame_C)) > 1 \
                        and len(parentB.nodes(frame_selector=frame_D)) > 1:
                    candidates.append((frame_C, frame_D))

    if not candidates:
        return [None, None]

    # Chose the frames that will be swapped
    chosen_frame_C, chosen_frame_D = random_generator.choice(candidates)

    nodes_in_frame_C = individualC.nodes(frame_selector=chosen_frame_C)
    nodes_in_frame_D = individualD.nodes(frame_selector=chosen_frame_D)

    # __________________________Choose the cut nodes________________________________________________________________
    # Example:
    #   nodesC = [n4_c, n5_c, n6_c, n7_c, n8_c]
    #   cut_nodeC = n6_c
    #   nodesD = [n7_d, n8_d, n9_d, n10_d, n11_d]
    #   nodesC will be = [n4_c, n5_c, n6_c, n10_d, n11_d]
    #   nodesD will be = [n7_d, n8_d, n9_d, n7_c, n8_c]
    cut_node_C = random_generator.choice(nodes_in_frame_C[:-1])
    cut_index_C = nodes_in_frame_C.index(cut_node_C)
    # If the frames have different size -> pick a new random node from the nodes in D
    if len(nodes_in_frame_C) != len(nodes_in_frame_D):
        cut_node_D = random_generator.choice(nodes_in_frame_D[:-1])
        cut_index_D = nodes_in_frame_D.index(cut_node_D)
    else:
        cut_index_D = cut_index_C
        cut_node_D = nodes_in_frame_D[cut_index_D]
    # __________________________Create movable nodes and fill parameters____________________________________________
    nodes_to_copy_from_C = nodes_in_frame_C[:cut_index_C + 1]
    nodes_to_copy_from_D = nodes_in_frame_D[cut_index_D + 1:]
    first_movable_node_C = individualC.create_movable_nodes(individualD, nodes_to_copy_from_D)
    first_movable_node_D = individualD.create_movable_nodes(individualC, nodes_to_copy_from_C)

    # ______________________________________________________________________________________________________________
    # Save the (key:)NodeID of the first node of the 'next-chain' and a tuple containing the parent, the first node
    #   outside the chosen frame and the frame path of the nodes in frame (they will be used in individualC.finalize())
    first_outside_C = individualC.get_next(nodes_in_frame_C[-1])
    first_outside_D = individualD.get_next(nodes_in_frame_D[-1])
    frame_path_C = individualC.graph_manager[cut_node_C]['frame_path']
    frame_path_D = individualD.graph_manager[cut_node_D]['frame_path']
    individualC._unlinked_nodes[first_movable_node_C] = (cut_node_C, first_outside_C, frame_path_C)
    individualD._unlinked_nodes[first_movable_node_D] = (cut_node_D, first_outside_D, frame_path_D)

    individualC.finalize()
    individualD.finalize()
    is_valid_C = individualC.valid
    is_valid_D = individualD.valid
    individualC = None if not is_valid_C else individualC
    individualD = None if not is_valid_D else individualD
    # if is_valid_C and is_valid_D:
    #     print_individual(parentA, 'parentA', plot=True)
    #     print_individual(parentB, 'parentB', plot=True)
    #     print_individual(individualC, 'individualC', plot=True)
    #     print_individual(individualD, 'individualD', plot=True)
    assert all(individualC.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"
    assert all(individualD.nodes(data='frame_path').values()), "Illegal frame_path in individual's node"

    return [individualC, individualD]

# TODO: Check. Urgent. (fall 2020)
def macro_pool_uniform_crossover(parentA: Individual, parentB: Individual, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """This crossover builds two lists of MacroPools in parentA and parentB
      belonging to common sections, chooses one element for each list.
      parentA and parentB are cloned and subsequently modified (in individualC
      , individualD); each individual will have the chosen MacroPool swapped
      with that of the other.

      **Examples**:

      - parentA has a MacroPool with nodes: [A, B, C, D, E]

      - parentB has a MacroPool with nodes: [F, G, H, I, L]

      - individualC will have a MacroPool with nodes: [F, G, C, D, E]

      - individualD will have a MacroPool with nodes: [A, B, H, I, L]

      If the chosen MacroPools has a different number of nodes:

      **Examples**:

      - parentA has a MacroPool with nodes: [A, B, C, D, E, F, G]

      - parentB has a MacroPool with nodes: [H, I, L]

      - individualC will have a MacroPool with nodes: [H, I, L]

      - individualD will have a MacroPool with nodes: [A, B, C, D, E, F, G]

      Args:
          parentA (Individual): First individual
          parentB (Individual): Second individual

      Returns:
          A list with the new individuals or None if it is not valid
      """
    assert all([parentA, parentB]), f"Arity of crossover_3 is 2, received {len(parents)} instead"

    # Copy the graph_manager structure from the parents and set internal hereditary characteristics_____________________________
    # Initialize first son (individualC) from parentA
    individualC = clone_individual(parentA)
    individualC.parents = {parentA, parentB}
    individualC.operator = macro_pool_uniform_crossover
    assert all(individualC.nodes[n]['frame_path'] for n in individualC.nodes), "Illegal frame_path in individual's node"

    # Initialize second son (individualD) from parentB
    individualD = clone_individual(parentB)
    individualD.parents = {parentA, parentB}
    individualD.operator = macro_pool_uniform_crossover
    assert all(individualD.nodes[n]['frame_path'] for n in individualD.nodes), "Illegal frame_path in individual's node"

    # If the individuals are identical -> return the copies
    if parentA == parentB:
        individualC.finalize()
        individualD.finalize()
        return [individualC, individualD]

    # Find the common frames with the same number of nodes inside
    candidates = list()
    for frame_C in parentA.frame_tree.node_dict:
        if isinstance(frame_C.section, MacroPool):
            for frame_D in parentB.frame_tree.node_dict:
                if frame_C.section == frame_D.section and \
                        len(parentA.nodes(frame_selector=frame_C)) == len(parentB.nodes(frame_selector=frame_D)):
                    candidates.append((frame_C, frame_D))

    if not candidates:
        return [None]

    # Choose the frames that will be swapped
    chosen_frame_C, chosen_frame_D = random_generator.choice(candidates)

    nodes_in_frame_C = individualC.nodes(frame_selector=chosen_frame_C)
    nodes_in_frame_D = individualD.nodes(frame_selector=chosen_frame_D)
    first_node_id_C = nodes_in_frame_C[0]
    first_node_id_D = nodes_in_frame_D[0]

    # __________________________Create movable nodes and fill parameters____________________________________________
    nodes_to_copy_from_C = nodes_in_frame_C
    nodes_to_copy_from_D = nodes_in_frame_D
    first_movable_node_C = individualC.create_movable_nodes(individualD, nodes_to_copy_from_D)
    first_movable_node_D = individualD.create_movable_nodes(individualC, nodes_to_copy_from_C)

    # ______________________________________________________________________________________________________________
    # Save the (key:)NodeID of the first node of the 'next-chain' and a tuple containing the parent, the first node
    #   outside the chosen frame and the frame path of the nodes in frame (they will be used in individualC.finalize())
    first_node_outside_C = individualC.get_next(nodes_in_frame_C[-1])
    first_node_outside_D = individualD.get_next(nodes_in_frame_D[-1])
    pred_C = individualC.get_predecessors(first_node_id_C)
    pred_D = individualD.get_predecessors(first_node_id_D)
    pred_C = pred_C[0] if pred_C else None
    pred_D = pred_D[0] if pred_D else None
    frame_path_C = individualC.graph_manager[first_node_id_C]['frame_path']
    frame_path_D = individualD.graph_manager[first_node_id_D]['frame_path']
    individualC._unlinked_nodes[first_movable_node_C] = (pred_C, first_node_outside_C, frame_path_C)
    individualD._unlinked_nodes[first_movable_node_D] = (pred_D, first_node_outside_D, frame_path_D)

    individualC.finalize()
    is_valid_C = individualC.valid
    assert individualC.valid is False or all(
        individualC.graph_manager[n]['frame_path']
        for n in individualC.graph_manager.nodes()), "Illegal frame_path in individual's node"

    individualD.finalize()
    is_valid_D = individualD.valid
    assert individualD.valid is False or all(
        individualD.graph_manager[n]['frame_path']
        for n in individualD.graph_manager.nodes()), "Illegal frame_path in individual's node"

    individualC = None if not is_valid_C else individualC
    individualD = None if not is_valid_D else individualD
    # if is_valid_C and is_valid_D:
    #     print_individual(parentA, 'parentA', plot=True)
    #     print_individual(parentB, 'parentB', plot=True)
    #     print_individual(individualC, 'individualC', plot=True)
    #     print_individual(individualD, 'individualD', plot=True)
    return [individualC, individualD]


# MUTATIONS_____________________________________________________________________________________________________________
# TODO: Check. Urgent. (fall 2020)
def check_muation_parameters(original_individual: Individual, strength: float):
    # TODO: Double Check
    assert issubclass(type(strength), float), '"strength" parameter must be a float'
    assert 0 <= strength <= 1, '"strength" parameter must be in [0, 1]'
    assert original_individual, "Original individual can't be None"
    assert isinstance(original_individual, Individual), "Original individual must be of type Individual"


# TODO: Check. Urgent. (fall 2020)
def remove_node_mutation(original_individual: Individual, strength: float, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """Try to remove a node taken from the possible set of nodes in the
    individual. The removal could fail because of the minimum number of nodes
    that the individual must contain. This method returns a modified copy of
    the passed individual leaving it unchanged.

    Args:
        original_individual (Individual): source individual to mutate
        strength (float): mutation strength

    Returns:
        A list with the new mutated individual or None if it is not valid
    """
    # logging.debug("Remove a node mutation has been chosen")
    check_muation_parameters(original_individual, strength)

    new_individual = clone_individual(original_individual)
    new_individual.parents = [original_individual]
    new_individual.operator = remove_node_mutation
    while True:
        if len(new_individual.nodes()) <= 2:
            logging.debug("Individual should have at least two nodes")
            return [None]

        frame_count = get_macro_pool_nodes_count(new_individual)
        shrinkable_frames = set()
        # Find the frames from which I can remove a node
        for chosen_frame, count in frame_count.items():
            if chosen_frame.section.size[0] <= count - 1:
                shrinkable_frames.add(chosen_frame)
        # If there are not shrinkable frames return (operator fails)
        if len(shrinkable_frames) == 0:
            return [None]
        # Otherwise -> removal of a node is always executed

        # Choice a valid frame
        chosen_frame = random_generator.choice(list(shrinkable_frames))

        # Choose randomly the node that will be removed
        candidate_nodes = get_nodes_in_section(individual=new_individual, section=chosen_frame[1])
        node_to_remove = random_generator.choice(candidate_nodes)
        chosen_root_frame = new_individual.nodes[node_to_remove]['frame_path'][1]

        new_individual.remove_node(node_to_remove)
        assert node_to_remove not in new_individual.nodes(), "Node has not been removed"

        # Example: If the removed NodeID_2 was a destination of a Reference in NodeID_1 and NodeID_6 -> change the value
        #  in parameter of the NodeID_1 and NodeID_6 with a new possible target (mutate(1))
        from .parameter import LocalReference
        for node in new_individual.nodes(frame_selector=chosen_root_frame):
            for parameter_name, parameter in new_individual.nodes[node]['parameters'].items():
                if isinstance(parameter, LocalReference) and parameter.value == node_to_remove:
                    parameter.mutate(1)

        if strength == 1.0 or not (random_generator.random() < strength):
            break

    assert len(original_individual.nodes()) > len(
        new_individual.nodes()), "Something wrong!"
    new_individual.finalize()
    if not new_individual.valid:
        return [None]
    else:
        # print_individual(original_individual, 'Original individual', True)
        # print_individual(individual, 'Mutated individual', True)
        return [new_individual]


# TODO: Check. Urgent. (fall 2020)
def add_node_mutation(original_individual: Individual, strength: float, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """Insert a new node in the individual graph_manager. An insertion of a new node
    could fail because of there are no valid targets for the node that
    contains a LocalReference.

    Args:
        original_individual (Individual): source individual to mutate
        strength (float): mutation strength

    Returns:
        A list with the new mutated individual or None if it is not valid
    """
    # logging.debug("Insert a new node mutation has been chosen")
    check_muation_parameters(original_individual, strength)

    new_individual = clone_individual(original_individual)
    new_individual.parents = {original_individual}
    new_individual.operator = add_node_mutation

    while True:
        frame_count = get_macro_pool_nodes_count(new_individual)
        expandable_frames = set()
        # Find the frames in which I can place a new node
        for frame in frame_count:
            if frame.section.size[1] >= frame_count[frame] + 1:
                expandable_frames.add(frame)
        # If there are not expandable frames return (operator fails)
        if len(expandable_frames) == 0:
            return [None]

        # Choice a valid frame
        chosen_frame = random_generator.choice(list(expandable_frames))

        # Choose randomly a node that will be the parent of the new node
        candidate_nodes = get_nodes_in_section(individual=new_individual, section=chosen_frame[1])
        chosen_parent_node = random_generator.choice(candidate_nodes)

        frame_path = new_individual.graph_manager[chosen_parent_node]['frame_path']
        candidate_macros = chosen_frame.section.macro_pool
        chosen_macro = random_generator.choice(candidate_macros)

        # Add node to graph_manager
        node_to_insert = new_individual.add_node(parent_node=chosen_parent_node,
                                                 macro=chosen_macro,
                                                 frame_path=frame_path)

        # Initialize parameters of the inserted node
        new_individual.initialize_macros(chosen_macro, node_to_insert)

        assert node_to_insert in new_individual.graph_manager.nodes(), "Node has not been inserted"

        if strength == 1.0 or not (random_generator.random() < strength):
            break

    assert len(original_individual.graph_manager.nodes()) < len(
        new_individual.graph_manager.nodes()), "Something wrong!"
    new_individual.finalize()
    if not new_individual.valid:
        return [None]
    else:
        # print_individual(individual, 'Mutated individual', True)
        # print_individual(original_individual, 'Original individual', True)
        return [new_individual]


# TODO: Check. Urgent. (fall 2020)
def hierarchical_mutation(original_individual: Individual, strength: float, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """Choose a node in the graph_manager, choose a parameter inside the node, mutate it.
    Each parameter has probability: `1/len(nodes) * 1/len(parameters in that node)`.

    Args:
        original_individual (Individual): source individual to mutate
        strength (float): mutation strength

    Returns:
        A list with the new mutated individual or None if it is not valid
    """
    check_muation_parameters(original_individual, strength)

    new_individual = clone_individual(original_individual)
    new_individual.parents = {original_individual}
    new_individual.operator = hierarchical_mutation

    # Do while not (rnd.random() < strength)
    while True:
        # Use "while loop" to try choosing a node that doesn't contain only the Information parameter or the mutation
        #   had no effect
        while True:
            # Choose a node that contains the parameter to mutate
            chosen_node = random_generator.choice(new_individual.nodes())

            # Create a list of parameters contained into the macro
            candidate_parameters = list()
            for parameter_name, parameter in new_individual.nodes[chosen_node]['parameters'].items():
                if not isinstance(parameter, Information):
                    candidate_parameters.append(parameter)

            # If I tried to mutate a macro that contains only an Information parameter -> pick another node to mutate
            #   else -> mutate a random parameter
            if candidate_parameters:
                # Choose only one parameter to mutate in the list of all parameters of the chosen macro
                chosen_parameter = random_generator.choice(candidate_parameters)
                assert strength
                chosen_parameter.mutate(strength)
                break

        # Stop condition
        if strength == 1.0 or not (random_generator.random() < strength):
            break

    new_individual.finalize()
    if not new_individual.valid:
        return [None]
    else:
        # print_individual(original_individual, 'ORIGINAL', True)
        # print_individual(individual, 'MUTATED', True)
        return [new_individual]


# TODO: Check. Urgent. (fall 2020)
def flat_mutation(original_individual: Individual, strength: float, **kwargs) -> List[Optional[Individual]]:
    # TODO: Double Check
    """Build a list of all parameters contained in all nodes then choose one
    of them and mutate it. Each parameter has probability: `1/len(nodes)`.

    Args:
        original_individual (Individual): source individual to mutate
        strength (float): mutation strength

    Returns:
        A list with the new mutated individual or None if it is not valid
    """
    # logging.debug("Flat mutation has been chosen")
    check_muation_parameters(original_individual, strength)

    new_individual = clone_individual(original_individual)
    new_individual.parents = {original_individual}
    new_individual.operator = flat_mutation

    while True:
        # Create a list that contains all parameters
        candidate_parameters = list()
        # Iterate for each node in the individual and save a list of parameters
        for node in new_individual.nodes():
            for parameter_name in sorted(new_individual.nodes[node]['parameters']):
                # node parameters need to be in predictable order!
                parameter = new_individual.nodes[node]['parameters'][parameter_name]
                if not isinstance(parameter, Information):
                    candidate_parameters.append(parameter)

        # If the individual contains only Information parameters flat_mutate returns [None]
        if not candidate_parameters:
            return [None]

        # Choose and mutate a parameter
        chosen_parameter = random_generator.choice(candidate_parameters)
        chosen_parameter.mutate(strength)

        # Stop condition
        if strength == 1.0 or not (random_generator.random() < strength):
            break

    new_individual.finalize()
    if not new_individual.valid:
        return [None]
    else:
        # print_individual(original_individual, 'ORIGINAL', True)
        # print_individual(individual, 'MUTATED', True)
        return [new_individual]
