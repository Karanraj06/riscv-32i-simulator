// Editor
let machineCodeEditor = document.getElementById('machine_code_editor');

// Save Button
let saveButton = document.getElementById('save_button');

saveButton.addEventListener('click', () => {
  let machineCode = machineCodeEditor.value;

  // Send the machine code to the Flask app using fetch
  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ machineCode: machineCode }),
  });
});

let intToHex32 = value => {
  let isNegative = value < 0;
  let absValue = isNegative ? -value : value;
  let hexValue = absValue.toString(16).padStart(8, '0');
  if (isNegative) {
    let twosCompValue = (~parseInt(hexValue, 16) + 1) & 0xffffffff;
    hexValue = twosCompValue.toString(16).padStart(8, '0');
  }
  return '0x' + hexValue.toUpperCase();
};

let binToHex32 = binString => {
  let isNegative = binString[0] === '1';
  let binValue = parseInt(binString, 2);
  if (isNegative) {
    binValue = (~binValue + 1) & 0xffffffff;
  }
  let hexValue = binValue.toString(16).padStart(8, '0');
  return '0x' + hexValue.toUpperCase();
};

let binToDec32 = binString => {
  let isNegative = binString[0] === '1';
  let binValue = parseInt(binString, 2);
  if (isNegative) {
    binValue = ~binValue + 1;
  }
  return binValue;
};

setInterval(() => {
  fetch('/data')
    .then(response => response.json())
    .then(data => {
      let clock_cycles = document.getElementById('clock_cycles');
      clock_cycles.innerHTML = data.clock;

      let registers = document.getElementById('registers');
      registers.innerHTML = '';
      for (let i = 0; i < data.registers.length; i++) {
        registers.innerHTML += `<div class="flex justify-evenly font-mono">
                <div>x${i}</div>
                <div
                    class="border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400"
                >
                    ${intToHex32(data.registers[i])}
                </div>
                <div
                    class="border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400"
                >
                    ${data.registers[i]}
                </div>
            </div>`;
      }

      document.getElementById('instruction_fetch').innerHTML =
        data.current_instruction[0];
      document.getElementById('decode').innerHTML = data.current_instruction[1];
      document.getElementById('execute').innerHTML =
        data.current_instruction[2];
      document.getElementById('memory_access').innerHTML =
        data.current_instruction[3];
      document.getElementById('write_back').innerHTML =
        data.current_instruction[4];

      let memory = document.getElementById('memory');
      memory.innerHTML = '';
      for (let i = 0; i < Object.keys(data.memory).length; i++) {
        // let address = Object.keys(data.data_memory)[i];
        // document.querySelector(`#mem-${address}`).textContent =
        //     data.data_memory[address];
        memory.innerHTML += `<div class="flex justify-evenly font-mono">
                <div>${intToHex32(
                  Number.parseInt(Object.keys(data.memory)[i])
                )}</div>
                <div
                    class="border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400"
                >
                    ${binToHex32(data.memory[Object.keys(data.memory)[i]])}
                </div>
                <div
                    class="border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400"
                >
                    ${binToDec32(data.memory[Object.keys(data.memory)[i]])}
                </div>
            </div>`;
      }
    });
}, 100);

let runButton = document.getElementById('run_button');
let stepButton = document.getElementById('step_button');
let resetButton = document.getElementById('reset_button');

runButton.addEventListener('click', () => {
  fetch('/run')
    .then(response => response.json())
    .then(data => {
      if (!data.success) {
        alert('Invalid Machine Code');
      }
    })
    .catch(error => {
      alert('Invalid Machine Code');
    });
});

stepButton.addEventListener('click', () => {
  fetch('/step')
    .then(response => response.json())
    .then(data => {
      if (!data.success) {
        alert('Invalid Machine Code');
      }
    })
    .catch(error => {
      alert('Invalid Machine Code');
    });
});

resetButton.addEventListener('click', () => {
  fetch('/reset')
    .then(response => response.json())
    .then(data => {
      if (!data.success) {
        alert('Invalid Machine Code');
      }
    })
    .catch(error => {
      alert('Invalid Machine Code');
    });
});
