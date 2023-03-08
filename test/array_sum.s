# This RISCV program finds sum of n numbers in a array, and stores it in the nth index of the array.
addi s0, x0, 10    # s0 = 10
lui s1, 0x10000    # base address of the array
addi t0, x0, 1    # i = 1
add t1, x0, s1    # t1 = s1

loop1:
	bgt t0, s0, end1
    sw t0, 0(t1)
    addi t0, t0, 1
    addi t1, t1, 4
    beq x0, x0, loop1

end1:

add t2, x0, x0    # t2 = 0
add t0, x0, x0    # i = 0
add t1, x0, s1

loop2:
    bge t0, s0, end2
    lw t3, 0(t1) 
    add t2, t2, t3    # sum += a[i]
    addi t1, t1, 4
    addi t0, t0, 1
    beq x0, x0, loop2

end2:
    sw t2 0(t1)    # a[n] = sum