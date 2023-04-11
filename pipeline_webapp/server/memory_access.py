# ==============! Incomplete SB,SH(check how it works)==========
# ===============DONE!!!CHECK if memory address exists===============
# ===============CHECK if we should store addresses as hex and not int============
import decode as de
import execute as ex
import write_back as wb
from pipeline_registers import EX_MA as instpkt
from pipeline_registers import DE_EX as prev_pip

# ========Globals=========
loadData: int = None
# Data Memory
data_memory: dict[int, str] = {}
data_transfer_instructions: int = 0
current_instruction = ""


def update_mem(address: str, value: str) -> None:
    global data_memory
    data_memory[int(address, 16)] = bin(int(value, 16))[2:].zfill(32)


def dec_to_bin(x: int) -> str:
    ret = bin(x)
    if x < 0:
        ret = ret[3:]
        ret = bin(2 ** len(ret) + 2 ** len(ret) + x)
        ret = ret[2:].rjust(32, "1")
    else:
        ret = ret[2:].zfill(32)
    return ret


def check_wb() -> None:
    # for store type
    if instpkt.opcode == "0100011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex.ma_forwarding_path+="WB-MA "
                ex.ma_dependency="Data "
                instpkt.op2 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal


def memory_access() -> None:
    #clearing all the forwarding paths from previous cycle
    ex.ex_forwarding_path=""
    ex.de_forwarding_path=""
    ex.ma_forwarding_path=""
    #clearing all dependencies
    ex.de_dependency=""
    ex.ex_dependency=""
    ex.ma_dependency=""

    # print("In MA")
    global loadData, current_instruction, data_transfer_instructions
    # store all the values in the pipeline register first
    instpkt.nop = prev_pip.nop

    instpkt.instruction = prev_pip.instruction
    if instpkt.nop == 1:
        print("MA: Bubble")
        current_instruction = "MA: Bubble"
        loadData = None
        ex.execute()
        return
    if instpkt.instruction is None:
        with open("output.txt", "a") as f:
            current_instruction = "\n\n"
            f.write("\n\n")
        return
    instpkt.pc = prev_pip.pc

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

    instpkt.aluResult = ex.aluResult
    # check for data hazards
    check_wb()
    print(f"MA: for PC = {instpkt.pc}")
    print(ex.ma_forwarding_path)

    # print(instpkt.MemOp)
    f = open("output.txt", "a")
    # f.write(f"{instpkt.MemOp} for rd={instpkt.rd} and rs1={instpkt.rs1} and rs2={instpkt.rs2}\n")
    if instpkt.MemOp == 0 or instpkt.MemOp == None:
        f.write(f"MEMORY (pc: {hex(instpkt.pc)}):No Memory Operation\n")
        current_instruction = f"MEMORY (pc: {hex(instpkt.pc)}):No Memory Operation\n"
    elif instpkt.MemOp == 1:
        data_transfer_instructions += 1
        f.write(
            f"MEMORY (pc: {hex(instpkt.pc)}): Load at address {instpkt.aluResult}\n"
        )
        current_instruction = (
            f"MEMORY (pc: {hex(instpkt.pc)}): Load at address {instpkt.aluResult}\n"
        )
        # Check if memory address exists or not
        if instpkt.aluResult not in data_memory.keys():
            data_memory[instpkt.aluResult] = "0" * 32
        if instpkt.func3 == "010":  # for LW
            loadData = de.bin_to_dec(data_memory[instpkt.aluResult])
            f.write(f"The loaded value is{loadData}")
            current_instruction = f"The loaded value is{loadData}"
        elif instpkt.func3 == "000":  # for LB
            temp = data_memory[instpkt.aluResult]
            loadData = de.bin_to_dec(temp[:8].rjust(32, temp[0]))
            f.write(f"The loaded value is{loadData}")
            current_instruction = f"The loaded value is{loadData}"
        elif instpkt.func3 == "001":  # for LH
            temp = data_memory[instpkt.aluResult]
            loadData = de.bin_to_dec(temp[:16].rjust(32, temp[0]))
            f.write(f"The loaded value is{loadData}")
            current_instruction = f"The loaded value is{loadData}"
    elif instpkt.MemOp == 2:
        data_transfer_instructions += 1
        print(f"MA:{instpkt.op2} written to memory at address:{instpkt.aluResult}")
        if instpkt.func3 == "010":  # for SW
            f.write(
                f"MEMORY (pc: {hex(instpkt.pc)}): Store {instpkt.op2} at address {instpkt.aluResult}\n"
            )
            current_instruction = f"MEMORY (pc: {hex(instpkt.pc)}): Store {instpkt.op2} at address {instpkt.aluResult}\n"
            data_memory[instpkt.aluResult] = dec_to_bin(instpkt.op2)
        elif instpkt.func3 == "000":  # for SB
            data_memory[instpkt.aluResult] = dec_to_bin(instpkt.op2)[24:].zfill(32)
            f.write(
                f"MEMORY (pc: {hex(instpkt.pc)}): Store {de.bin_to_dec(dec_to_bin(instpkt.op2)[24:].zfill(32))} at address {instpkt.aluResult}\n"
            )
            current_instruction = f"MEMORY (pc: {hex(instpkt.pc)}): Store {de.bin_to_dec(dec_to_bin(instpkt.op2)[24:].zfill(32))} at address {instpkt.aluResult}\n"
        elif instpkt.func3 == "001":  # for SH
            data_memory[instpkt.aluResult] = dec_to_bin(instpkt.op2)[16:].zfill(32)
            f.write(
                f"MEMORY (pc: {hex(instpkt.pc)}): Store {de.bin_to_dec(dec_to_bin(instpkt.op2)[16:].zfill(32))} at address {instpkt.aluResult}\n"
            )
            current_instruction = f"MEMORY (pc: {hex(instpkt.pc)}): Store {de.bin_to_dec(dec_to_bin(instpkt.op2)[16:].zfill(32))} at address {instpkt.aluResult}\n"
    f.close()
    # calling execute
    ex.execute()


def init() -> None:
    """Initialize the global variables"""
    global loadData, data_memory, current_instruction,data_transfer_instructions
    loadData = None
    data_memory = {}
    data_transfer_instructions=0
    current_instruction = ""
