# python_unreal_ardupilot

Control a UE5 actor in realtime with Python, Dronekit and/or PyMavlink, and Ardupilot SITL

## Requirements
- Python Unreal TCP Relay: https://github.com/igsxf22/python_unreal_relay

- Dronekit, PyMavlink (MavProxy optional)

- ArduPilot SITL
    - Mission Planner, Docker container, anything you can access with Dronekit or PyMavlink

- Optional: A game model for your aircraft


## Set up
This assumes you know the basics of Unreal Engine, and can start a new project, import custom unreal assets, and are familiar with blueprints

1. `pip install dronekit pymavlink`

> Later versions of Python require a small fix to dronekit:
https://github.com/dronekit/dronekit-python/issues/1132#issuecomment-2203771945

IN WORK
