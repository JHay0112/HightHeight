'''
    Generate plot of observation sites
'''

# - Imports

import folium
from process import load_data

# - Main

if __name__ == "__main__":

    # Get observation data
    observations = load_data("observations.csv")

    # Create folium map at UC
    map = folium.Map(location = [-43.52253, 172.58043], tiles = "OpenStreetMap", zoom_start = 17)

    # Add observations
    for name, obsv in observations.items():
        # Hacky way of adding labels
        folium.Marker(
            location = obsv.latlong,
            icon = folium.DivIcon(
                icon_size = (30, 30),
                icon_anchor = (10, 30),
                html = f"""
                            <svg viewbox="0 0 80 100">
                                <path d="M40 99.5 C-22.5 57.5 0 0 40 0.5 C80 0 102.5 57.5 40 99.5z" stroke-width="1" stroke="black" fill="white"/>
                            </svg>
                            <div style='font-size: 12pt; color: black; text-align: center; position: relative; top: -40px'>{name}</div>
                        """,
            )
        ).add_to(map)

    # Save map
    map.save("map.html")