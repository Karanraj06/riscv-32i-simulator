import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import registers as rg

# Initialize clock to 0
clk: int = 0

# Displaying the current instruction in Flask app
current_instruction: str = ""


def writeBack() -> None:
    """Writeback the result into the Register File by selecting ResultSelect accordingly."""
    global clk, current_instruction

    # if RFWrite is 0, then there is no need to write result
    if de.RFWrite == 0:
        # with open("output.txt", "a") as f:
        #     f.write(f"WRITEBACK:No writeback Operation\n\n")
        current_instruction = "No writeback Operation"
        clk += 1
        return

    # if rd is set to x0, then its value can't be updated
    if int(de.rd, 2) != 0:
        # Selecting ResultSelect
        if de.ResultSelect == 0:
            rg.x[int(de.rd, 2)] = ex.aluResult
        elif de.ResultSelect == 1:
            rg.x[int(de.rd, 2)] = ma.loadData
        elif de.ResultSelect == 2:
            rg.x[int(de.rd, 2)] = de.immU
        elif de.ResultSelect == 3:
            rg.x[int(de.rd, 2)] = de.pc + 4
        elif de.ResultSelect == 4:
            rg.x[int(de.rd, 2)] = de.immU + de.pc

        # with open("output.txt", "a") as f:
        #     f.write(
        #         f"WRITEBACK: write {rg.x[int(de.rd,2)]} to rd = x[{int(de.rd, 2)}]\n\n"
        #     )
        current_instruction = f"write {rg.x[int(de.rd,2)]} to rd = x[{int(de.rd, 2)}]"

    else:
        # with open("output.txt", "a") as f:
        #     f.write(f"WRITEBACK:Can't write to rd = x[{int(de.rd, 2)}]\n\n")
        current_instruction = f"Can't write to rd = x[{int(de.rd, 2)}]"

    # incrementing clock cycle by 1 after the writeback stage is completed
    clk += 1


def init() -> None:
    """Initializes pc to its initial value"""
    global clk, current_instruction
    # initialising clk cycle to 0
    clk = 0
    current_instruction = ""
