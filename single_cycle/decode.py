# =================== Incomplete! : To-do Control Signals ===================
# =================== Incomplete! : To-do ALU Operation ===================
# =================== Debugging: To-do ===================
# =================== GLOBAL VARIABLES ===================
instruction: str = None
pc: int = None
rs1: str = None
rs2: str = None
rd: str = None
func3: str = None
func7: str = None
op1: int = None
op2: int = None

# =================== IMMEDIATE VALUES ===================
imm: int = None
immS: int = None
immU: int = None
immB: int = None
immJ: int = None

OP2Select: int = None
ALUOperation: int = None
MemOp: int = None
ResultSelect: int = None
RFWrite: int = None

BranchTargetAddress: int = None


def bin_to_dec(binary: str) -> int:
    """Converts a binary string (2's complement representation) to its decimal equivalent"""
    if binary[0] == '0':
        return int(binary, 2)
    else:
        return int(binary, 2) - 2 ** len(binary)


def decode() -> None:
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress

    opcode = instruction[25:]

    # R type
    if opcode == "0110011":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        func7 = instruction[:7]
        pass

    # I type
    elif opcode == "0010011":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        imm = bin_to_dec(instruction[:12])
        pass
    # S type
    elif opcode == "0100011":
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        immS = bin_to_dec(instruction[:7] + instruction[20:25])
        pass
    # B type
    elif opcode == "1100011":
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        immB = bin_to_dec(instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0')
        pass
    # U type
    elif opcode == "0010111":
        rd = instruction[20:25]
        immU = bin_to_dec(instruction[:20] + '0' * 12)
        pass
    # J type
    elif opcode == "1101111":
        rd = instruction[20:25]
        immJ = bin_to_dec(instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0')
        pass


def init() -> None:
    """Initializes all global variables to their initial value"""
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress

    instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
