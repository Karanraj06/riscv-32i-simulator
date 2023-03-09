import decode as de
import execute as ex
from collections import defaultdict
#Data Memory
data_memory:defaultdict[int,str]=defaultdict(lambda:None)
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
    if(de.MemOp==0):
        pass
    elif(de.MemOp==1):
        loadData=de.bin_to_dec(data_memory[ex.aluResult])
    elif(de.MemOp==2):
        data_memory[ex.aluResult]=dec_to_bin(de.op2)