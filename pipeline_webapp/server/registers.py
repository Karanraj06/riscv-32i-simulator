# Register File
x: list[int] = [0] * 32
x[2] = 0x7FFFFFFC  # Stack Pointer: Stack segment starts at 0x7FFFFFFC
x[3] = 0x10000000  # Global Pointer: Global segment starts at 0x10000000


def init():
    """Initializes the register file to its initial state"""
    global x

    x = [0] * 32
    x[2] = 0x7FFFFFFC
    x[3] = 0x10000000
    