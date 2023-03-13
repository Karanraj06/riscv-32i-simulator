# Single-Cycle Processor Design

The simulator flow follows a single-cycle processor design. During each clock cycle, the following steps are executed:


*Fetch*:
The instruction pointed by the Program Counter (PC) is fetched from the Instruction Memory.

*Decode*:
The fetched instruction is decoded to determine the operation to be performed, the operands involved, and the destination register.

*Execute*:
The ALU (Arithmetic Logic Unit) operates on the operands.

*Memory Access*:
If the instruction involves a memory operation (e.g. load/store), the memory is accessed to read/write data.

*Write Back*:
The result of the execution is written back to the destination register.

## *Usage*


### **How to Use**
In the CLI version, three options are available: run, step, and reset. The run option allows the simulator to execute all instructions until the program is complete or the exit instruction is reached. The step option allows the user to execute one instruction at a time, and the reset option resets the simulator to its initial state.

### **Input**
The CLI of the single-cycle RISC-V processor require machine code as input. 

Each line should have the following format:
>
    <address of instruction><delimiter - space><machine code of the instruction>
Example of the input format: 
>
    0x0	0x00200093
    0x4	0x00300113
    0x8	0x002081B3
    0xC	_


It is important to note that the instruction '_' is used to exit the simulator and is required as the last instruction to terminate the simulator.




### **Output**

The simulator generates output messages for each stage of execution in the output.txt file.
Once the execution of the program is complete, the simulator prints the state of the register file and memory.


For the machine instruction: **0x0 0x00A00093**, the output format would like:



>
    IF: Fetch instruction 0x00A00093 from address 0x0
    DE: I-type instruction: ADDI, rs1 = x0 = 0, imm = 10, rd = x1
    EXECUTE: ADD 0 and 10
    MEMORY:No Memory Operation
    WRITEBACK: write 10 to rd = x[1]





## *Directory Structure*

```bash
|---single_cycle
            |---input.mc
            |---output.txt
            |---main.py
            |---instruction_fetch.py
            |---decode.py
            |---execute.py
            |---memory_access.py
            |---write_back.py
            |---registers.py
            |---README.md
```
## *How To Run*

### Dependencies
>Python3 

- Clone the repository to your local machine. (**Some features may not work properly on windows**)
- Change working directory to where single_cycle is located.
- Run the following command:
> 
      python main.py




