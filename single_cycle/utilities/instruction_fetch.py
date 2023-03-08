import decode
end=0
instruction_memory = {}
next_pc = "0x0"
pc = "0x0"


def fetch():
    inst = instruction_memory[pc]
    decode.instruction = inst
    if(inst=='$'):
        end=1
    next_pc = str(hex(int(pc, 16) + 0x4))
    decode.next_pc = next_pc