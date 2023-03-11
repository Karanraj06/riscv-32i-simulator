from flask import Flask, render_template, request, jsonify

import instruction_fetch as fi
import decode as de
import execute as ex
import memory_access as ma
import write_back as wb
import registers as rg

from collections import OrderedDict

app = Flask(__name__)



@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def input_machine_code():
    if request.method == 'POST':
        with open("input.mc", "w") as f:
            f.truncate(0)
            f.write(request.json['machineCode'])
        
        with open("input.mc", "r") as f:
            while True:
                key, value = f.readline().split()

                if value == "_":
                    fi.instruction_memory[int(key, 16)] = None
                    break
                else:
                    fi.instruction_memory[int(key, 16)] = value
        
    return render_template("index.html")

@app.route("/data")
def get_data():
    current_instruction = [fi.current_instruction, de.current_instruction, ex.current_instruction, ma.current_instruction, wb.current_instruction]
    return jsonify({
        "clock": wb.clk,
        "registers": rg.x,
        "memory": OrderedDict(sorted(ma.data_memory.items())),
        "current_instruction": current_instruction
    })

def run() -> None:
    '''Executes the program until the end of the instruction memory is reached'''
    while(step()):
        continue



def step() -> None:
    '''Executes one instruction'''
    if (not fi.fetch()):
        de.decode()
        ex.execute()
        ma.memory_access()
        wb.writeBack()
        return True
    return False


def reset() -> None:
    '''Resets to the initial state'''
    fi.init()
    de.init()
    ex.init()
    ma.init()
    wb.init()
    rg.init()
    with open("input.mc", "w") as f:
        f.truncate(0)

@app.route('/run')
def run_simulator():
    run()
    return jsonify({'success': True})

@app.route('/step')
def step_simulator():
    step()
    return jsonify({'success': True})

@app.route('/reset')
def reset_simulator():
    reset()
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True, port=5001)