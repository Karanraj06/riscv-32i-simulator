#==============! Incomplete SB,SH,LB,LH(check how it works)==========
import decode as de
import execute as ex
# ========Globals=========
loadData: int = None
# Data Memory
data_memory: dict[int, str] = {}


def update_mem(address: str, value: str) -> None:
    global data_memory
    data_memory[int(address, 16)] = bin(int(value, 16))[2:].zfill(32)


def dec_to_bin(x: int) -> str:
    ret = bin(x)
    if (x < 0):
        ret=ret[3:]
        ret=bin(2**len(ret)+2**len(ret)+x)
        ret=ret[2:].rjust(32,'1')
    else:
        ret = ret[2:].zfill(32)
    return ret

def memory_access() -> None:
    global loadData
    f = open("output.txt", "a")
    if (de.MemOp == 0):
        f.write(f"MEMORY:No Memory Operation\n")
        pass
    elif (de.MemOp == 1):
        f.write(f"MEMORY: Load at address {ex.aluResult}")
        if(de.func3=='010'):#for LW
            loadData = de.bin_to_dec(data_memory[ex.aluResult])
            print(f"The loaded value is{loadData}")
        elif(de.func3=='000'):#for LB
            pass
        elif(de.func3=='001'):#for LH
            pass
    elif (de.MemOp == 2):
        if(de.func3=='010'):#for SW
            f.write(f"MEMORY: Store {de.op2} at address {ex.aluResult}")
            data_memory[ex.aluResult] = dec_to_bin(de.op2)
        elif(de.func3=='000'):#for SB
            pass
        elif(de.func3=='001'):#for SH
            pass


def init() -> None:
    """Initialize the global variables"""
    global loadData,data_memory
    loadData = None
    data_memory={}
