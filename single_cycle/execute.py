import decode as de
aluResult: int = None
isBranch: int = None


def execute()->int:
    global aluResult, isBranch
    op1 = de.op1
    op2 = de.op2
    if (de.ALUOperation == 0):
        aluResult = op1+op2
    elif (de.ALUOperation == 1):
        aluResult = op1-op2
    elif (de.ALUOperation == 2):
        aluResult = op1 ^ op2
    elif (de.ALUOperation == 3):
        aluResult = op1 | op2
    elif (de.ALUOperation == 4):
        aluResult = op1 & op2
    elif (de.ALUOperation == 5):
        aluResult = op1 << op2
    elif (de.ALUOperation == 6):
        aluResult = op1 >> op2
    elif (de.ALUOperation == 7):
        aluResult = op1 >> op2
    elif (de.ALUOperation == 8):
        if (op1 == op2):
            isBranch = 1
        else:
            isBranch = 0
    elif (de.ALUOperation == 9):
        if (op1 != op2):
            isBranch = 1
        else:
            isBranch = 0
    elif (de.ALUOperation == 10):
        if (op1 >= op2):
            isBranch = 1
        else:
            isBranch = 0
    elif (de.ALUOperation == 11):
        if (op1 < op2):
            isBranch = 1
        else:
            isBranch = 0
    print(aluResult)

# def init()->None:
#     '''Initializes all global variables to their initial value'''
#     global aluResult, isBranch = None , None
