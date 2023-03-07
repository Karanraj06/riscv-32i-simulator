add x1, x0, x0 # x1 = x0 + x0
addi x2, x0, 1 # x2 = x0 + 1
addi x3, x0, 10 # x3 = x0 + n
addi x4, x0, 2 # x4 = x0 + 2
bne x3, x0, loop # if x3 != x0 then next
add x2, x1, x0 # x2 = x1 + x0
loop: bgt x4, x3, exit # if x4 > x3 then exit
add x5, x1, x2 # x5 = x1 + x2
add x1, x2, x0 # x1 = x2 + x0
add x2, x5, x0 # x2 = x5 + x0
addi x4, x4, 1 # x4 = x4 + 1
beq x0, x0, loop # if x0 == x0 then loop
exit:
