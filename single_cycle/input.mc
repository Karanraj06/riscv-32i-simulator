0x0	0x000000B3
0x4	0x00100113
0x8	0x00A00193
0xC	0x00200213
0x10 0x00019463
0x14 0x00008133
0x18 0x0041CC63
0x1C 0x002082B3
0x20 0x000100B3
0x24 0x00028133
0x28 0x00120213
0x2C 0xFE0006E3
0x30 _


==================== Debugging Information ====================


# nth Fibonacci number of the Fibonacci sequence in RISCV-32I Assembly Language
add x1, x0, x0    # x1 = 0
addi x2, x0, 1    # x2 = 1
addi x3, x0, 10    # x3 = n
addi x4, x0, 2    # x4 = 2
bne x3, x0, loop    # if x3 != 0, goto loop
add x2, x1, x0    # x2 = x1

loop:
    bgt x4, x3, end    # if x4 > x3, goto end
    add x5, x1, x2    # x5 = x1 + x2
    add x1, x2, x0    # x1 = x2
    add x2, x5, x0    # x2 = x5
    addi x4, x4, 1    # x4++
    beq x0, x0, loop    # goto loop

end: