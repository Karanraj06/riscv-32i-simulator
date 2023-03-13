# **RISCV-32I-Simulator**

Functional Simulator for subset of RISC-V Instruction set. The simulator reads encoded instructions from a memory file (machine code), decodes, executes, and writes back the results to a register file.


## *Summary*

The project has two components: a command-line interface (CLI) and a web-based graphical user interface (GUI) built with Flask and Tailwind.
> Command Line interface is elaborated in detail at: https://github.com/Karanraj06/RISCV-32I-Simulator/blob/main/single_cycle/README.md

> The webapp is active at the following URL: http://karanraj.pythonanywhere.com/


## *Directory Structure*

```bash

|---docs
|        |---reference.docx
|
|---single_cycle
|
|---single_cycle_webapp
|   
|---test
    |---array_sum.mc
    |---array_sum.s
    |---bubble_sort.mc
    |---bubble_sort.s
    |---fibonacci.mc
    |---fibonacci.s

```
## *Instructions Supported*

```
R format - add, and, or, sll, slt, sra, srl, sub, xor
I format - addi, andi, ori, lb, lh, lw, jalr
S format - sb, sw, sh
SB format - beq, bne, bge, blt
U format - auipc, lui
J format - jal
```

## *Contributors* 
```bash
Atharva Mulay :- 2021CSB1076
Karanraj Mehta:- 2021CSB1100
Nishad Dhuri  :- 2021CSB1116
Sumit Patil   :- 2021CSB1135
```




