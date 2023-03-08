add x1, x0, x0    # x1 = 0
addi x2, x0, 1    # x2 = 1
addi x3, x0, 10    # x3 = n
addi x4, x0, 2    # x4 = 2
bne x3, x0, loop    # if x3 != 0, goto next
add x2, x1, x0    # x2 = x1

loop:
    bgt x4, x3, exit    # if x4 > x3, goto exit
    add x5, x1, x2    # x5 = x1 + x2
    add x1, x2, x0    # x1 = x2
    add x2, x5, x0    # x2 = x5
    addi x4, x4, 1    # x4++
    beq x0, x0, loop    # goto loop

exit: