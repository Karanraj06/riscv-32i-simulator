# ============ IsBranch: 0 -> pc + 4, 1 -> BranchTargetAddress, 2 -> ALUResult ==============
import instruction_fetch as fi
import decode as de
import memory_access as ma

# ===========GLOBAL VARIABLES===============
aluResult: int = None
isBranch: int = None

# Displaying the current instruction in Flask app
current_instruction: str = ""


def srl(a: int, b: int) -> int:
    if a >= 0:
        return a >> b
    else:
        return (a + 0x100000000) >> b
    

def sll(a: int, b: int) -> int:
    if b >= 32:
        return 0
    else:
        a = ma.dec_to_bin(a)
        a =a [b:].ljust(32, '0')
        return de.bin_to_dec(a)


def execute() -> int:
    global aluResult, isBranch, current_instruction

    op1: int = de.op1
    op2: int = None

    # Selecting op2
    if de.OP2Select == 0:
        op2 = de.op2
    elif de.OP2Select == 1:
        op2 = de.imm
    elif de.OP2Select == 2:
        op2 = de.immS

    # opening file to write output
    # f = open("output.txt", "a")
    if de.ALUOperation == 0:
        aluResult = op1 + op2
        # f.write(f"EXECUTE:ADD {op1} and {op2}\n")
        current_instruction = f"ADD {op1} and {op2}"

    elif de.ALUOperation == 1:
        aluResult = op1 - op2
        # f.write(f"EXECUTE:SUB {op1} and {op2}\n")
        current_instruction = f"SUB {op2} from {op2}"

    elif de.ALUOperation == 2:
        aluResult = op1 ^ op2
        # f.write(f"EXECUTE:XOR {op1} and {op2}\n")
        current_instruction = f"{op1} XOR {op2}"

    elif de.ALUOperation == 3:
        aluResult = op1 | op2
        # f.write(f"EXECUTE:OR {op1} and {op2}\n")
        current_instruction = f"{op1} OR {op2}"

    elif de.ALUOperation == 4:
        aluResult = op1 & op2
        # f.write(f"EXECUTE:AND {op1} and {op2}\n")
        current_instruction = f"{op1} AND {op2}"

    elif de.ALUOperation == 5:
        # aluResult = op1 << op2
        aluResult = sll(op1, op2)
        # f.write(f"EXECUTE:SLL {op1} and {op2}\n")
        current_instruction = f"{op1} << {op2}"

    elif de.ALUOperation == 6:
        if(op2 >= 32):
            op2 = op2 % 32

        aluResult = srl(op1, op2)
        # f.write(f"EXECUTE:SRL {op1} and {op2}\n")
        current_instruction = f"{op1} >>> {op2}"

    elif de.ALUOperation == 7:
        if(op2 >= 32):
            op2 = op2 % 32
            
        aluResult = op1 >> op2
        # f.write(f"EXECUTE:SRA {op1} and {op2}\n")
        current_instruction = f"{op1} >> {op2}"

    elif de.ALUOperation == 8:
        if op1 == op2:
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            # f.write(f"EXECUTE:BEQ PC set to {de.BranchTargetAddress}\n")
            current_instruction = f"Branch taken, PC set to {de.BranchTargetAddress}"
        else:
            isBranch = 0
            current_instruction = f"Branch not taken"

    elif de.ALUOperation == 9:
        if op1 != op2:
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            # f.write(f"EXECUTE:BNE PC set to {de.BranchTargetAddress}\n")
            current_instruction = f"Branch taken, PC set to {de.BranchTargetAddress}"
        else:
            isBranch = 0
            current_instruction = f"Branch not taken"

    elif de.ALUOperation == 10:
        if op1 >= op2:
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            # f.write(f"EXECUTE:BGE PC set to {de.BranchTargetAddress}\n")
            current_instruction = f"Branch taken, PC set to {de.BranchTargetAddress}"
        else:
            isBranch = 0
            current_instruction = f"Branch not taken"

    elif de.ALUOperation == 11:
        if op1 < op2:
            isBranch = 1
            fi.pc = de.BranchTargetAddress
            # f.write(f"EXECUTE:BLT PC set to {de.BranchTargetAddress}\n")
            current_instruction = f"Branch taken, PC set to {de.BranchTargetAddress}"
        else:
            isBranch = 0
            current_instruction = f"Branch not taken"

    # for JAL
    if de.opcode == "1101111":
        fi.pc = de.BranchTargetAddress
        # f.write(f"EXECUTE: PC set to {de.BranchTargetAddress}\n")
        current_instruction = f"Branch taken, PC set to {de.BranchTargetAddress}"

    elif de.opcode == "1100111":  # for JALR
        fi.pc = aluResult
        # f.write(f"EXECUTE: PC set to {aluResult}\n")
        current_instruction = f"Branch taken, PC set to {aluResult}"
    # f.close()


def init() -> None:
    """Initializes all global variables to their initial value"""
    global aluResult, isBranch, current_instruction
    aluResult = None
    isBranch = None
    current_instruction = ""
