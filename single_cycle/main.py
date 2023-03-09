import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg

# Read the contents of the input file and store them in instruction_memory
with open("input.mc", "r") as f:
    while True:
        key, value = f.readline().split()

        if value == "_":
            fi.instruction_memory[int(key, 16)] = None
            break
        else:
            fi.instruction_memory[int(key, 16)] = value


def run() -> None:
    '''Executes the program until the end of the instruction memory is reached'''
    pass


def step() -> None:
    '''Executes one instruction'''
    fi.fetch()
    pass


def reset() -> None:
    '''Resets to the initial state'''
    fi.init()
    de.init()

    rg.init()
    with open("output.txt", "w") as f:
        f.truncate(0)

print(fi.instruction_memory)
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
