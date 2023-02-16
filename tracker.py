import opensky_api
import argparse
import time
import csv
import ctypes
from get_nearest_airport import get_nearest_airport


# Load the shared library
mylib = ctypes.CDLL('./lib_get_current_time.so')

# Define the argument types and return type of the function
mylib.get_current_time.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
mylib.get_current_time.restype = None

# Create a buffer to hold the time string
time_string = ctypes.create_string_buffer(20)

# Call the C function to get the current time
mylib.get_current_time(time_string, len(time_string))

def get_aircraft_info(icao24, username="Henry", password="123456"):
    # Create an instance of the OpenSkyApi class with the provided username and password
    api = opensky_api.OpenSkyApi(username=username, password=password)

    # Convert the input icao24 to lowercase
    icao24 = icao24.lower()

    # Get the states for the aircraft with the specified icao24 identifier
    states = api.get_states(icao24=icao24)

    # Check if there are any states returned
    if states.states:
        # If there are states, select the first one
        sv = states.states[0]
        # Return the state information as a dictionary
        if sv.latitude is not None and sv.longitude is not None:
            nearest = get_nearest_airport(sv.latitude, sv.longitude)
        if sv.geo_altitude is None and sv.on_ground is True:
            sv.geo_altitude = 0
        data_row = [time_string.value.decode(), sv.latitude, sv.longitude, sv.geo_altitude, sv.on_ground,
                    sv.velocity, sv.true_track, nearest[2], nearest[5]]
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data_row)
            csvfile.close()
        return [
            sv.icao24,
            # Unique identifier for the aircraft
            sv.callsign,
            # Callsign of the aircraft
            sv.latitude,
            # Latitude of the aircraft's current position
            sv.longitude,
            # Longitude of the aircraft's current position
            sv.geo_altitude,
            # Altitude above sea level in meters
            sv.on_ground,
            # Boolean indicating whether the aircraft is on the ground or not
            sv.velocity,
            # Velocity of the aircraft in meters per second
            sv.true_track,
            # Heading of the aircraft in degrees from North
            nearest[2],
            # Nearest Airport
            nearest[5]
            # Distance in kilometers
        ]
    else:
        # If there are no states returned, return None
        return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get information about an aircraft from the OpenSky API')
    parser.add_argument('icao24', type=str, help='The ICAO24 identifier for the aircraft')
    args = parser.parse_args()
    filename = "data.csv"
    fields = ["Time",
              "Latitude",
              "Longitude",
              "Geo Altitude",
              "On Ground",
              "Velocity",
              "True Track",
              "Nearest Airport",
              "Nearest Airport Distance"]
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvfile.close()
status = None
last_status = None
not_airport = None
last_below = None
last_on_ground = None
counter = 0
on_ground = None
below = None
# Infinite loop to keep checking the aircraft information
while True:
    # Counter to keep track of the iteration
    counter += 1
    # Get the information of the aircraft using the provided function
    output = (get_aircraft_info(args.icao24))
    # Initialize the below and on_ground variables
    # Check if the output of the function is not None
    if output is not None:
        # Set the status to True if the output is not None
        status = True
        # Print the information of the aircraft
        print("======", counter, "================================================================")
        print("ICAO: ", output[0])
        print("Callsign: ", output[1])
        print("Latitude: ", output[2])
        print("Longitude: ", output[3])
        print("Altitude: ", output[4])
        print("On Ground: ", output[5])
        print("Velocity: ", output[6])
        print("True Track: ", output[7])
        print("Nearest Airport: ", output[8])
        print("Nearest Airport Distance: ", output[9])
    else:
        # Set the status to False if the output is None
        status = False
        # Print a message indicating that there is no aircraft data
        print("No Aircraft Data")
    # Check if the status is True
    if status:
        if (output[5]) is not None:
            on_ground = (output[5])
        # Check if the aircraft is on the ground
        # Check if the distance to the nearest airport is less than 5
        if (output[8]) is not None:
            airport = output[8]
        if (output[9]) is not None:
            if float(output[9]) < 12:
                not_airport = False
            else:
                not_airport = True
        # Check if the altitude of the aircraft is below 1500
        if (output[4]) is not None:
            if float(output[4]) < 1500:
                below = True
            else:
                below = False
    # Landing
    if not_airport is False and below and on_ground is False and (
                (last_status is False and status) or (last_on_ground)):
        print("Took off from", airport)
    # Takeoff
    if last_below and not_airport is False and ((last_status and status is False and last_on_ground is False) or (
                on_ground and last_on_ground is False)):
        print("Landed at", airport)
    last_status = status
    last_on_ground = on_ground
    last_below = below
    # Store the current status, on_ground and below values for the next iteration
    time.sleep(120)