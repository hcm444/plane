import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the Haversine distance between two points on a sphere

    Parameters:
    lat1 (float): Latitude coordinate of the first point in degrees
    lon1 (float): Longitude coordinate of the first point in degrees
    lat2 (float): Latitude coordinate of the second point in degrees
    lon2 (float): Longitude coordinate of the second point in degrees

    Returns:
    float: Haversine distance in kilometers between the two points on the sphere
    """
    # Earth's radius in km
    R = 6371

    # Difference between the latitudes of the two points in radians
    d_lat = math.radians(lat2 - lat1)

    # Difference between the longitudes of the two points in radians
    d_lon = math.radians(lon2 - lon1)

    # Compute intermediate value 'a' using the Haversine formula
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
        d_lon / 2) ** 2

    # Compute intermediate value 'c' using the Haversine formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Compute the Haversine distance 'd'
    d = R * c

    # Return the Haversine distance
    return d
