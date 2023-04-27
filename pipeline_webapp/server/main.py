from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg
import knobs
from collections import OrderedDict
from cache import Cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

word = 0
blocks = 0
associativity = 0
replace = 0
hit = 1
miss = 20

dword = 0
dblocks = 0
dassociativity = 0
dreplace = 0
dhit = 1
dmiss = 20


@app.post("/text")
async def create(request: Request):
    global word, blocks, associativity, replace, hit, miss, dword, dblocks, dassociativity, dreplace, dhit, dmiss
    text = await request.json()

    word = text["word"]
    blocks = text["blocks"]
    associativity = text["associativity"]
    replace = text["replace"]
    hit = text["hit"]
    miss = text["miss"]

    dword = text["dword"]
    dblocks = text["dblocks"]
    dassociativity = text["dassociativity"]
    dreplace = text["dreplace"]
    dhit = text["dhit"]
    dmiss = text["dmiss"]

    fi.i_cache = Cache(
        text["word"],
        text["blocks"],
        text["associativity"],
        text["replace"],
        text["hit"],
        text["miss"],
    )

    ma.d_cache = Cache(
        text["dword"],
        text["dblocks"],
        text["dassociativity"],
        text["dreplace"],
        text["dhit"],
        text["dmiss"],
    )

    knobs.data_forwarding = 1 if text["checked"] else 0
    with open("input.mc", "w") as f:
        f.truncate(0)
        f.write(text["text"])

    try:
        with open("input.mc", "r") as f:
            lines = f.readlines()
            track = 0
            for line in lines:
                key, value = line.split()
                if track == 0:
                    # print(key+" "+value)
                    if value == "_":
                        fi.instruction_memory[int(key, 16)] = None
                        track = 1
                    else:
                        fi.instruction_memory[int(key, 16)] = value
                elif track == 1:
                    print(key + " " + value)
                    ma.update_mem(key, value)
    except:
        return {"success": False}

    with open("output.txt", "w") as f:
        f.truncate(0)

    return {"success": True}


# importing pipeline registers
from pipeline_registers import IF_DE, DE_EX, EX_MA, MA_WB

clk: int = 0
CPI: int = None
current_instruction = [
    fi.current_instruction,
    de.current_instruction,
    ex.current_instruction,
    ma.current_instruction,
    wb.current_instruction,
]
forwarding_paths = [ex.de_forwarding_path, ex.ex_forwarding_path, ex.ma_forwarding_path]
dependencies = [ex.de_dependency, ex.ex_dependency, ex.ma_dependency]
stats = [
    clk,
    wb.total_instructions,
    0,
    ma.data_transfer_instructions,
    ex.alu_instructions,
    ex.control_instructions,
    wb.total_bubbles,
    ex.data_hazard_count,
    ex.control_hazard_count,
    ex.branch_mispredictions,
    ex.data_hazard_stalls,
    ex.control_hazard_stalls,
]

data = {
    "registers": rg.x,
    "memory": OrderedDict(sorted(ma.data_memory.items())),
    "current_instruction": current_instruction,
    "stats": stats,
    "forwarding_paths": forwarding_paths,
    "dependencies": dependencies,
    # "istats": [],
}


def updateData():
    global stats, data, clk, current_instruction, CPI, forwarding_paths, dependencies
    if wb.total_instructions > 0:
        CPI = clk / wb.total_instructions
    else:
        CPI = 0
    current_instruction = [
        fi.current_instruction,
        de.current_instruction,
        ex.current_instruction,
        ma.current_instruction,
        wb.current_instruction,
    ]
    forwarding_paths = [
        ex.de_forwarding_path,
        ex.ex_forwarding_path,
        ex.ma_forwarding_path,
    ]
    dependencies = [ex.de_dependency, ex.ex_dependency, ex.ma_dependency]
    stats = [
        clk,
        wb.total_instructions,
        CPI,
        ma.data_transfer_instructions,
        ex.alu_instructions,
        ex.control_instructions,
        wb.total_bubbles,
        ex.data_hazard_count,
        ex.control_hazard_count,
        ex.branch_mispredictions,
        ex.data_hazard_stalls,
        ex.control_hazard_stalls,
    ]
    data = {
        "registers": rg.x,
        "memory": OrderedDict(sorted(ma.data_memory.items())),
        "current_instruction": current_instruction,
        "stats": stats,
        "forwarding_paths": forwarding_paths,
        "dependencies": dependencies,
    }


def updateRegisterStatus():
    with open("./output/registers_status.txt", "a") as f:
        f.truncate(0)
        f.write("# ========= Register File ===========\n\n")
        track = 0
        for x in rg.x:
            f.write(f"x{track} : {x}\n")
            track += 1


def updateStats():
    global CPI
    CPI = clk / wb.total_instructions

    with open("./output/stats.txt", "a") as f:
        f.truncate(0)
        f.write(f"Total number of cycles: {clk}\n")
        f.write(f"Total instructions executed: {wb.total_instructions}\n")
        f.write(f"CPI: {CPI}\n")
        f.write(
            f"Number of Data-transfer (load and store) instructions executed: {ma.data_transfer_instructions}\n"
        )  #################remaining
        f.write(f"Number of ALU instructions executed: {ex.alu_instructions}\n")
        f.write(f"Number of Control instructions executed: {ex.control_instructions}\n")
        f.write(f"Number of stalls/bubbles in the pipeline: {wb.total_bubbles}\n")
        f.write(f"Number of data hazards: {ex.data_hazard_count}\n")
        f.write(f"Number of control hazards: {ex.control_hazard_count}\n")
        f.write(f"Number of branch mispredictions: {ex.branch_mispredictions}\n")
        f.write(f"Number of stalls due to data hazards: {ex.data_hazard_stalls}\n")
        f.write(
            f"Number of stalls due to control hazards: {ex.control_hazard_stalls}\n"
        )


