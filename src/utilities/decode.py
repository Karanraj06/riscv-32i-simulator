instruction='0x00000000'
pc='0x0'
next_pc='0x0'
def dec_to_bin(x):
    my_list=[0,0,0,0]
    for i in range(0,4):
        my_list[4-i-1]=x%2
        x=x//2
    return str(my_list)
def decode():
    inst_bin=str(bin(int(instruction,16)))
    if(int(instruction[2])<8):
        temp=inst_bin[::-1]
        temp=temp[0:28:]
        temp=temp[::-1]
        inst_bin='0b'+dec_to_bin(instruction[2])+temp
    #lets invert the inst_bin for easier indexing
    inst_bin=inst_bin[::-1]
    #for opcode
    opcode=inst_bin[0:7:]
    opcode=opcode[::-1]
    #for rd
    rd=inst_bin[7:12:]
    rd=rd[::-1]
    #for funct3
    funct3=inst_bin[12:15:]
    funct3=funct3[::-1]
    #for rs1
    rs1=inst_bin[15:20:]
    rs1=rs1[::-1]
    #for rs2
    rs2=inst_bin[20:25:]
    rs2=rs2[::-1]
    #for funct7
    funct7=inst_bin[25:32:]
    funct7=funct7[::-1]
    #for immI
    immI=inst_bin[20:32:]
    immI=immI[::-1]
    #for immS
    immS=funct7+rd
    #for immU
    immU=inst_bin[12:32:]
    immU=immU[::-1]

    
