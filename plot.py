import plotly.express as px
import pandas as pd

# Read the data from the "data.csv" file into a Pandas DataFrame
data = pd.read_csv("data.csv")

# Read the airport data from the "GlobalAirportDatabase.csv" file into a Pandas DataFrame
airports = pd.read_csv("GlobalAirportDatabase.csv", header=None)

# Calculate the minimum and maximum values of longitude and latitude
lon_min = data["Longitude"].min()
lon_max = data["Longitude"].max()
lat_min = data["Latitude"].min()
lat_max = data["Latitude"].max()

# Calculate the center latitude and longitude
lat_center = (lat_min + lat_max) / 2
lon_center = (lon_min + lon_max) / 2

# Give the columns of the airport data meaningful names
airports.columns = ["Name1", "Name2", "Name3", "Name4", "Name5", "Latitude", "Longitude"]

# Create a scatter plot of the airports using Plotly Express
fig = px.scatter_mapbox(airports, text="Name1", lat="Latitude", lon="Longitude", hover_name="Name3",
                        color_discrete_sequence=["fuchsia"], zoom=10, height=600,
                        center={"lat": lat_center, "lon": lon_center})

# Add a line trace to the plot to represent the flight route
fig.add_scattermapbox(
    mode="text+lines",  # Add both text labels and lines to the trace
    lat=data['Latitude'],  # Latitude values
    lon=data['Longitude'],  # Longitude values
    text=data['Time'],  # Text labels
    connectgaps=False,  # Connect the points in the line trace with lines
    showlegend=False  # Do not show a legend for this trace
)

# Select only the rows in the DataFrame where the "On Ground" column is equal to True
df_on_ground = data[data["On Ground"] == True]

# Add a scatter mapbox trace for the locations where the flight was on the ground
fig.add_scattermapbox(
    lat=df_on_ground["Latitude"],  # Latitude values
    lon=df_on_ground["Longitude"],  # Longitude values
    mode="markers",  # Show markers instead of lines
    marker=dict(
        color="green",  # Set marker color to green
        size=10,  # Set marker size to 10
        opacity=0.7  # Set marker opacity to 0.7
    ),
    showlegend=False  # Do not show a legend for this trace
)

# Set the mapbox style to "open-street-map"
fig.update_layout(mapbox_style="open-street-map")

# Remove the margins around the plot
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.show()
