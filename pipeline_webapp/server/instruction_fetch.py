import decode as de


current_instruction: str = ""

# Instruction Memory
instruction_memory: dict[int, str] = {}
# Branch Target Buffer
# pc branch_address taken/nt
branch_target_buffer: dict[int, list[int, int]] = {}
# Initialize Program Counter
pc: int = 0x0
instruction: str = None
nop: int = None
prev_pc: int = 0x0


def fetch() -> None:
    # print("In IF")
    """
    Fetch the instruction from the instruction memory
    returns True if the program has reached the end of the instruction memory, False otherwise
    """

    global instruction_memory, pc, instruction, prev_pc, current_instruction
    global nop
    if nop == 1:
        print("IF: Bubble")
        current_instruction = "IF: Bubble"
        nop = 0
        de.nop = 1
        return
    print(pc)
    instruction = instruction_memory[pc]
    print(f"IF:for PC = {pc}")
    # Write the fetch operation to the output file
    with open("output.txt", "a") as f:
        if instruction is not None:
            current_instruction = f"IF (pc: {hex(pc)}): Fetch instruction {instruction} from address {hex(pc)}\n\n"
            f.write(
                f"IF (pc: {hex(pc)}): Fetch instruction {instruction} from address {hex(pc)}\n\n"
            )
        else:
            current_instruction = "\n\n"
            f.write("\n\n")
    # Program Counter is passed to the decode stage
    # de.pc = pc

    # Increment the program counter by 4 to point to the next instruction
    if pc in branch_target_buffer.keys():
        if branch_target_buffer[pc][1] == 1:
            prev_pc = pc
            pc = branch_target_buffer[pc][0]
        else:
            prev_pc = pc
            pc += 4
    else:
        prev_pc = pc
        pc += 4
    # Pass the instruction to the decode stage in binary format with 32 bits
    # de.instruction = bin(int(instruction, 16))[2:].zfill(32)

    # return True


def init() -> None:
    """Initializes pc to its initial value"""
    global pc, prev_pc, current_instruction
    current_instruction = ""
    global nop
    nop = 0
    pc = 0x0
    prev_pc = 0x0
