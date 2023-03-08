from collections import defaultdict
import decode
instructionMemory=defaultdict(lambda:'$')
PC='0x0'
Next_PC='0x0'
def fetch():
    inst=instructionMemory[PC]
    decode.instruction=inst
    decode.PC=str(hex(int(PC,16)+0x4))
