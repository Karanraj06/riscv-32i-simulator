# ============ IsBranch: 0 -> pc + 4, 1 -> BranchTargetAddress, 2 -> ALUResult ==============
from pipeline_registers import DE_EX as instpkt
from pipeline_registers import IF_DE as prev_pip
import data_lock_unit as lock
import decode as de
import memory_access as ma
import instruction_fetch as fi

# for forwarding
import write_back as wb
import knobs

# ===========GLOBAL VARIABLES===============
aluResult: int = None
isBranch: int = None
stall_count: int = 0
control_hazard_stalls: int = 0
control_hazard_count: int = 0
branch_mispredictions: int = 0
alu_instructions: int = 0
control_instructions: int = 0
data_hazard_count:int=0
data_hazard_stalls:int=0
current_instruction = ""
#for highlighting data forwarding path
de_forwarding_path:list[str]=""
ex_forwarding_path:list[str]=""
ma_forwarding_path:list[str]=""
#dependency type
de_dependency=""
ex_dependency=""
ma_dependency=""

def check_ma() -> None:
    global stall_count,data_hazard_stalls,data_hazard_count,ex_forwarding_path,ex_dependency
    # for R type
    if instpkt.opcode == "0110011":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU + ma.instpkt.pc
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.immU + ma.instpkt.pc
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for I type
    elif instpkt.opcode == "0010011":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU + ma.instpkt.pc
        # no need to do anything for store,branch and jal
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
    # for Load type
    elif instpkt.opcode == "0000011":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU + ma.instpkt.pc
        # no need to do anything for store,branch and jal
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
    # for Store type
    elif instpkt.opcode == "0100011":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU + ma.instpkt.pc
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
    # for Branch Type
    elif instpkt.opcode == "1100011":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU + ma.instpkt.pc
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.immU + ma.instpkt.pc
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
            if instpkt.rs2 == ma.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op2 = ma.instpkt.pc + 4
    # for JALR
    elif instpkt.opcode == "1100111":
        # R type inst in MA
        if ma.instpkt.opcode == "0110011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # I type inst in MA
        if ma.instpkt.opcode == "0010011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.aluResult
        # Load instruction in MA
        if ma.instpkt.opcode == "0000011":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.loadData
                stall_count = 2
                data_hazard_stalls += 1
                data_hazard_count += 1
        # U type instruction in MA
        # LUI
        if ma.instpkt.opcode == "0110111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.immU
        # AUIPC
        if ma.instpkt.opcode == "0010111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + ma.instpkt.immU
        # for JAL
        if ma.instpkt.opcode == "1101111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
        # for JALR
        if ma.instpkt.opcode == "1100111":
            if instpkt.rs1 == ma.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="MA-EX "
                ex_dependency="Data "
                instpkt.op1 = ma.instpkt.pc + 4
        # no need to do anything for store,branch and jal


