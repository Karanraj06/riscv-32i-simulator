# ============ IsBranch: 0 -> pc + 4, 1 -> BranchTargetAddress, 2 -> ALUResult ==============
import decode as de
import instruction_fetch as fi
# ===========GLOBAL VARIABLES===============
aluResult: int = None
isBranch: int = None

def srl(a:int,b:int)->int:
    if(a>=0):
        return a>>b
    else:
        return (a+0x100000000)>>b

def execute() -> int:
    global aluResult, isBranch
    op1:int = de.op1
    op2: int = None
    # Selecting op2
    if (de.OP2Select == 0):
        op2 = de.op2
    elif (de.OP2Select == 1):
        op2 = de.imm
    elif (de.OP2Select == 2):
        op2 = de.immS
    # opening file to write output
    f = open("output.txt", "a")
    if (de.ALUOperation == 0):
        aluResult = op1+op2
        f.write(f"EXECUTE:ADD {op1} and {op2}\n")
    elif (de.ALUOperation == 1):
        aluResult = op1-op2
        f.write(f"EXECUTE:SUB {op1} and {op2}\n")
    elif (de.ALUOperation == 2):
        aluResult = op1 ^ op2
        f.write(f"EXECUTE:XOR {op1} and {op2}\n")
    elif (de.ALUOperation == 3):
        aluResult = op1 | op2
        f.write(f"EXECUTE:OR {op1} and {op2}\n")
    elif (de.ALUOperation == 4):
        aluResult = op1 & op2
        f.write(f"EXECUTE:AND {op1} and {op2}\n")
    elif (de.ALUOperation == 5):
        aluResult = op1 << op2
        f.write(f"EXECUTE:SLL {op1} and {op2}\n")
    elif (de.ALUOperation == 6):
        aluResult=srl(op1,op2)
        f.write(f"EXECUTE:SRL {op1} and {op2}\n")
    elif (de.ALUOperation == 7):
        aluResult = op1 >> op2
        f.write(f"EXECUTE:SRA {op1} and {op2}\n")
    elif (de.ALUOperation == 8):
        if (op1 == op2):
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            f.write(f"EXECUTE:BEQ PC set to {de.BranchTargetAddress}\n")
        else:
            isBranch = 0
    elif (de.ALUOperation == 9):
        if (op1 != op2):
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            f.write(f"EXECUTE:BNE PC set to {de.BranchTargetAddress}\n")
        else:
            isBranch = 0
    elif (de.ALUOperation == 10):
        if (op1 >= op2):
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            f.write(f"EXECUTE:BGE PC set to {de.BranchTargetAddress}\n")
        else:
            isBranch = 0
    elif (de.ALUOperation == 11):
        if (op1 < op2):
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            f.write(f"EXECUTE:BLT PC set to {de.BranchTargetAddress}\n")
        else:
            isBranch = 0
    # for JAL
    if (de.opcode == '1101111'):
        fi.pc = de.BranchTargetAddress
        f.write(f"EXECUTE: PC set to {de.BranchTargetAddress}\n")
    elif (de.opcode == '1100111'):  # for JALR
        fi.pc = aluResult
        f.write(f"EXECUTE: PC set to {de.BranchTargetAddress}\n")
    f.close()
    print(aluResult)


def init() -> None:
    '''Initializes all global variables to their initial value'''
    global aluResult, isBranch
    aluResult = None
    isBranch = None
