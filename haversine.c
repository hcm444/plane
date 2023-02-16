#include <math.h>

double haversine(double lat1, double lon1, double lat2, double lon2) {
    // Earth's radius in km
    const double R = 6371.0;

    // Convert latitudes and longitudes from degrees to radians
    const double lat1_rad = lat1 * M_PI / 180.0;
    const double lon1_rad = lon1 * M_PI / 180.0;
    const double lat2_rad = lat2 * M_PI / 180.0;
    const double lon2_rad = lon2 * M_PI / 180.0;

    // Calculate differences in latitude and longitude in radians
    const double d_lat = lat2_rad - lat1_rad;
    const double d_lon = lon2_rad - lon1_rad;

    // Calculate intermediate value 'a' using the Haversine formula
    const double a = pow(sin(d_lat / 2), 2) + cos(lat1_rad) * cos(lat2_rad) * pow(sin(d_lon / 2), 2);

    // Calculate intermediate value 'c' using the Haversine formula
    const double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    // Calculate the Haversine distance 'd'
    const double d = R * c;

    // Return the Haversine distance
    return d;
}