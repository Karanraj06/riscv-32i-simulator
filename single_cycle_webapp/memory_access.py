import decode as de
import execute as ex

# ======== Globals =========
loadData: int = None

# Data Memory
data_memory: dict[int, str] = {}

# Displaying the current instruction in Flask app
current_instruction: str = ""


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


def memory_access() -> None:
    global loadData, current_instruction
    # f = open("output.txt", "a")
    if de.MemOp == 0:
        # f.write(f"MEMORY:No Memory Operation\n")
        # pass
        current_instruction = "No Memory Operation"

    elif de.MemOp == 1:
        # f.write(f"MEMORY: Load at address {ex.aluResult}\n")
        current_instruction = f"Load at address {ex.aluResult}"

        # Check if memory address exists or not
        if ex.aluResult not in data_memory.keys():
            data_memory[ex.aluResult] = "0" * 32

        if de.func3 == "010":  # for LW
            loadData = de.bin_to_dec(data_memory[ex.aluResult])
            # print(f"The loaded value is{loadData}")

        elif de.func3 == "000":  # for LB
            temp = data_memory[ex.aluResult]
            loadData = de.bin_to_dec(temp[:8].rjust(32, temp[0]))
            # print(f"The loaded value is{loadData}")

        elif de.func3 == "001":  # for LH
            temp = data_memory[ex.aluResult]
            loadData = de.bin_to_dec(temp[:16].rjust(32, temp[0]))
            # print(f"The loaded value is{loadData}")

    elif de.MemOp == 2:
        if de.func3 == "010":  # for SW
            # f.write(f"MEMORY: Store {de.op2} at address {ex.aluResult}\n")
            current_instruction = f"Store {de.op2} at address {ex.aluResult}"

            data_memory[ex.aluResult] = dec_to_bin(de.op2)

        elif de.func3 == "000":  # for SB
            data_memory[ex.aluResult] = dec_to_bin(de.op2)[24:].zfill(32)
            current_instruction = "Store {de.bin_to_dec(dec_to_bin(de.op2)[24:].zfill(32))} at address {ex.aluResult}"

        elif de.func3 == "001":  # for SH
            data_memory[ex.aluResult] = dec_to_bin(de.op2)[16:].zfill(32)
            current_instruction = "Store {de.bin_to_dec(dec_to_bin(de.op2)[16:].zfill(32))} at address {ex.aluResult}"


def init() -> None:
    """Initialize the global variables"""
    global loadData, data_memory, current_instruction
    loadData = None
    data_memory = {}
    current_instruction = ""
