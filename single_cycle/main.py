import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg

# Read the contents of the input file and store them in instruction_memory and also in data memory
track: int = 0  # to know if we are now scanning data memory or instruction memory
with open("input.mc", "r") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split()
        if track == 0:
            print(key+" "+value)
            if value == "_":
                fi.instruction_memory[int(key, 16)] = None
                track = 1
            else:
                fi.instruction_memory[int(key, 16)] = value
        elif track == 1:
            print(key+" "+value)
            ma.update_mem(key, value)


def run() -> None:
    '''Executes the program until the end of the instruction memory is reached'''
    pass


def step() -> None:
    '''Executes one instruction'''
    if (not fi.fetch()):
        de.decode()
        ex.execute()
        ma.memory_access()
    pass


def reset() -> None:
    '''Resets to the initial state'''
    fi.init()
    de.init()
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
        step()
    elif choice == "3":
        reset()
    else:
        print("Invalid choice")
