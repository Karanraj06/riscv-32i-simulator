import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg


def print_output():
    print("# ========= Register File ===========")
    track = 0
    for x in rg.x:
        print(f"x{track} : {x}")
        track += 1
    print("# =============== Data Memory ===========")
    # we will first sort the data memory according to address
    mem_addresses = list(ma.data_memory.keys())
    mem_addresses.sort()
    sorted_memory = {i: ma.data_memory[i] for i in mem_addresses}
    for key in mem_addresses:
        value = de.bin_to_dec(ma.data_memory[key])
        key = "0x" + (hex(key)[2:].zfill(8))
        if key[2] == "1":
            print(f"{key}: {value}")


with open("input.mc", "r") as f:
    lines = f.readlines()
    track = 0
    for line in lines:
        key, value = line.split()
        if track == 0:
            print(key + " " + value)
            if value == "_":
                fi.instruction_memory[int(key, 16)] = None
                track = 1
            else:
                fi.instruction_memory[int(key, 16)] = value
        elif track == 1:
            print(key + " " + value)
            ma.update_mem(key, value)

# Clearing the contents of the output file before writing anything.
with open("output.txt", "w") as f:
    f.truncate(0)


def run() -> None:
    """Executes the program until the end of the instruction memory is reached"""
    while step():
        continue
    print_output()


def step() -> bool:
    """Executes one instruction"""
    if fi.fetch():
        de.decode()
        ex.execute()
        ma.memory_access()
        wb.writeBack()
        return True
    print("# =============== Program Execution Successfull. =================")
    return False


def reset() -> None:
    """Resets to the initial state"""
    fi.init()
    de.init()
    ex.init()
    ma.init()
    wb.init()
    rg.init()
    with open("output.txt", "w") as f:
        f.truncate(0)


while True:
    print("1. Run")
    print("2. Step")
    print("3. Reset")

    choice = input("Enter your choice: ")

    if choice == "1":
        run()
        break
    elif choice == "2":
        if not step():
            print_output()
            break
    elif choice == "3":
        reset()
    else:
        print("Invalid choice")
