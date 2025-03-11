# Realtime Python and Ardupilot in Unreal Engine 5

Control a UE5 actor in realtime with Python, Dronekit and/or PyMavlink, and Ardupilot SITL

![PreviewGIF](media/preview_sitl_dronekit_unreal.gif)

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

## Set up & Launch
This assumes you know the basics of Unreal Engine, and can start a new project, import custom unreal assets, and are familiar with blueprints

1. `pip install dronekit pymavlink`

    > Later versions of Python require a small fix to dronekit:
    https://github.com/dronekit/dronekit-python/issues/1132#issuecomment-2203771945<br>
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


### Notes

1. Vehicle N, E, -D = Unreal X, Y, Z


### Extra Setup Options
#### Set vehicle origin in Unreal to (0, 0) at runtime, even if the vehicle is already flying around
If you relaunch the Unreal runtime with vehicle already airborne, the vehicle will appear at its local frame distance from home. 

If you don't want to reset the SITL each time you re-launch Unreal, you can make minor changes to `bp_pythonPawn` and negate any distance the vehicle has flown away from home

In UE editor, compare original blueprint with these changes: [Reset offset Blueprint](media/bp_pythonPawn_with_offset_xy.jpg)

> This shows the blueprint for resetting initial x, y but doesn't reset apparent z (vehicle alt). To also reset the z to 0 or another offset at unreal launch, just subtract `location - location_in` with the entire vector and use that value in the `Set Actor Location and Rotation` node 

> Instead of using the vehicle's current position in SITL to set the initial offset, you can also use `get location` node to get the location vector of another actor, like the tcpRelay. This way, you can use the tcpRelay as a new default origin for the vehicle.

> This won't work for rotation, so if you need the vehicle facing a certain heading at start, set the yaw with dronekit, mavlink, etc.

#### Control vehicle with Controller ***in work***
- There's a few ways to do this, but focusing on simplicity and Python, I'll include basic set ups for a generic USB gaming controller and the RadioMaster Pocket using Pygame.
