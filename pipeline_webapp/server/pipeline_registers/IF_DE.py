instruction: str = None
pc: int = None

nop: int = 0


def init() -> None:
    global instruction, pc, nop
    (instruction, pc, nop) = (None, None, None)
