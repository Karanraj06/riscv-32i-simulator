# Importing the required modules
import sys
sys.path.append('utilities')
from utilities import instruction_fetch, decode, execute, memory_access, write_back

# from utilities import instruction_fetch
execute.aluOperation = 0
decode.rd = 0
pc = "0x0"

with open("input.mc", "r") as f:
    while True:
        key, value = f.readline().split()
        instruction_fetch.instruction_memory[key] = value
        if value == '_':
            break


# instruction memory has been populated
keys_list = instruction_fetch.instruction_memory.keys()
for key in keys_list:
    pc = key
    break
# while 1:
#     instruction_fetch.pc = pc
#     instruction_fetch.fetch()
#     if not instruction_fetch.end:
#         decode.decode()
#         execute.execute()
#         memory_access.ma()
#         write_back.wb()
#     else:
#         break
print(key, instruction_fetch.instruction_memory.keys())