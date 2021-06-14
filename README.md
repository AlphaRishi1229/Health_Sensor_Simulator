# Health_Sensor_Simulator
This python project simulates the working of a health wearable sensor.

Process to execute the code:
1) Create a virtual environment `python3 -m venv env`
2) Activate the virtual environment by `source env/bin/activate`
3) Install dependency requirements by `pip install -r requirements.txt`
4) Execute the main file as `python3 main.py`
5) Input the user name.
6) Input the time for simulation to run in minutes.
7) At the end it will ask for generation of a hourly report. Enter Y if you want to generate.

Notes:
1) To change the default simulation time change values in constants.py
2) `TIMER_DURATION` will be the interval for the function to be called.
3) `DEFAULT_SIMULATION_MINUTES` is the default value for simulation to run i.e. 2 hours.
4) `SEGMENTED_SECONDS` is the value in which we divide the report in 15 minute segments.
5) `HOURLY_SECONDS` is the value for hourly reports.
