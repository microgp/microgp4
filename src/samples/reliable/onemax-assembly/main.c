/*-**********************************************************************-*\
*             * CLASS SAMPLE FOR "COMPUTER SCIENCES" (04JCJ**)             *
*   #####     * (!) 2020, Giovanni Squillero <squillero@polito.it>         *
*  ######     *                                                            *
*  ###   \    * Copying and distributing this file, either with or without *
*   ##G  c\   * modification, is permitted in any medium without royalty,  *
*   #     _\  * provided that this 10-line comment is preserved.           *
*   |  _/     *                                                            *
*             * ===> THIS FILE IS OFFERED AS-IS, WITHOUT ANY WARRANTY <=== *
\*-**********************************************************************-*/

#include <stdio.h>
#include <stdlib.h>

int darwin();

int main(int argc, char *argv[])
{
    unsigned int x = darwin();

    int n = 0;
    while(x) {
        n += x & 0x1;
        x >>= 1;
    }
    printf("%d\n", n);
    return EXIT_SUCCESS;
}
Fitness score: Lexicographic(32)

    .file   "solution.c"
    .text
    .globl  _darwin
    .def    _darwin;        .scl    2;      .type   32;     .endef
_darwin:
LFB17:
    .cfi_startproc
    pushl   %ebp
    .cfi_def_cfa_offset 8
    .cfi_offset 5, -8
    movl    %esp, %ebp
    .cfi_def_cfa_register 5

    movl	$-3275, %eax
    movl	$32766, %ebx
    movl	$-22022, %ecx
    movl	$-1926, %edx

    cmp %edx, %edx
    xor %ebx, %edx
    shl $245, %ebx
    or %eax, %ecx
    shl $139, %edx
    or %ecx, %eax
    or %eax, %ebx
    jne n16
    shl $86, %edx
    shr $185, %eax
    shr $222, %ebx
    cmp %eax, %eax
    shl $43, %ebx
n16:
    jmp n22
    xor %ebx, %ebx
    cmp %eax, %ebx
    add %ecx, %edx
    shl $32, %ebx
    shl $234, %ecx
n22:
    jz n23
n23:
    shl $170, %ebx
    or %ebx, %eax
    movl	%eax, -4(%ebp)
    movl	-4(%ebp), %eax
    leave
    .cfi_restore 5
    .cfi_def_cfa 4, 4
    ret
    .cfi_endproc
LFE17:
   .ident  "GCC: (MinGW.org GCC-8.2.0-5) 8.2.0"