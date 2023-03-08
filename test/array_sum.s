#This RISCV program finds sum of n numbers in a array, and stores it in the nth index of the array.
addi s0 x0 11 #n= 11 = s0
lui s1 0x10000  #base address of the array
add t0 x0 x0 # i= t0 =0
add t1 x0 s1 #t1 = s1
initialise:
	bge t0 s0 initialiseEnd
    sw t0 0(t1)
    addi t0 t0 1
    addi t1 t1 4
    beq x0 x0 initialise
initialiseEnd:
	add t2 x0 x0 #sum = = t2 = 0
    add t0 x0 x0 	
    add t1 x0 s1
    getSum:
    	bge t0 s0 getSumEnd
        lw t3 0(t1) 
        add t2 t2 t3    #sum+=a[i]
        addi t1 t1 4
        addi t0 t0 1
        beq x0 x0 getSum
    getSumEnd:
   		sw t2 0(t1) #a[n] = sum