def check_wb() -> None:
    global ex_forwarding_path
    # for R type
    if instpkt.opcode == "0110011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for I type
    elif instpkt.opcode == "0010011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for Load type
    elif instpkt.opcode == "0000011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for store type
    elif instpkt.opcode == "0100011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for Branch type
    elif instpkt.opcode == "1100011":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:  # rs2 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
            if instpkt.rs2 == wb.instpkt.rd and int(instpkt.rs2, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op2 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal
    # for JALR
    elif instpkt.opcode == "1100111":
        # R type inst in WB
        if wb.instpkt.opcode == "0110011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # I type inst in WB
        if wb.instpkt.opcode == "0010011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.aluResult
        # Load instruction in WB
        if wb.instpkt.opcode == "0000011":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.loadData
        # U type instruction in WB
        # LUI
        if wb.instpkt.opcode == "0110111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU
        # AUIPC
        if wb.instpkt.opcode == "0010111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:  # rs1 hazard
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.immU + wb.instpkt.pc
        # for JAL
        if wb.instpkt.opcode == "1101111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        # for JALR
        if wb.instpkt.opcode == "1100111":
            if instpkt.rs1 == wb.instpkt.rd and int(instpkt.rs1, 2) != 0:
                ex_forwarding_path+="WB-EX "
                instpkt.op1 = wb.instpkt.pc + 4
        # no need to do anything for store,branch and jal


def data_hazard() -> None:
    check_wb()
    check_ma()


def srl(a: int, b: int) -> int:
    if a >= 0:
        return a >> b
    else:
        return (a + 0x100000000) >> b


def sll(
    a: int, b: int
) -> (
    int
):  # required as python doesnt have 32 bit limit on int,when we use left shift,python arbitrarily extends the number
    if b >= 32:
        return 0
    else:
        a = ma.dec_to_bin(a)
        a = a[b:].ljust(32, "0")
        return de.bin_to_dec(a)


def add_32Bit(binstr1, binstr2):
    # binstr1 = dec2bin(num1)
    # binstr2 = dec2bin(num2)

    binAddStr = [0] * 32
    carry = 0
    for ind in range(32):
        add = (int(binstr1[::-1][ind]) + int(binstr2[::-1][ind]) + carry) % 2
        carry = (int(binstr1[::-1][ind]) + int(binstr2[::-1][ind]) + carry) // 2
        binAddStr[ind] = str(add)
    return int("".join(binAddStr[::-1]), 2)


def execute() -> int:
    global aluResult, isBranch, stall_count, control_hazard_count, control_hazard_stalls, branch_mispredictions, alu_instructions, control_instructions, current_instruction
    global de_forwarding_path,ex_forwarding_path,ma_forwarding_path,ex_dependency
    # print("In EX")
    # updating values in pipeline register from decode
    instpkt.nop = prev_pip.nop
    if instpkt.nop == 1:
        print("EX: Bubble")
        current_instruction = "EX: Bubble"
        de.decode()
        return
    instpkt.instruction = de.instruction
    if instpkt.instruction is None:
        with open("output.txt", "a") as f:
            f.write("\n\n")
            current_instruction = "\n\n"
        return
    if stall_count == 0:
        instpkt.pc = de.pc

        instpkt.rs1 = de.rs1
        instpkt.rs2 = de.rs2
        instpkt.rd = de.rd
        instpkt.func3 = de.func3
        instpkt.func7 = de.func7
        instpkt.op1 = de.op1
        instpkt.op2 = de.op2
        instpkt.opcode = de.opcode

        instpkt.imm = de.imm
        instpkt.immS = de.immS
        instpkt.immU = de.immU
        instpkt.immB = de.immB
        instpkt.immJ = de.immJ

        instpkt.OP2Select = de.OP2Select
        instpkt.ALUOperation = de.ALUOperation
        instpkt.MemOp = de.MemOp
        instpkt.ResultSelect = de.ResultSelect
        instpkt.RFWrite = de.RFWrite
        instpkt.BranchTargetAddress = de.BranchTargetAddress
    print(f"EX: for PC = {instpkt.pc}")
    if knobs.data_forwarding == 1:
        if stall_count == 0:
            data_hazard()  # to check if data hazards are present
            print(ex_forwarding_path)
        if stall_count > 1:
            current_instruction = "EX: Stall"
            fi.current_instruction = "IF: Stall"
            de.current_instruction = "DE: Stall"
            instpkt.nop = 1
            stall_count -= 1
            return
        elif stall_count > 0:
            check_wb()
            print(ex_forwarding_path)
            stall_count -= 1
    op1: int = instpkt.op1
    op2: int = None
    # Selecting op2
    if instpkt.OP2Select == 0:
        op2 = instpkt.op2
    elif instpkt.OP2Select == 1:
        op2 = instpkt.imm
    elif instpkt.OP2Select == 2:
        op2 = instpkt.immS
    # opening file to write output
    f = open("output.txt", "a")
    if instpkt.ALUOperation == 0:
        alu_instructions += 1
        aluResult = add_32Bit(ma.dec_to_bin(op1), ma.dec_to_bin(op2))
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): ADD {op1} and {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): ADD {op1} and {op2}\n"
    elif instpkt.ALUOperation == 1:
        alu_instructions += 1
        aluResult = add_32Bit(ma.dec_to_bin(op1), ma.dec_to_bin(-1 * op2))
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): SUB {op1} from {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): SUB {op1} from {op2}\n"
    elif instpkt.ALUOperation == 2:
        alu_instructions += 1
        aluResult = op1 ^ op2
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} XOR {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} XOR {op2}\n"
    elif instpkt.ALUOperation == 3:
        alu_instructions += 1
        aluResult = op1 | op2
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} OR {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} OR {op2}\n"
    elif instpkt.ALUOperation == 4:
        alu_instructions += 1
        aluResult = op1 & op2
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} AND {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} AND {op2}\n"
    elif instpkt.ALUOperation == 5:
        alu_instructions += 1
        aluResult = sll(op1, op2)
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} << {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} << {op2}\n"
    elif instpkt.ALUOperation == 6:
        alu_instructions += 1
        if op2 >= 32:
            op2 = op2 % 32
        aluResult = srl(op1, op2)
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} >>> {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} >>> {op2}\n"
    elif instpkt.ALUOperation == 7:
        alu_instructions += 1
        if op2 > 32:
            op2 = op2 % 32
        aluResult = op1 >> op2
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} >> {op2}\n")
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): {op1} >> {op2}\n"
    elif instpkt.ALUOperation == 8:
        control_instructions += 1
        if instpkt.pc not in fi.branch_target_buffer.keys():
            fi.branch_target_buffer[instpkt.pc] = [instpkt.BranchTargetAddress, 0]
        if op1 == op2:
            if fi.branch_target_buffer[instpkt.pc][1] == 0:
                fi.branch_target_buffer[instpkt.pc][1] = 1
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.BranchTargetAddress
            isBranch = 1
            print(f"EX: BEQ PC set to {instpkt.BranchTargetAddress}")
            f.write(f"EXECUTE:BEQ PC set to {instpkt.BranchTargetAddress}\n")
            current_instruction = (
                f"EXECUTE:BEQ PC set to {instpkt.BranchTargetAddress}\n"
            )
        else:
            if fi.branch_target_buffer[instpkt.pc][1] == 1:
                fi.branch_target_buffer[instpkt.pc][1] = 0
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.pc + 4
            isBranch = 0
            f.write("EXECUTE: Brach not taken\n")
            current_instruction = "EXECUTE: Brach not taken\n"
    elif instpkt.ALUOperation == 9:
        control_instructions += 1
        if instpkt.pc not in fi.branch_target_buffer.keys():
            fi.branch_target_buffer[instpkt.pc] = [instpkt.BranchTargetAddress, 0]
        if op1 != op2:
            if fi.branch_target_buffer[instpkt.pc][1] == 0:
                fi.branch_target_buffer[instpkt.pc][1] = 1
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.BranchTargetAddress
            isBranch = 1
            f.write(f"EXECUTE:BNE PC set to {instpkt.BranchTargetAddress}\n")
            current_instruction = (
                f"EXECUTE:BNE PC set to {instpkt.BranchTargetAddress}\n"
            )
        else:
            if fi.branch_target_buffer[instpkt.pc][1] == 1:
                fi.branch_target_buffer[instpkt.pc][1] = 0
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.pc + 4
            isBranch = 0
            f.write("EXECUTE: Brach not taken\n")
            current_instruction = "EXECUTE: Brach not taken\n"
    elif instpkt.ALUOperation == 10:
        control_instructions += 1
        if instpkt.pc not in fi.branch_target_buffer.keys():
            fi.branch_target_buffer[instpkt.pc] = [instpkt.BranchTargetAddress, 0]
        if op1 >= op2:
            if fi.branch_target_buffer[instpkt.pc][1] == 0:
                fi.branch_target_buffer[instpkt.pc][1] = 1
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.BranchTargetAddress
            isBranch = 1
            f.write(f"EXECUTE:BGE PC set to {instpkt.BranchTargetAddress}\n")
            current_instruction = (
                f"EXECUTE:BGE PC set to {instpkt.BranchTargetAddress}\n"
            )
        else:
            if fi.branch_target_buffer[instpkt.pc][1] == 1:
                fi.branch_target_buffer[instpkt.pc][1] = 0
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.pc + 4
            isBranch = 0
            f.write("EXECUTE: Brach not taken\n")
            current_instruction = "EXECUTE: Brach not taken\n"
    elif instpkt.ALUOperation == 11:
        control_instructions += 1
        if instpkt.pc not in fi.branch_target_buffer.keys():
            fi.branch_target_buffer[instpkt.pc] = [instpkt.BranchTargetAddress, 0]
        if op1 < op2:
            if fi.branch_target_buffer[instpkt.pc][1] == 0:
                fi.branch_target_buffer[instpkt.pc][1] = 1
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.BranchTargetAddress
            isBranch = 1
            f.write(f"EXECUTE:BLT PC set to {instpkt.BranchTargetAddress}\n")
            current_instruction = (
                f"EXECUTE:BLT PC set to {instpkt.BranchTargetAddress}\n"
            )
        else:
            if fi.branch_target_buffer[instpkt.pc][1] == 1:
                fi.branch_target_buffer[instpkt.pc][1] = 0
                lock.stall()
                ex_dependency+="Control"
                control_hazard_count += 1
                control_hazard_stalls += 2
                branch_mispredictions += 1
                fi.pc = instpkt.pc + 4
            isBranch = 0
            f.write("EXECUTE: Brach not taken\n")
            current_instruction = "EXECUTE: Brach not taken\n"
    # for JAL
    if instpkt.opcode == "1101111":
        control_instructions += 1
        if instpkt.pc not in fi.branch_target_buffer.keys():
            fi.branch_target_buffer[instpkt.pc] = [instpkt.BranchTargetAddress, 0]
        if fi.branch_target_buffer[instpkt.pc][1] == 0:
            fi.branch_target_buffer[instpkt.pc][1] = 1
            lock.stall()
            ex_dependency+="Control"
            control_hazard_count += 1
            control_hazard_stalls += 2
            branch_mispredictions += 1
            fi.pc = instpkt.BranchTargetAddress
        print(f"JAL!!!:PC set from {instpkt.pc+8}to {instpkt.BranchTargetAddress}")
        f.write(
            f"EXECUTE (pc: {hex(instpkt.pc)}): PC set to {instpkt.BranchTargetAddress}\n"
        )
        current_instruction = f"EXECUTE (pc: {hex(instpkt.pc)}): PC set to {instpkt.BranchTargetAddress}\n"
    elif instpkt.opcode == "1100111":  # for JALR
        control_instructions += 1
        lock.stall()
        ex_dependency+="Control"
        control_hazard_count += 1
        control_hazard_stalls += 2
        fi.pc = aluResult
        f.write(f"EXECUTE (pc: {hex(instpkt.pc)}): PC set to {aluResult}\n")
        current_instruction = (
            f"EXECUTE (pc: {hex(instpkt.pc)}): PC set to {aluResult}\n"
        )
    f.close()

    # calling decode now
    de.decode()


def init() -> None:
    """Initializes all global variables to their initial value"""
    global aluResult, isBranch, current_instruction,stall_count,control_hazard_stalls,control_hazard_count,branch_mispredictions,alu_instructions,control_instructions
    global data_hazard_count,data_hazard_stalls
    aluResult = None
    isBranch = None
    current_instruction = ""
    stall_count=0
    control_hazard_stalls=0
    control_hazard_count=0
    branch_mispredictions=0
    alu_instructions=0
    control_instructions=0
    data_hazard_count=0
    data_hazard_stalls=0