def print_output():
    print(f"Data Hazard Stalls: {ex.data_hazard_stalls}")
    print(f"Data Hazard Count: {ex.data_hazard_count}")
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


def run() -> None:
    """Executes the program until the end of the instruction memory is reached"""
    global clk
    flag = 1
    while True:
        if flag == 1:
            fi.fetch()
            updateData()
            updateRegisterStatus()
            clk += 1
            print("\n")

            de.decode()
            updateData()
            updateRegisterStatus()
            clk += 1
            print("\n")

            ex.execute()
            updateData()
            updateRegisterStatus()
            clk += 1
            print("\n")

            ma.memory_access()
            updateData()
            updateRegisterStatus()
            clk += 1
            print("\n")

            flag = 0
        if not wb.writeBack():
            break
        updateData()
        updateRegisterStatus()
        clk += 1
        print("\n")
    updateStats()
    print("# =============== Program Execution Successfull. =================")
    print_output()
    print(ma.data_memory)


step_flag = 0


def step() -> bool:
    global step_flag, clk, data
    if step_flag == 0:
        fi.fetch()
        updateData()
        updateRegisterStatus()
        clk += 1
        step_flag += 1
    elif step_flag == 1:
        de.decode()
        updateData()
        updateRegisterStatus()
        clk += 1
        step_flag += 1
    elif step_flag == 2:
        ex.execute()
        updateData()
        updateRegisterStatus()
        clk += 1
        step_flag += 1
    elif step_flag == 3:
        ma.memory_access()
        updateData()
        updateRegisterStatus()
        clk += 1
        step_flag += 1
    else:
        if not wb.writeBack():
            updateStats()
            print("# =============== Program Execution Successfull. =================")
            return False
        updateData()
        updateRegisterStatus()
        clk += 1
    print(data)
    print("\n")
    return True


def reset() -> None:
    global clk, step_flag
    clk = 0
    step_flag = 0
    """Resets to the initial state"""
    fi.init()
    IF_DE.init()
    de.init()
    DE_EX.init()
    ex.init()
    EX_MA.init()
    ma.init()
    MA_WB.init()
    wb.init()
    rg.init()
    with open("output.txt", "w") as f:
        f.truncate(0)


@app.get("/data")
async def root():
    data["istats"] = [
        fi.i_cache.block_size,
        fi.i_cache.cache_size,
        fi.i_cache.sets,
        fi.i_cache.accesses,
        fi.i_cache.hits,
        fi.i_cache.misses,
        fi.i_cache.cold_misses,
        fi.i_cache.capacity_misses,
        fi.i_cache.conflict_misses,
        fi.i_cache.memory_stalls,
        list(fi.i_cache.prev_address),
        list(fi.i_cache.prev_victim),
    ]
    data["i_cache"] = fi.i_cache.cache
    data["d_cache"] = ma.d_cache.cache
    data["dstats"] = [
        ma.d_cache.block_size,
        ma.d_cache.cache_size,
        ma.d_cache.sets,
        ma.d_cache.accesses,
        ma.d_cache.hits,
        ma.d_cache.misses,
        ma.d_cache.cold_misses,
        ma.d_cache.capacity_misses,
        ma.d_cache.conflict_misses,
        ma.d_cache.memory_stalls,
        list(ma.d_cache.prev_address),
        list(ma.d_cache.prev_victim),
    ]
    return data


@app.get("/run")
def run_simulator():
    try:
        reset_simulator()
        run()
        updateData()
    except:
        return {"success": False}
    return {"success": True}


@app.get("/step")
def step_simulator():
    try:
        if not step():
            print_output()
        updateData()
    except:
        return {"success": False}
    return {"success": True}


@app.get("/reset")
def reset_simulator():
    try:
        global clk, step_flag, word, blocks, associativity, replace, hit, miss, dword, dblocks, dassociativity, dreplace, dhit, dmiss
        clk, step_flag = 0, 0
        wb.total_instructions = 0
        ma.data_transfer_instructions = 0
        ex.alu_instructions = 0
        ex.control_instructions = 0
        wb.total_bubbles = 0
        ex.data_hazard_count = 0
        ex.control_hazard_count = 0
        ex.branch_mispredictions = 0
        ex.data_hazard_stalls = 0
        ex.control_hazard_stalls = 0
        ex.de_forwarding_path = ""
        ex.ex_forwarding_path = ""
        ex.ma_forwarding_path = ""
        ex.de_dependency = ""
        ex.ex_dependency = ""
        ex.ma_dependency = ""
        fi.i_cache = Cache(word, blocks, associativity, replace, hit, miss)
        ma.d_cache = Cache(dword, dblocks, dassociativity, dreplace, dhit, dmiss)
        reset()
        updateData()

        with open("input.mc", "r") as f:
            lines = f.readlines()
            track = 0
            for line in lines:
                key, value = line.split()
                if track == 0:
                    # print(key+" "+value)
                    if value == "_":
                        fi.instruction_memory[int(key, 16)] = None
                        track = 1
                    else:
                        fi.instruction_memory[int(key, 16)] = value
                elif track == 1:
                    print(key + " " + value)
                    ma.update_mem(key, value)
    except:
        return {"success": False}
    return {"success": True}


@app.get("/cache")
async def root():
    return {"i_cache": fi.i_cache.cache, "d_cache": ma.d_cache.cache}
