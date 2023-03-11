import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg

def print_output():
    print("#=========Register File===========#")
# Read the contents of the input file and store them in instruction_memory
# !!!!!!!!!!IMPORTANT!!!!!!!!!!
# data memory is not part of input.mc, it will be filled as the instructions are executed
with open("input.mc", "r") as f:
    while True:
        key, value = f.readline().split()
        if value == "_":
            fi.instruction_memory[int(key, 16)] = None
            break
        else:
            fi.instruction_memory[int(key, 16)] = value

# Clearing the contents of the output file before writing anything.
with open("output.txt", "w") as f:      
    f.truncate(0)
    
def run() -> None:
    '''Executes the program until the end of the instruction memory is reached'''
    while(step()):
        continue
    print_output()



def step() -> None:
    '''Executes one instruction'''
    if (not fi.fetch()):
        de.decode()
        ex.execute()
        ma.memory_access()
        wb.writeBack()
        return True
    print("\n\n#================Program execution Successful!!!=====================#\n\n")
    return False


def reset() -> None:
    '''Resets to the initial state'''
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
        step()
    elif choice == "3":
        reset()
    else:
        print("Invalid choice")
