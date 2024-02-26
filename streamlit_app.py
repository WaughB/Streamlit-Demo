import streamlit as st
import pandas as pd
import pydeck as pdk


# Function to load data
def load_data():
    # Load the Excel file
    df = pd.read_excel("dominos_locations_expanded_mock_data.xlsx")
    return df


# Calculate summary statistics (this will be replaced with actual calculations based on your data)
def calculate_summary_statistics(df):
    # Placeholder for summary statistics calculation
    # Replace with actual calculations
    return {
        "Total Locations": len(df),
        "Countries Represented": df["Country"].nunique(),
        "Average Number of Employees": df["Number of Employees"].mean(),
    }


# Home Page
def home_page():
    st.title("Domino's Locations Worldwide")

    st.write(
        """
    ## Overview
    This application provides an interactive way to explore data on Domino's Pizza locations around the globe. 
    Users can view detailed information on each location, including city, state, country, number of employees, 
    and date of opening. Additionally, the app offers visualizations such as maps and charts to better understand 
    the distribution and characteristics of Domino's locations.
    
    ## How to Navigate
    Use the sidebar to navigate between different pages of the application:
    - **Home**: Overview of the project and global summary statistics.
    - **Data Exploration**: Interactive table with search and filter capabilities.
    
    ## Summary Statistics
    """
    )

    # Load data
    df = load_data()

    # Calculate summary statistics
    summary_statistics = calculate_summary_statistics(df)

    # Display summary statistics
    for key, value in summary_statistics.items():
        st.write(f"**{key}**: {value}")


def data_exploration_page(df):
    st.title("Data Exploration")

    # Place filters at the top of the page
    city = st.multiselect("City", options=sorted(df["City"].unique()), default=None)
    state = st.multiselect("State", options=sorted(df["State"].unique()), default=None)

    # Apply filters
    if city and state:  # Ensure at least one filter is applied
        filtered_df = df[df["City"].isin(city) & df["State"].isin(state)]
    elif city:  # Only city filter is applied
        filtered_df = df[df["City"].isin(city)]
    elif state:  # Only state filter is applied
        filtered_df = df[df["State"].isin(state)]
    else:  # No filter is applied
        filtered_df = df

    # Display the filtered dataframe
    st.dataframe(filtered_df)

    # Download link for the filtered dataframe
    def convert_df_to_csv(download_df):
        return download_df.to_csv().encode("utf-8")

    csv = convert_df_to_csv(filtered_df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv",
    )


# This function can be added to your existing Streamlit app code
def map_visualization_page(df):
    st.title("Map Visualization of Domino's Locations")

    # Define filters
    city = st.multiselect("City", options=sorted(df["City"].unique()), default=None)
    state = st.multiselect("State", options=sorted(df["State"].unique()), default=None)
    country = st.multiselect(
        "Country", options=sorted(df["Country"].unique()), default=None
    )

    # Apply filters
    filtered_df = df
    if city:
        filtered_df = filtered_df[filtered_df["City"].isin(city)]
    if state:
        filtered_df = filtered_df[filtered_df["State"].isin(state)]
    if country:
        filtered_df = filtered_df[filtered_df["Country"].isin(country)]

    # Checkbox to toggle heatmap view
    heatmap_enabled = st.checkbox("Enable Heatmap")

    # Map layer setup
    if heatmap_enabled:
        # Heatmap layer
        layer = pdk.Layer(
            "HeatmapLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            opacity=0.9,
            get_weight="Number of Employees",
        )
    else:
        # Scatterplot layer for individual locations
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["Longitude", "Latitude"],
            get_color="[200, 30, 0, 160]",
            get_radius=200,
            opacity=0.8,
        )

    # PyDeck map
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(), longitude=df["Longitude"].mean(), zoom=1
    )
    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
    )

    # Display map
    st.pydeck_chart(map)


# Main app logic
def main():
    df = load_data()  # Load data at the start

    # Page navigation
    page = st.sidebar.selectbox(
        "Choose a page", ["Home", "Data Exploration", "Map Visualization"]
    )

    if page == "Home":
        home_page()
    elif page == "Data Exploration":
        data_exploration_page(df)
    elif page == "Map Visualization":
        map_visualization_page(df)


if __name__ == "__main__":
    main()
