from collections import defaultdict
#Data Memory
data_memory:defaultdict[int,str]=defaultdict(lambda:None)
def update_mem(address:str,value:str)->None:
    global data_memory
    data_memory[int(address,16)]=bin(int(value, 16))[2:].zfill(32)

def memory_access()->None: