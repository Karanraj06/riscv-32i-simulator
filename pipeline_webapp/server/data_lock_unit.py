import instruction_fetch as fi
import decode as de
from pipeline_registers import IF_DE as reg


def stall() -> None:
    fi.init()
    de.init()
    de.nop = 1
    fi.nop = 1
    reg.instruction = None
    reg.pc = None
    reg.nop = 1
