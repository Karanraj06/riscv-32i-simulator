# RISCV-32I-Simulator

FastAPI and React project for executing machine code with pipeline execution

## Prerequisites

Download

- [Node.js](https://nodejs.org/en/)

- [Python](https://www.python.org/downloads/)

## Install and Run Locally

### Clone the repository

```
git clone https://github.com/Karanraj06/RISCV-32I-Simulator
```

### Change the current working directory to `pipeline_webapp/server`

```
cd pipeline_webapp/server
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

### Run the FastAPI Server with Uvicorn

```
uvicorn main:app --reload
```
### Now change the current working directory to `pipeline_webapp/client`

### Install all npm dependencies

```
npm install
```

### Start a local development server for the React app

```
npm run dev
```

The webapp should be available at http://127.0.0.1:5173