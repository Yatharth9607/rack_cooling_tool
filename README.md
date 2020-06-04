# rack_cooling_tool
A computational model for calculating airflows, pressures and temperature values inside a rack system

A brief summary of the files in this project is as follows:

1. `rack_app.py`
This contains the GUI of the MDC (Micro Data Center) Rack cooling tool. It is connected to the solver - rack_solver.py

2. `rack_solver.py`
This contains the flow network model as well as steady state and transient solver for the MDC rack model.

## Running the Micro Data Center Cooling Calculator

### Python Dependencies
* `python 3.7`
* `dash 0.43`
* `scipy latest`

`pip install dash==0.43`
`pip install scipy`

### Running on Local host (Windows/Linux)
Run the following command in the current directory through command-line interface
`python rack_app.py`

Or run the `rack_app.py` script through python IDE.

Open following link on web browser:
http://127.0.0.1:8071/

### Executing on webserver
`PORT=8777 python rack_app.py`

Specify a `PORT` to run webserver on. If no port is specified, port 8070 is
used.

### Running on Linux Server 
Run as a background process on a linux server.
`PORT=8777 nohup python rack_app.py &`
