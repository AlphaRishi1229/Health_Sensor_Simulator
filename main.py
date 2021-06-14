"""The main file to be executed. This will start the simulator and process the data."""
from constants import DEFAULT_SIMULATION_MINUTES
from processors.sensor_simulator import Sensor_Simulator


user_name = str(input("Enter the name of the user: "))
total_time = int(input("Enter the time for simulation to run in minutes (default: 120): ")) or DEFAULT_SIMULATION_MINUTES

a = Sensor_Simulator(user_name, total_time)
a.start_simulation()
