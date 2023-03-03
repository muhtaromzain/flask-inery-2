# INERY Blockchain Todo DApp

## Introduction

A simple application with the ability to add, edit and delete data todo.

### Compile the Smart Contract

Type below commands to generate the WAST & ABI file:

```bash
$ cd todo
$ inery-cpp ./todo.cpp -o ./todo.wasm
```

### Deploy and run the Smart Contract

This includes the source code of the INERY Smart Contract which to simulate a simple contacts list.

```bash
$ cd todo
$ cline set contract YOUR_ACCOUNT_NAME ./
```

## Run the webapp at your Inery node server

In addition to the above prerequisites, you'll need run the requirements to install all the dependencies:

```bash
$ pip install -r REQUIREMENTS.txt
```

### Config and run the app

Before run the app, you'll need to change the env file. you need to rename `.env.example` to `.env` and fill the your credentials there:

```ini
[DEFAULT]
ACCOUNT = you_account_name
PRIVATE_KEY = your_private_key
URL = your_node_server_url
TABLE = your_table_name
```

Start the web server:

```bash
$ python main.py
```

OR

```bash
$ python3 main.py
```

Browse the `http://127.0.0.1:5000/` to run the demo.


### Demo
You can see a demo in [HERE](TBA).