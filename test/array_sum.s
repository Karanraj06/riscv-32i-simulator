# Sum of an array of n elements in RISCV-32I Assembly Language
# Initialize an array in the first loop with each element equal to its index
# In the second loop, find this array's sum, and store the result at a[n]
addi x1, x0, 10    # x1 = n = 10
lui x2, 0x10000    # x2 = array base address = 0x10000000
addi x3, x0, 1    # x3 = loop 1 counter = i = 1
add x4, x2, x0    # x4 = x2

addi x7, x1, 1      #x7 = x1 +1
loop1:
    bge x3, x7, end1    # if x3 >= x7, goto end1
    sw x3, 0(x4)    # M[x4] = x3 OR a[i - 1] = i
    addi x3, x3, 1    # x3++
    addi x4, x4, 4    # x4 += 4
    beq x0, x0, loop1    # goto loop1

end1:

add x3, x0, x0    # x3 = loop 2 counter = 0
add x4, x2, x0    # x4 = x2
add x5, x0, x0    # x5 = sum = 0

loop2:
    bge x3, x1, end2    # if x3 >= x1, goto end2
    lw x6, 0(x4)    # x6 = M[x4] OR x6 = a[i]
    add x5, x5, x6    # x5 += x6 OR sum += a[i]
    addi x4, x4, 4    # x4 += 4
    addi x3, x3, 1    # x3++
    beq x0, x0, loop2    # goto loop2

end2:
    sw x5, 0(x4)    # M[x4] = x5 OR a[n] = sum