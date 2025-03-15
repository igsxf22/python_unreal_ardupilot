# Realtime Dronekit-Python and Ardupilot for Unreal Engine 5

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

1. Unreal X, Y, Z = Vehicle Local N, E, -D

## Simple Recipes
> Whenever you change the actor that you want to control with Python, make sure you change the `Get Actor of Class` node in the `bp_tcpRelay` event graph to the class of the new actor.

These recipes require the core assets from (https://github.com/igsxf22/python_unreal_relay) though we'll swap out the `bp_pythonPawn` for new blueprints

### Vehicle with Time-of-Flight Height Sensor
 - `examples/simple_tofHeight.py`
 - `vehicles/bp_pythonPawn_tofHeight.uasset`
 - `assets/simple/bp_simpleFloor.uasset`  (*a 10x10 plane that returns Hit events to vehicle line trace*)

Vehicle simulates a tof-sensor fixed (*NOT stabilized*) to the bottom of platform using a line trace aimed down from its local frame, returns distance to first object set to return hits. 
- Default max distance is 1000cm, returns -1 if no hit
 

## Extra Setup Options
### Set vehicle origin in Unreal to (0, 0) at runtime, even if the vehicle has moved
If you want the vehicle to start at a certain origin and don't want to reset the SITL each time you launch Unreal, you can make minor changes to `bp_pythonPawn` and offset any distance the vehicle is away from home. In UE editor, compare current blueprint with these changes: [Reset offset Blueprint](media/bp_pythonPawn_with_offset_xy.jpg). To also ignore vehicle altitude and reset to 0, use `location - location_in` with all three items.

 - Instead of using the vehicle's current position in SITL to set the initial offset, you can also use `get location` node to get the location vector of another actor, like the tcpRelay. This way, you can use the tcpRelay as a new default origin for the vehicle.

> This won't work for rotation, so if you need the vehicle facing a certain heading at start, set the yaw with dronekit, mavlink, etc.

#### Control vehicle with Controller ***in work***
- There's a few ways to do this, but focusing on simplicity and Python, I'll include basic set ups for a generic USB gaming controller and the RadioMaster Pocket using Pygame.
