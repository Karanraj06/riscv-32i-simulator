# Bubble Sort Algorithm in RISCV-32I Assembly Language
# Sorts an array of random numbers using bubble sort, and stores the sorted array
jal x0, main

# Generates a pseudo random number using a seed value
random:
    add t3, x0, x4    # t3 = x4 = seed
    slli t4, t3, 21    # t4 = t3 << 21
    xor t3, t3, t4    # t3 ^= t4
    addi t5, x0, 23    # t5 = 23
    srl t4, t3, t5    # t4 = t3 >> t5
    xor t3, t3, t4    # t3 ^= t4
    add x4, x0, t3    # x4 = seed = t3
    add a0, x0, t3    # a0 = t3
    ret    # return

# Implements the bubble sort algorithm
bubbleSort:
    add t0, x0, x0    # t0 = loop 2 counter = 0

    # Start of loop2
    loop2:
        beq t0, x3, end2    # if t0 == x3, goto end2
        add t1, x0, x0    # t1 = loop 3 counter = 0

        # Start of loop3
        loop3:
            addi t2, t0, 1    # t2 = t0 + 1
            sub t2, x3, t2    # t2 = x3 - t2
            beq t1, t2, end3    # if t1 == t2, goto loop2

            addi t2, t1, 1    # t2 = t1 + 1
            slli t2, t2, 2    # t2 <<= 2 OR t2 *= 4
            add t2, t2, s1    # t2 += s1
            lw t3, 0(t2)    # t3 = M[t2] OR t3 = sortedArray[t1 + 1]
            slli t4, t1, 2    # t4 = t1 << 2 OR t4 = t1 * 4
            add t4, t4, s1    # t4 += s1
            lw t5, 0(t4)    # t5 = M[t4] OR t5 = sortedArray[t1]
            ble t5, t3, label    # if t5 <= t3, goto label

            # Swap
            sw t3, 0(t4)    # Store t3 in the address pointed to by t4
            sw t5, 0(t2)    # Store t5 in the address pointed to by t2

            # Continue to label
            label:
                addi t1, t1, 1    # t1++
                beq x0, x0, loop3    # Continue to loop3

        end3:
            addi t0, t0, 1    # t0++
            beq x0, x0, loop2

    end2:
    ret    # return

main:
    addi x3, x0, 10    # x3 = n = 10
    lui x4, 0x10000    # x4 = seed = 0x10000000
    lui s0, 0x10001    # s0 = array = 0x10001000
    lui s1, 0x10002    # s1 = sortedArray = 0x10002000

    add t0, x0, x0    # t0 = loop 1 counter = 0
    add t1, x0, s0    # t1 = s0
    add t2, x0, s1    # t2 = s1

    loop1:
        beq t0, x3, end1    # if t0 == x3, goto end1
        jal x1, random    # Call random

        # Store the generated random number in the arrays
        sw a0, 0(t1)
        sw a0, 0(t2)

        # Updation
        addi t0, t0, 1
        addi t1, t1, 4
        addi t2, t2, 4
        beq x0, x0, loop1

    end1:
    jal x1, bubbleSort