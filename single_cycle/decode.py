import execute
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
    opcode='0b'+opcode[::-1]
    #for rd
    rd=inst_bin[7:12:]
    rd='0b'+rd[::-1]
    #for funct3
    funct3=inst_bin[12:15:]
    funct3='0b'+funct3[::-1]
    #for rs1
    rs1=inst_bin[15:20:]
    rs1='0b'+rs1[::-1]
    #for rs2
    rs2=inst_bin[20:25:]
    rs2='0b'+rs2[::-1]
    #for funct7
    funct7=inst_bin[25:32:]
    funct7='0b'+funct7[::-1]
    #for immI
    immI=inst_bin[20:32:]
    immI=immI[::-1]#now we need to perform sign extension
    if(immI[0]=='1'):
        immI='0b11111111111111111111'+immI
    else:
        immI='0b00000000000000000000'+immI
    #for immS
    immS=funct7+rd
    if(immS[0]=='1'):
        immS='0b11111111111111111111'+immS
    else:
        immS='0b00000000000000000000'+immS
    #for immU
    immU=inst_bin[12:32:]
    immU=immU[::-1]
    if(immU[0]=='1'):
        immU='0b111111111111'+immU
    else:
        immU='0b000000000000'+immU

    #for control signals(we set them according to the different opcodes)
    #for R type
    # if(opcode=='0b0110011'):
    #     execute.rfWrite=1
    #     execute.isBranch_de=0
    #     execute.isBranch_ALU=0
    #     execute.op2Select=0