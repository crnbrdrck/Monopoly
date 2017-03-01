# Monopoly
Monopoly project for Computer Science 3rd Year

# Installation Instructions
1. Install Python >= 3.4 if you haven't already
  - [Downloads](https://www.python.org/downloads/)
2. Download the source code
  - [ZIP Archive](https://github.com/crnbrdrck/Monopoly/archive/master.zip)
3. Use pip to install all necessary requirements
  - `python3 -m pip -r requirements.txt`

# Running The Game
For ease, we have split the Client and Server into 2 separate modules.
To run the game, navigate to the folder you extracted the code into
  - This folder should contain both the Client and Server folders
  
To run:

- Client
  ```bash
python3 -m Client
```

- Server
  ```bash
python3 -m Server
```

For more details about running the Server, see [here](Server#running-server-module)

## Running Both Parts on one machine
If you wish to run both parts at the same time, you can have 2 terminal windows open and run one command in each, or use the following:

- Windows
  ```bash
    start python3 -m Server
    python3 -m Client
  ```

- Linux
  ```bash
    python3 -m Server &
    python3 -m Client
  ```
