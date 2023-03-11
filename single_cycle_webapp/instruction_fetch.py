import decode as de

# Instruction Memory
instruction_memory: dict[int, str] = {}

# Initialize Program Counter
pc: int = 0x0

# Displaying the current instruction in Flask app
current_instruction: str = ""


def fetch() -> bool:
    """
    Fetch the instruction from the instruction memory
    returns True if the program has reached the end of the instruction memory, False otherwise
    """

    global instruction_memory, pc, current_instruction

    instruction = instruction_memory[pc]

    # Write the fetch operation to the output file
    # with open("output.txt", "a") as f:
    #     if instruction is None:
    #         # HALT: Program has reached the end of the instruction memory
    #         f.write("Program execution completed successfully")
    #         return True
    #     else:
    #         f.write(f"IF: Fetch instruction {instruction} from address {hex(pc)}\n")

    if instruction is None:
        return True
    else:
        current_instruction = f"Fetch instruction {instruction} from address {hex(pc)}"

    # Program Counter is passed to the decode stage
    de.pc = pc

    # Increment the program counter by 4 to point to the next instruction
    pc += 4

    # Pass the instruction to the decode stage in binary format with 32 bits
    de.instruction = bin(int(instruction, 16))[2:].zfill(32)

    return False


def init() -> None:
    """Initializes pc to its initial value"""
    global pc, current_instruction, instruction_memory

    pc, current_instruction = 0x0, ""
    instruction_memory = {}