import microgp4 as ugp
byte = ugp.f.integer_parameter(0, 256)
reg = ugp.f.choice_parameter(['ax', 'bx', 'cx'])
macro1 = ugp.f.macro('{reg} = {val:#x}  ; hey {reg}', reg=reg, val=byte)
macro2 = ugp.f.macro('jmp {target}', target=ugp.f.local_reference(backward=False, loop=False))
sub = ugp.f.bunch([macro1], size=(5, 11), name='xxx')
macro3 = ugp.f.macro('call {target}', target=ugp.f.global_reference('xxx'))
prog = ugp.f.bunch([macro1, macro2, macro3], size=20)
pop = ugp.classes.Population(prog, None)
pop.add_random_individual()
pop.individuals[0]