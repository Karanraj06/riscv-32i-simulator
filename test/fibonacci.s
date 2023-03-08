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