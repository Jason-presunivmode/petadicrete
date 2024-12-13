import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import pydeck as pdk
from city_data import provinces_data  # Import the city data

# Apply custom CSS for larger sidebar buttons
st.markdown(
    """
    <style>
    .css-1v3fvcr { font-size: 20px !important; }
    .css-1v3fvcr span { font-size: 20px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Page 1: Profile Page ---
def profile_page():
    st.title("Profile Page")
    st.subheader("Team Members")

    # Display 3 image slots with names below them
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://raw.githubusercontent.com/Jason-presunivmode/petadicrete/refs/heads/main/Guest3.jpg", caption="Person 1", use_column_width=True)
        st.text("Jason Matthew Pham")

    with col2:
        st.image("https://raw.githubusercontent.com/Jason-presunivmode/petadicrete/refs/heads/main/Guest2.jpg", caption="Person 2", use_column_width=True)
        st.text("Risma Choerunnisa")

    with col3:
        st.image("https://raw.githubusercontent.com/Jason-presunivmode/petadicrete/refs/heads/main/Guest1.jpg", caption="Person 3", use_column_width=True)
        st.text("Bunga Aulia")


# --- Page 2: Graph Visualization ---
def graph_visualization_page():
    st.title("Graph Visualization with Streamlit")

    # User inputs
    num_nodes = st.number_input("Enter the number of nodes:", min_value=2, value=5, step=1)
    num_edges = st.number_input("Enter the number of edges:", min_value=1, value=4, step=1)

    if num_edges > (num_nodes * (num_nodes - 1)) // 2:
        st.warning("Too many edges for the given number of nodes. Adjust the input.")
    else:
        # Create a random graph
        G = nx.Graph()
        G.add_nodes_from(range(1, num_nodes + 1))

        # Add random edges
        edges = set()
        while len(edges) < num_edges:
            u = random.randint(1, num_nodes)
            v = random.randint(1, num_nodes)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        G.add_edges_from(edges)

        # Draw the graph
        plt.figure(figsize=(8, 6))
        nx.draw(
            G,
            with_labels=True,
            node_color="skyblue",
            node_size=2000,
            font_size=10,
            font_weight="bold",
            edge_color="gray"
        )
        plt.title("Randomly Generated Graph")

        # Display the graph
        st.pyplot(plt)


# --- Page 3: Province Map Visualization ---
def map_visualization_page():
    st.title("Province Map Visualization")
    
    # Select a province
    province_name = st.selectbox("Select a Province", list(provinces_data.keys()))
    if province_name:
        cities = provinces_data[province_name]
        all_cities = [city["name"] for city in cities]

        # Multiselect for cities
        selected_cities = st.multiselect("Select Cities to Show", all_cities, default=all_cities)

        # Generate button to create the map
        if st.button("Generate Map"):
            if selected_cities:
                # Filter selected cities
                cities_df = pd.DataFrame([city for city in cities if city["name"] in selected_cities])

                # Generate connections between selected cities
                connections = []
                for i, city1 in cities_df.iterrows():
                    for j, city2 in cities_df.iterrows():
                        if i < j:
                            connections.append({
                                "start_lat": city1["lat"],
                                "start_lon": city1["lon"],
                                "end_lat": city2["lat"],
                                "end_lon": city2["lon"],
                            })
                connections_df = pd.DataFrame(connections)

                # Render the map
                st.pydeck_chart(
                    pdk.Deck(
                        map_style="mapbox://styles/mapbox/streets-v11",
                        initial_view_state=pdk.ViewState(
                            latitude=cities_df["lat"].mean(),
                            longitude=cities_df["lon"].mean(),
                            zoom=8,
                        ),
                        layers=[
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=cities_df,
                                get_position="[lon, lat]",
                                get_color="[200, 30, 30, 160]",
                                get_radius=1500,
                            ),
                            pdk.Layer(
                                "LineLayer",
                                data=connections_df,
                                get_source_position=["start_lon", "start_lat"],
                                get_target_position=["end_lon", "end_lat"],
                                get_color="[50, 50, 200, 150]",
                                get_width=2,
                            ),
                        ],
                    )
                )
            else:
                st.warning("Please select at least one city to generate the map.")


# --- Page Navigation ---
st.sidebar.title("Navigation")
pages = {
    "Profile Page": profile_page,
    "Graph Visualization": graph_visualization_page,
    "Map Visualization": map_visualization_page,
}

# Sidebar for selecting a page
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Render the selected page
pages[selected_page]()
