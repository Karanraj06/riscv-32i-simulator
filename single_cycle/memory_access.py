import decode as de
import execute as ex
#========Globals=========
loadData: int=None
#Data Memory
data_memory:dict[int,str]={}
def update_mem(address:str,value:str)->None:
    global data_memory
    data_memory[int(address,16)]=bin(int(value, 16))[2:].zfill(32)

def dec_to_bin(x:int)->str:
    ret=bin(x)
    if(x<0):
        ret=ret[2:].rjust(32,'1')
    else:
        ret=ret[2:].zfill(32)    

def memory_access()->None:
    global loadData
    f=open("output.txt","a")
    if(de.MemOp==0):
        f.write(f"MEMORY:No Memory Operation\n")
        pass
    elif(de.MemOp==1):
        f.write(f"MEMORY: Load at address {ex.aluResult}")
        loadData=de.bin_to_dec(data_memory[ex.aluResult])
        print(f"The loaded value is{loadData}")
    elif(de.MemOp==2):
        f.write(f"MEMORY: Store at address {ex.aluResult}")
        data_memory[ex.aluResult]=dec_to_bin(de.op2)

def init()->None:
    """Initialize the global variables"""
    global loadData
    loadData=None
