# Automagically generated by MicroGP v4!2.0a0.dev1 on 17-May-2023 at 15:49:45

.globl _one_max ## -- Begin function one_max
_one_max:
push %rbx
push %rcx
push %rdx
pushq %rbp
movq %rsp, %rbp
movq $0xd52a65f42922d800, %rax
movq $0xd52a65f42922d800, %rbx
movq $0xd52a65f42922d800, %rcx
movq $0xd52a65f42922d800, %rdx
addq $0, %rax

andq $0x3db0, %rbx
subq $0xa962, %rdx
orq $0xb1de, %rax
jnz n59
subq %rax, %rcx
jnz n39
orq %rdx, %rcx
subq %rax, %rcx
subq $0x8128, %rax
jz n80
jz n40
jnz n21
jnz n81
jz n26
andq $0x21bf, %rcx
subq %rax, %rbx
jz n55
n21:
subq $0x8f28, %rbx
andq $0x923c, %rbx
andq $0x249d, %rdx
subq %rdx, %rax
jz n52
n26:
jnz n75
xorq $0xea6, %rcx
subq $0x8e99, %rdx
jnz n82
subq $0xd93b, %rcx
xorq $0x2abe, %rbx
subq $0x170d, %rcx
orq %rdx, %rbx
addq %rax, %rdx
xorq $0x26fd, %rbx
jnz n80
addq %rax, %rbx
jz n52
n39:
jz n46
n40:
andq %rdx, %rcx
orq $0xc8e6, %rcx
xorq %rcx, %rax
jnz n73
jnz n82
xorq $0xc802, %rdx
n46:
addq %rbx, %rax
jnz n74
andq $0xefa6, %rax
jz n66
jnz n74
jnz n66
n52:
jnz n61
xorq %rbx, %rax
addq $0xe5a3, %rdx
n55:
andq $0x83da, %rbx
xorq $0xb7bf, %rcx
xorq %rcx, %rcx
andq $0x5167, %rax
n59:
addq %rax, %rbx
jnz n68
n61:
jz n80
jz n66
jnz n75
subq $0xa148, %rdx
jz n77
n66:
xorq $0x8912, %rdx
xorq %rax, %rdx
n68:
jz n83
subq $0xc861, %rax
subq %rax, %rdx
xorq $0xe714, %rax
jnz n78
n73:
xorq %rdx, %rdx
n74:
subq $0xd9e3, %rax
n75:
andq %rax, %rdx
jnz n77
n77:
orq $0xd387, %rax
n78:
subq %rcx, %rax
orq %rbx, %rax
n80:
addq $0xac17, %rbx
n81:
jnz n82
n82:
jz n83
n83:
subq $0xf381, %rdx

popq %rbp
pop %rdx
pop %rcx
pop %rbx
retq

