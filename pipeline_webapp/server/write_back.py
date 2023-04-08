from pipeline_registers import MA_WB as instpkt
from pipeline_registers import EX_MA as prev_pip
import memory_access as ma
import registers as rg

# Initialize clock to 0
clk: int = 0
total_bubbles: int = 0
total_instructions: int = 0
current_instruction: str = ""


def writeBack() -> bool:
    # store all the values in the pipeline register first
    global total_bubbles, clk, total_instructions, current_instruction
    instpkt.nop = prev_pip.nop

    instpkt.instruction = prev_pip.instruction
    if instpkt.nop == 1:
        total_bubbles += 1
        print("WB: Bubble")
        current_instruction = "WB: Bubble"
        ma.memory_access()
        return True
    if instpkt.instruction is None:
        # HALT: Program has reached the end of the instruction memory
        with open("output.txt", "a") as f:
            f.write("\nProgram execution completed successfully.")
            current_instruction = "\nProgram execution completed successfully."
        return False
    instpkt.pc = prev_pip.pc
    # print(f"In writeback for pc= {instpkt.pc}")

    instpkt.rs1 = prev_pip.rs1
    instpkt.rs2 = prev_pip.rs2
    instpkt.rd = prev_pip.rd
    instpkt.func3 = prev_pip.func3
    instpkt.func7 = prev_pip.func7
    instpkt.op1 = prev_pip.op1
    instpkt.op2 = prev_pip.op2
    instpkt.opcode = prev_pip.opcode

    instpkt.imm = prev_pip.imm
    instpkt.immS = prev_pip.immS
    instpkt.immU = prev_pip.immU
    instpkt.immB = prev_pip.immB
    instpkt.immJ = prev_pip.immJ

    instpkt.OP2Select = prev_pip.OP2Select
    instpkt.ALUOperation = prev_pip.ALUOperation
    instpkt.MemOp = prev_pip.MemOp
    instpkt.ResultSelect = prev_pip.ResultSelect
    instpkt.RFWrite = prev_pip.RFWrite
    instpkt.BranchTargetAddress = prev_pip.BranchTargetAddress

    instpkt.aluResult = prev_pip.aluResult
    instpkt.loadData = ma.loadData

    print(f"WB: for PC = {instpkt.pc}")
    """Writeback the result into the Register File by selecting ResultSelect accordingly."""

    # if RFWrite is 0, then there is no need to write result
    if instpkt.RFWrite == 0:
        with open("output.txt", "a") as f:
            f.write(f"WRITEBACK (pc: {hex(instpkt.pc)}):No writeback Operation\n")
            current_instruction = (
                f"WRITEBACK (pc: {hex(instpkt.pc)}):No writeback Operation\n"
            )
        clk += 1
    # if rd is set to x0, then its value can't be updated
    elif int(instpkt.rd, 2) != 0:
        # Selecting ResultSelect
        if instpkt.ResultSelect == 0:
            rg.x[int(instpkt.rd, 2)] = instpkt.aluResult
        elif instpkt.ResultSelect == 1:
            rg.x[int(instpkt.rd, 2)] = instpkt.loadData
        elif instpkt.ResultSelect == 2:
            rg.x[int(instpkt.rd, 2)] = instpkt.immU
        elif instpkt.ResultSelect == 3:
            rg.x[int(instpkt.rd, 2)] = instpkt.pc + 4
        elif instpkt.ResultSelect == 4:
            rg.x[int(instpkt.rd, 2)] = instpkt.immU + instpkt.pc
        with open("output.txt", "a") as f:
            f.write(
                f"WRITEBACK (pc: {hex(instpkt.pc)}): write {rg.x[int(instpkt.rd,2)]} to rd = x[{int(instpkt.rd, 2)}]\n"
            )
            current_instruction = f"WRITEBACK (pc: {hex(instpkt.pc)}): write {rg.x[int(instpkt.rd,2)]} to rd = x[{int(instpkt.rd, 2)}]\n"
    else:
        with open("output.txt", "a") as f:
            f.write(
                f"WRITEBACK (pc: {hex(instpkt.pc)}):Can't write to rd = x[{int(instpkt.rd, 2)}]\n"
            )
            current_instruction = f"WRITEBACK (pc: {hex(instpkt.pc)}):Can't write to rd = x[{int(instpkt.rd, 2)}]\n"
    # incrementing clock cycle by 1 after the writeback stage is completed
    clk += 1
    total_instructions += 1
    # calling memory_access
    ma.memory_access()

    return True


def init() -> None:
    """Initializes pc to its initial value"""
    global clk, current_instruction,total_bubbles,total_instructions
    # initialising clk cycle to 0
    clk = 0
    current_instruction = ""
    total_instructions=0
    total_bubbles=0
    