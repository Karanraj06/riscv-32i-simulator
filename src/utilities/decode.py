
instruction='0x00000000'
pc='0x0'
next_pc='0x0'
def decode():
    inst_bin=str(bin(int(instruction,16)))
    if(int(instruction[2])<8):
        temp=instruction[::-1]