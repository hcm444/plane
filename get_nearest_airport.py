import csv
import ctypes

# Load the shared library
libhaversine = ctypes.cdll.LoadLibrary('./lib_haversine.so')

# Declare the argument and return types of the function
libhaversine.haversine.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libhaversine.haversine.restype = ctypes.c_double


def get_nearest_airport(lat, lon):
    """
    Returns the name of the nearest airport to the given latitude and longitude
    """
    nearest_distance = float("inf")
    with open("GlobalAirportDatabase.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            airport_lat = float(row[-2])
            airport_lon = float(row[-1])
            dist = libhaversine.haversine(lat, lon, airport_lat, airport_lon)
            if dist < nearest_distance:
                nearest_distance = float(dist)
                nearest_airport_icao = row[0]
                nearest_airport_iata = row[1]
                nearest_airport_name = row[2]
                nearest_airport_city = row[3]
                nearest_airport_country = row[4]
                nearest_airport_lat = float(row[-2])
                nearest_airport_lon = float(row[-1])
    return nearest_airport_icao, nearest_airport_iata, \
        nearest_airport_name, nearest_airport_city, nearest_airport_country, \
        '{:.2f}'.format(nearest_distance), nearest_airport_lat, nearest_airport_lon
