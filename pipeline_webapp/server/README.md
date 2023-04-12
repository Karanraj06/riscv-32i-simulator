# **Pipelined Processor**

The simulator flow follows a piplined processor design. This design divides processor into a set of 5 stages namely FETCH(IF), DECODE(DE), EXECUTE(EX), MEMORY ACCESS(MA) and WRITEBACK(WB), where the stages are ordered one after the other,and simultaneously process a set of instructions by assigning an instruction to each stage. 

## **Additions to Single-Cycle Design**

The implementation of pipelined processor includes the following things in addition to single cycle processor design:-

- Implemented pipelined registers (IF-DE, DE-EX, EX-MA and MA-WB).
- Input knob to enable/disable forwarding. 
- Handling of data and control hazards by taking appropriate data forwarding paths and using branch-table-buffer (BTB) respectively.
- Use of 1-bit branch prediction logic for creation of branch-table-buffer. 
- Implemented data-lock unit for stalling registers and flushing pipeline registers.
- Data forwarding along with highlighting the forwarding path taken.

## **Input**

The input format is same as of single cycle processor design. The processor requires machine code as an input text file in the editor section.

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

## **Implementation Details**

### *Simulator Flow*

There are separate file for each of the 5 major units - FETCH, DECODE, EXECUTE, MEMORY ACCESS and WRITEBACK.

Following is the recursive approach which is used in the pipeline implementation

>In the first cycle, only instruction_fetch is invoked. In the second sycle, decode is invoked which in turn calls instruction_fetch. Similarly, each stage calls its previous stage in order. In the third and fourth cycle, execute and memory_access are invoked. From the fifth cycle, writeback is only invoked. This ensures that in every clock cycle, each instruction moves ahead by one step. 
```
Cycle   Function calls
 1       IF
 2       DE => IF
 3       EX => DE => IF 
 4       MA => EX => DE => IF 
 5       WB => MA => EX => DE => IF 
 6       WB => MA => EX => DE => IF
 7       WB => MA => EX => DE => IF
 ...        ...
 ...        ...

```

### *Pipeline Registers*

There are separate file for each of the 4 pipeline registers - IF-DE, DE-EX, EX-MA and MA-WB. 

Each of the above pipeline registers contains the content of the previous pipeline register as well as the data generated in the previous stage in the form of instruction packet. This includes the instruction, the operands, immediates, control signals generated in decode stage, aluResult and loadData varaibles. The pipeline stages use this data from the pipeline registers. Additionally, they contain a **nop** variable which can be used to indicate if a bubble is present or not.

### *Forwarding* 

Forwarding is a method which allows processor to transfer values of operands between instructions in different pipeline stages through direct connections between the stages. In each stage, it is checked if it's **rs1** or **rs2** is matching with the **rd** of any of the previous instruction. In this way, read after write (RAW) hazards are handled using forwarding.

If forwarding is disabled, checking for data hazards is done in the decode stage itself. If there are any dependencies, data lock unit is used to stall the pipeline till the writeback stage is completed.

### *Data Lock Unit*
This unit is used to introduce stalls/bubbles in the pipeline in order to avoid data and control dependencies. In control hazards, if there is a need to take a branch, then data lock unit flushes the IF-DE stage. 

### *Branch Prediction*

Branch-table-buffer uses 1-bit branch prediction logic to reduce control hazards and improve the efficiency of pipeline processor. 

The structure of BTB table is given below:-  

| PC            | BranchTargetAddress | Branch Taken/Not Taken |
|    :---       |     :---:     |     :---:     |     
|   0x4  | 0x10  | Taken  |
|   0x8  | 0x16  | Not Taken  |
|   0xc  | 0x24  | Not Taken  |

The instruction fetch stage checks if the current pc is present in the branch table buffer. If it is, and the branch was taken during the previous execution, we will set the pc to the corresponding branch target address. The execute stage
computes the actual next pc, and if it matches with the output of the branch table buffer,we can proceed without any stalls. Otherwise, two bubbles will be introduced in the pipeline.
>
    Accuracy = ( n - 2 ) / n, where n is the number of branching instructions