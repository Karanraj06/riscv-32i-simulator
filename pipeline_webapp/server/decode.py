from pipeline_registers import IF_DE as instpkt
import instruction_fetch as fi
import registers as rg
import write_back as wb
import memory_access as ma
import execute as ex
import knobs

# Changed AluOperation for JAL
# Changed branchtargetadress in JAL
# Changed resultselect in LW to 1
# Added immU to the list of globals in decode()
# changed immediate in slli
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
opcode: str = None
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

nop: int = None
stall_count: int = 0


current_instruction = ""


def check_wb() -> None:
    global stall_count
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, immU, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress, nop

    global opcode
    # for R type
    if opcode == "0110011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for I type
    elif opcode == "0010011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                print(rs1)
                print("Error here!!")
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for Load type
    elif opcode == "0000011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for store type
    elif opcode == "0100011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for Branch type
    elif opcode == "1100011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                op2 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for JALR
    elif opcode == "1100111":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.aluResult
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.loadData
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                op1 = wb.instpkt.immU + wb.instpkt.pc
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if rs1 == wb.instpkt.rd and int(rs1, 2) != 0:
                op1 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
            if rs2 == wb.instpkt.rd and int(rs2, 2) != 0:
                op2 = wb.instpkt.pc + 4
                stall_count = 2
                if knobs.data_forwarding == 0:
                    ex.data_hazard_stalls += 1
                    ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal


def check_ma() -> None:
    global stall_count
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, immU, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress, nop

    global opcode
    # for R type
    if opcode == "0110011":
        # R type inst in WB
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in WB
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for I type
    elif opcode == "0010011":
        # R type inst in WB
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in WB
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for Load type
    elif opcode == "0000011":
        # R type inst in WB
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in WB
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for store type
    elif opcode == "0100011":
        # R type inst in WB
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in ma
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in ma
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in ma
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
    # for Branch type
    elif opcode == "1100011":
        # R type inst in ma
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in ma
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in ma
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in ma
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
            if rs2 == ma.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for JALR
    elif opcode == "1100111":
        # R type inst in ma
        if ma.instpkt.opcode == "0110011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # I type inst in ma
        if ma.instpkt.opcode == "0010011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # Load instruction in ma
        if ma.instpkt.opcode == "0000011":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # U type instruction in ma
        # LUI
        if ma.instpkt.opcode == "0110111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if rs1 == ma.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 3
                ex.data_hazard_stalls += 2
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal


def check_ex() -> None:
    global stall_count
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, immU, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress, nop

    global opcode
    # for R type
    if opcode == "0110011":
        # R type inst in WB
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in WB
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for I type
    elif opcode == "0010011":
        # R type inst in WB
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in WB
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for Load type
    elif opcode == "0000011":
        # R type inst in WB
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in WB
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in WB
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in WB
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for store type
    elif opcode == "0100011":
        # R type inst in WB
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in ex
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in ex
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in ex
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for Branch type
    elif opcode == "1100011":
        # R type inst in ex
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in ex
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in ex
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in ex
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:  # rs2 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
            if rs2 == ex.instpkt.rd and int(rs2, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal
    # for JALR
    elif opcode == "1100111":
        # R type inst in ex
        if ex.instpkt.opcode == "0110011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # I type inst in ex
        if ex.instpkt.opcode == "0010011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # Load instruction in ex
        if ex.instpkt.opcode == "0000011":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # U type instruction in ex
        # LUI
        if ex.instpkt.opcode == "0110111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # AUIPC
        if ex.instpkt.opcode == "0010111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:  # rs1 hazard
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JAL
        if ex.instpkt.opcode == "1101111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # for JALR
        if ex.instpkt.opcode == "1100111":
            if rs1 == ex.instpkt.rd and int(rs1, 2) != 0:
                stall_count = 4
                ex.data_hazard_stalls += 3
                ex.data_hazard_count += 1
        # no need to do anything for store,branch and jal


def bin_to_dec(binary: str) -> int:
    """Converts a binary string (2's complement representation) to its decimal equivalent"""
    if binary[0] == "0":
        return int(binary, 2)
    else:
        return int(binary, 2) - 2 ** len(binary)


def decode() -> None:
    """Decodes the instruction and passes the required values to the execute stage"""
    # print("In DE")
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, immU, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress, nop

    global opcode, stall_count, current_instruction
    # update the pipeline register with values from instruction fetch
    instpkt.instruction = fi.instruction
    instpkt.pc = fi.prev_pc
    instpkt.nop = nop
    instruction = instpkt.instruction

    if instpkt.nop == 1:
        print("DE: Bubble")
        current_instruction = "DE: Bubble"
        nop = 0
        fi.fetch()
        return
    if instruction is None:
        with open("output.txt", "a") as f:
            current_instruction = "\n\n"
            f.write("\n\n")
        return
    instruction = bin(int(instruction, 16))[2:].zfill(32)
    pc = instpkt.pc
    opcode = instruction[25:]
    print(f"DE:for PC = {pc}")
    # R type
    if opcode == "0110011":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        print(rs1)
        rs2 = instruction[7:12]
        func7 = instruction[:7]

        op1 = rg.x[int(rs1, 2)]
        op2 = rg.x[int(rs2, 2)]
        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                current_instruction = "DE: Stall"
                fi.current_instruction = "IF: Stall"
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        if func3 == "000":
            # ADD
            if func7 == "0000000":
                OP2Select = 0
                ALUOperation = 0
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0
                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: ADD, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: ADD, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
            # SUB
            elif func7 == "0100000":
                OP2Select = 0
                ALUOperation = 1
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0
                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: SUB, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SUB, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
        # XOR
        elif func3 == "100":
            OP2Select = 0
            ALUOperation = 2
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): R-type instruction: XOR, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: XOR, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
        # OR
        elif func3 == "110":
            OP2Select = 0
            ALUOperation = 3
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): R-type instruction: OR, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: OR, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
        # AND
        elif func3 == "111":
            OP2Select = 0
            ALUOperation = 4
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): R-type instruction: AND, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: AND, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
        # SLL
        elif func3 == "001":
            OP2Select = 0
            ALUOperation = 5
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): R-type instruction: SLL, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SLL, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
        elif func3 == "101":
            # SRL
            if func7 == "0000000":
                OP2Select = 0
                ALUOperation = 6
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0
                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: SRL, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SRL, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
            # SRA
            elif func7 == "0100000":
                OP2Select = 0
                ALUOperation = 7
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0
                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: SRA, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SRA, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, rd = x{int(rd, 2)}\n"
    # I type
    elif opcode == "0010011":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        imm = bin_to_dec(instruction[:12])

        op1 = rg.x[int(rs1, 2)]
        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        # ADDI
        if func3 == "000":
            OP2Select = 1
            ALUOperation = 0
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: ADDI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: ADDI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # XORI
        elif func3 == "100":
            OP2Select = 1
            ALUOperation = 2
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: XORI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: XORI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # ORI
        elif func3 == "110":
            OP2Select = 1
            ALUOperation = 3
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: ORI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: ORI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # ANDI
        elif func3 == "111":
            OP2Select = 1
            ALUOperation = 4
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: ANDI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: ANDI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # SLLI
        elif func3 == "001":
            OP2Select = 1
            ALUOperation = 5
            MemOp = 0
            ResultSelect = 0
            RFWrite = 1
            BranchTargetAddress = 0

            # imm = bin_to_dec(instruction[7:12])
            imm = int(instruction[7:12], 2)
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: SLLI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: SLLI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        elif func3 == "101":
            # imm = bin_to_dec(instruction[7:12])
            imm = int(instruction[7:12], 2)

            # SRLI
            if instruction[:7] == "0000000":
                OP2Select = 1
                ALUOperation = 6
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0

                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: SRLI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SRLI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
            # SRAI
            elif instruction[:7] == "0100000":
                OP2Select = 1
                ALUOperation = 7
                MemOp = 0
                ResultSelect = 0
                RFWrite = 1
                BranchTargetAddress = 0
                with open("output.txt", "a") as f:
                    f.write(
                        f"DE (pc: {hex(pc)}): R-type instruction: SRAI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                    )
                    current_instruction = f"DE (pc: {hex(pc)}): R-type instruction: SRAI, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
    # I type continued (LB, LH, LW)
    elif opcode == "0000011":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        imm = bin_to_dec(instruction[:12])

        op1 = rg.x[int(rs1, 2)]
        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        # LB
        if func3 == "000":
            OP2Select = 1
            ALUOperation = 0
            MemOp = 1
            ResultSelect = 1
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: LB, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: LB, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # LH
        elif func3 == "001":
            OP2Select = 1
            ALUOperation = 0
            MemOp = 1
            ResultSelect = 1
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: LH, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: LH, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
        # LW
        elif func3 == "010":
            OP2Select = 1
            ALUOperation = 0
            MemOp = 1
            ResultSelect = 1
            RFWrite = 1
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): I-type instruction: LW, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: LW, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}, rd = x{int(rd, 2)}\n"
    # S type
    elif opcode == "0100011":
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        immS = bin_to_dec(instruction[:7] + instruction[20:25])

        op1 = rg.x[int(rs1, 2)]
        op2 = rg.x[int(rs2, 2)]

        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        # SB
        if func3 == "000":
            OP2Select = 2
            ALUOperation = 0
            MemOp = 2
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): S-type instruction: SB, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): S-type instruction: SB, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
        # SH
        elif func3 == "001":
            OP2Select = 2
            ALUOperation = 0
            MemOp = 2
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): S-type instruction: SH, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): S-type instruction: SH, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
        # SW
        elif func3 == "010":
            OP2Select = 2
            ALUOperation = 0
            MemOp = 2
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = 0
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): S-type instruction: SW, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): S-type instruction: SW, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immS = {immS}\n"
    # B type
    elif opcode == "1100011":
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]
        immB = bin_to_dec(
            instruction[0]
            + instruction[24]
            + instruction[1:7]
            + instruction[20:24]
            + "0"
        )

        op1 = rg.x[int(rs1, 2)]
        op2 = rg.x[int(rs2, 2)]

        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        # BEQ
        if func3 == "000":
            OP2Select = 0
            ALUOperation = 8
            MemOp = 0
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = pc + immB
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): B-type instruction: BEQ, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): B-type instruction: BEQ, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
        # BNE
        elif func3 == "001":
            OP2Select = 0
            ALUOperation = 9
            MemOp = 0
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = pc + immB
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): B-type instruction: BNE, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): B-type instruction: BNE, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
        # BGE
        elif func3 == "101":
            OP2Select = 0
            ALUOperation = 10
            MemOp = 0
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = pc + immB
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): B-type instruction: BGE, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): B-type instruction: BGE, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
        # BLT
        elif func3 == "100":
            OP2Select = 0
            ALUOperation = 11
            MemOp = 0
            ResultSelect = 0
            RFWrite = 0
            BranchTargetAddress = pc + immB
            with open("output.txt", "a") as f:
                f.write(
                    f"DE (pc: {hex(pc)}): B-type instruction: BLT, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
                )
                current_instruction = f"DE (pc: {hex(pc)}): B-type instruction: BLT, rs1 = x{int(rs1, 2)} = {op1}, rs2 = x{int(rs2, 2)} = {op2}, immB = {immB}\n"
    # U type
    # LUI
    elif opcode == "0110111":
        rd = instruction[20:25]
        immU = bin_to_dec(instruction[:20] + "0" * 12)

        OP2Select = 0
        ALUOperation = 12
        MemOp = 0
        ResultSelect = 2
        RFWrite = 1
        BranchTargetAddress = 0
        with open("output.txt", "a") as f:
            f.write(
                f"DE (pc: {hex(pc)}): U-type instruction: LUI, rd = x{int(rd, 2)}, immU = {immU}\n"
            )
        current_instruction = f"DE (pc: {hex(pc)}): U-type instruction: LUI, rd = x{int(rd, 2)}, immU = {immU}\n"
    # AUIPC
    elif opcode == "0010111":
        rd = instruction[20:25]
        immU = bin_to_dec(instruction[:20] + "0" * 12)
        op1, op2 = 0, 0
        OP2Select = 0
        ALUOperation = 0
        MemOp = 0
        ResultSelect = 4
        RFWrite = 1
        BranchTargetAddress = 0
        with open("output.txt", "a") as f:
            f.write(
                f"DE (pc: {hex(pc)}): U-type instruction: AUIPC, rd = x{int(rd, 2)}, immU = {immU}\n"
            )
            current_instruction = f"DE (pc: {hex(pc)}): U-type instruction: AUIPC, rd = x{int(rd, 2)}, immU = {immU}\n"
    # J type JAL
    elif opcode == "1101111":
        rd = instruction[20:25]
        immJ = bin_to_dec(
            instruction[0]
            + instruction[12:20]
            + instruction[11]
            + instruction[1:11]
            + "0"
        )

        OP2Select = 0
        ALUOperation = 12
        MemOp = 0
        ResultSelect = 3
        RFWrite = 1
        BranchTargetAddress = pc + immJ
        with open("output.txt", "a") as f:
            f.write(
                f"DE (pc: {hex(pc)}): J-type instruction: JAL, rd = x{int(rd, 2)}, immJ = {immJ}\n"
            )
        current_instruction = f"DE (pc: {hex(pc)}): J-type instruction: JAL, rd = x{int(rd, 2)}, immJ = {immJ}\n"
    # I type JALR
    elif opcode == "1100111":
        rd = instruction[20:25]
        func3 = instruction[17:20]
        rs1 = instruction[12:17]
        imm = bin_to_dec(instruction[:12])

        op1 = rg.x[int(rs1, 2)]
        if knobs.data_forwarding == 1:
            check_wb()
        else:
            if stall_count == 0:
                check_wb()
                check_ma()
                check_ex()
            if stall_count > 1:
                instpkt.nop = 1
                stall_count -= 1
                return
            elif stall_count > 0:
                stall_count -= 1
        # !!!!!!!!! IsBranch should select ALUResult !!!!!!!!!
        OP2Select = 1
        ALUOperation = 0
        MemOp = 0
        ResultSelect = 3
        RFWrite = 1
        BranchTargetAddress = 0
        with open("output.txt", "a") as f:
            f.write(
                f"DE (pc: {hex(pc)}): I-type instruction: JALR, rd = x{int(rd, 2)}, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}\n"
            )
            current_instruction = f"DE (pc: {hex(pc)}): I-type instruction: JALR, rd = x{int(rd, 2)}, rs1 = x{int(rs1, 2)} = {op1}, imm = {imm}\n"
    # calling instruction fetch now
    fi.fetch()


def init() -> None:
    """Initializes all global variables to their initial value"""
    global instruction, pc, rs1, rs2, rd, func3, func7, op1, op2, imm, immS, immB, immJ, OP2Select, ALUOperation, MemOp, ResultSelect, RFWrite, BranchTargetAddress, stall_count, current_instruction
    global nop,stall_count
    (
        instruction,
        pc,
        rs1,
        rs2,
        rd,
        func3,
        func7,
        op1,
        op2,
        imm,
        immS,
        immB,
        immJ,
        OP2Select,
        ALUOperation,
        MemOp,
        ResultSelect,
        RFWrite,
        BranchTargetAddress,
        current_instruction,
    ) = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ""
    )
    nop=0
    stall_count=0
