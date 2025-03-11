# Realtime Python and Ardupilot in Unreal Engine 5

Control a UE5 actor in realtime with Python, Dronekit and/or PyMavlink, and Ardupilot SITL

## Requirements
- Python Unreal TCP Relay: https://github.com/igsxf22/python_unreal_relay

- Dronekit, PyMavlink (MavProxy optional)

- ArduPilot SITL
    - Mission Planner, Docker container, anything you can access with Dronekit or PyMavlink

- Optional: A game model for your aircraft


### Successfully tested 11 Mar 25 with:
- Windows 11
- Unreal Engine 5.5.3
- Python 3.11
- MissionPlanner 1.3.82
    - Stable MultiCopter sim
    - Stable Plane sim

## Set up
This assumes you know the basics of Unreal Engine, and can start a new project, import custom unreal assets, and are familiar with blueprints

1. `pip install dronekit pymavlink`

    > Later versions of Python require a small fix to dronekit:
    https://github.com/dronekit/dronekit-python/issues/1132#issuecomment-2203771945
    > Fix is built into the basic example in this repo

2. Follow the instructions in the https://github.com/igsxf22/python_unreal_relay to download and enable the TCP plugin for Unreal and the sample tcpRelay and pythonPawn actors. 
    > I suggest running the tcp_relay.py script in that repo to make sure you're tcpRelay and pythonPawn are connecting

    > This project uses the local frame of the vehicle (meters from home position), and not geographic coordinates, but there is a geo coordinate system plugin for Unreal

3. Start your SITL instance
    > You can use the Mission Planner simulation tab to launch a SITL instance for Copter
    > The `sitl_dronekit_to_unreal.py` is set to connect to the Mission Planner SITL on `tcp:127.0.0.1:5763`

4. Launch `sitl_dronekit_to_unreal.py`

5. Launch Unreal Engine Play-in-Editor

6. Control your vehicle in Mission Planner and watch it fly around in Unreal
