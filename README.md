# rack_cooling_tool
A computational model for calculating airflows, pressures and temperature values inside a rack system

A brief summary of the files in this project is as follows:

1. Rack_App.py
This contains the GUI of the MDC Rack cooling tool. It is connected to the solver - Rack_solver.py

2. Rack_solver.py
This contains the flow network model as well as steady state and transient solver for the MDC rack model.

## Running the Micro Data Center Cooling Calculator

### Python Dependencies
* `python 3.7`
* `dash 0.43`
* `scipy latest`

`pip install dash==0.43`
`pip install scipy`

### Executing
`PORT=8777 python Rack_App.py`

Specify a `PORT` to run webserver on. If no port is specified, port 8070 is
used.


### Running On Linux Server 
Run as a background process on a linux server.
`PORT=8777 nohup python Rack_App.py &`
