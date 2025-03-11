# Fix for the error: AttributeError: module 'collections' has no attribute 'MutableMapping'
from collections import abc
import collections
collections.MutableMapping = abc.MutableMapping

import time
import math

from dronekit import connect, VehicleMode, Vehicle, LocationGlobalRelative

import tcp_relay

"""
SITL Dronekit to Unreal Engine - Basic Example
This script connects to a SITL instance using Dronekit and sends vehicle data to Unreal Engine using a TCP relay.
The basic example is configured to match the bp_pythonPawn example in the Unreal Engine project: 
    https://github.com/igsxf22/python_unreal_relay
"""

# Dronekit
connection_string = 'tcp:127.0.0.1:5763'
vehicle = connect(connection_string, wait_ready=True, baud=57600, rate=60)
print("Vehicle Connected.")

relay = tcp_relay.TCP_Relay()

def vehicle_to_unreal(vehicle, z_invert=True, scale=100):
    """
    Converts vehicle data to a dictionary and formats it for Unreal Engine.
    :param vehicle: The vehicle object from dronekit.
    :param z_invert: Invert the Z axis for local frame (default is True because Ardupilot uses NED).
    :param scale: The scale of the Unreal Engine world (default is 100, UE uses cm).
    """
    d = {}
    d["lat"] = vehicle.location.global_frame.lat
    d["lon"] = vehicle.location.global_frame.lon
    d["alt"] = vehicle.location.global_frame.alt
    d["n"] = vehicle.location.local_frame.north * scale
    d["e"] = vehicle.location.local_frame.east * scale
    d["d"] = vehicle.location.local_frame.down * scale
    if z_invert:
        d["d"] *= -1
    d["roll"] = vehicle.attitude.roll
    d["pitch"] = vehicle.attitude.pitch
    d["yaw"] = vehicle.attitude.yaw

    # Round based on required precision
    for k,v in d.items():
        if type(v) == float:
            if k in ["lat", "lon", "alt"]:
                d[k] = round(v, 8)
            elif k in ["n", "e", "d"]:
                d[k] = round(v, 3)
            elif k in ["roll", "pitch", "yaw"]:
                d[k] = round(math.degrees(v), 3)

    return d


while True:

    # Send vehicle data to Unreal Engine
    data = vehicle_to_unreal(vehicle)

    # Create a blank list of fields
    fields = [0.] * relay.num_fields

    # Set location and rotation fields with vehicle local frame and attitude data
    fields[0] = data["n"]
    fields[1] = data["e"]
    fields[2] = data["d"]
    fields[3] = data["roll"]
    fields[4] = data["pitch"]
    fields[5] = data["yaw"]

    # Update the relay message with from the fields, relay will send this to Unreal Engine in its thread
    relay.message = tcp_relay.create_fields_string(fields)
    
    time.sleep(1/60)