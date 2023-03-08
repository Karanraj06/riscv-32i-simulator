# Bubble Sort Algorithm in RISC-V Assembly Language
# Sorts an array of random numbers using bubble sort, and stores the sorted array
jal zero, main

random:
    # Generates a pseudo random number using a seed value
    add t3, zero, tp    # t3 = tp = seed
    slli t4, t3, 21    # t4 = t3 << 21
    xor t3, t3, t4    # t3 ^= t4
    addi t5, zero, 35    # t5 = 35
    srl t4, t3, t5    # t4 = t3 >> t5
    xor t3, t3, t4    # t3 ^= t4
    add tp, zero, t3    # tp = seed = t3
    add a0, zero, t3    # a0 = t3
    jalr zero, 0(ra)    # return

bubbleSort:
    # Implements the bubble sort algorithm
    add t0, zero, zero    # to = loop2 counter = 0
    # Start of loop2
    loop2:
        beq t0, gp, end2    # if t0 == gp, goto end2
        add t1, zero, zero    # t1 = loop3 counter = 0
        # Start of loop3
        loop3:
            addi t2, t0, 1    # t2 = t0 + 1
            sub t2, gp, t2    # t2 = gp - t2
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
                beq zero, zero, loop3    # Continue to loop3

        end3:
            addi t0, t0, 1    # t0++
            beq zero, zero, loop2

    end2:
    jalr zero, 0(ra)    # return

main:
    addi gp, zero, 10    # gp = N = 10
    lui tp, 0x10000    # tp = seed = 0x10000000
    lui s0, 0x10001    # s0 = array = 0x10001000
    lui s1, 0x10002    # s1 = sortedArray = 0x10002000

    add t0, zero, zero    # t0 = loop1 counter = 0
    add t1, zero, s0    # t1 = s0
    add t2, zero, s1    # t2 = s1

    loop1:
        beq t0, gp, end1    # if t0 == gp, goto end1
        jal ra, random    # Call random

        # Store the generated random number in the arrays
        sw a0, 0(t1)
        sw a0, 0(t2)

        # Updation
        addi t0, t0, 1
        addi t1, t1, 4
        addi t2, t2, 4
        beq zero, zero, loop1

    end1:
    jal ra, bubbleSort
