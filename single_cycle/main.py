from utilities import instruction_fetch,decode,execute,memory_access,write_back
pc='0x0'
end=0
if(__name__=="__main__"):
    with open('input.mc',mode="r") as inp_file:
        lines_list=inp_file.readlines()
        for line in lines_list:
            y=line.split()
            instruction_fetch.instructionMemory[y[0]]=y[1]
#instruction memory has been populated
keys_list=instruction_fetch.instructionMemory.keys()
for key in keys_list:
    pc=key
    break
while(1):
    instruction_fetch.pc=pc
    instruction_fetch.fetch()
    if not end:
       decode.decode()
       execute.execute()
       memory_access.ma()
       write_back.wb()
    else:
        break