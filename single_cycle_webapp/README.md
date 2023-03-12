# RISCV-32I-Simulator

Flask App for executing machine code with single cycle processor design. Uses Tailwind CSS

## Prerequisites

Download

- [Node.js](https://nodejs.org/en/)

- [Python](https://www.python.org/downloads/)

## Installation

### Clone the repository

```
git clone https://github.com/Karanraj06/RISCV-32I-Simulator
```

### Change the current working directory to `single_cycle_webapp`

```
cd single_cycle_webapp
```

### Create a Python virtual environment

```
python3 -m venv myenv
```

### Activate the virtual environment

For macOS / Linux

```
source myenv/bin/activate
```

For Windows

```
myenv\Scripts\activate.bat
```

### Install packages listed in `requirements.txt`

```
pip install -r requirements.txt
```

### Install all npm dependencies

```
node install
```

### Build CSS with Tailwind CSS

```
npm run watch-css
```

## Start a local development server for the Flask app

```
python app.py
```

The webapp should be available at http://127.0.0.1:5100