import streamlit as st
import pandas as pd
import altair as alt

# Set Streamlit page configuration
st.set_page_config(
    page_title="IPL-Stats_Dashboard",
    layout="wide",
    page_icon="🏂",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for dark theme
st.markdown(
    """
    <style>
    /* Set background color */
    body {
        background-color: #1E1E1E;
        color: #FFFFFF; /* Set text color to white */
    }
    
    /* Set background color for sidebar */
    [data-testid="stSidebar"] {
        background-color: darkgrey;
    }

    /* Set background color for main content area */
    [data-testid="stBlockContainer"] {
        background-color: #1E1E1E;
    }

    /* Set background color for buttons */
    .css-1tjvrzi.e1ls44fh1 {
        background-color: #555555 !important;
    }

    /* Set text color for buttons */
    .css-1tjvrzi.e1ls44fh1 {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to apply all filters and calculate win-lose counts
def apply_filters(df):
    season = st.selectbox("Select Season", df['season'].unique(), help="Choose the cricket season")
    team = st.selectbox("Select Team", pd.concat([df['team1'], df['team2']]).unique(), help="Choose the cricket team")
    city = st.selectbox("Select City", df['city'].fillna('Unknown').unique(), help="Choose the winning team")
    apply_button = st.button("Apply Filters", help="Apply the selected filters")
   
    if apply_button:
        max_dates_by_season = df.groupby('season')['date'].max()
        max_date_for_season = max_dates_by_season[season]

        dt = df[df['date'] == max_date_for_season]
        winner = dt['winner'].iloc[0]  # Get the winner of the most recent match

        st.sidebar.image("/home/kpit/Documents/IPL.webp", use_column_width=True)

        st.sidebar.success(f"🎉 {winner} won the Final! 🏆")

        filtered_data = df[(df['season'] == season) & ((df['team1'] == team) | (df['team2'] == team)) & (df['city'].fillna('Unknown') == city)]
        
        # Calculate statistics
        stats = filtered_data['winner'].describe()
        stats.index = ['Number of Matches', f'Teams to win in {city}', 'Team to win max matches', f'Max Wins by a team in {city}']

        # Calculate win-lose counts
        win_counts = filtered_data[filtered_data['winner'] == team].shape[0]
        lose_counts = filtered_data[filtered_data['winner'] != team].shape[0]
        win_lose_counts = {'Result': ['Win', 'Lose'], 'Count': [win_counts, lose_counts]}
        
        return filtered_data, win_lose_counts, stats
    else:
        return None, None, None

# Function to plot pie chart
def plot_pie_chart(win_lose_counts):
    df = pd.DataFrame(win_lose_counts)
    chart = alt.Chart(df).mark_arc().encode(
        theta='Count:Q',
        color='Result:N',
        tooltip=['Result', 'Count']
    ).properties(
        width=400,
        height=400
    )
    return chart

# Filters page
def filters_page():
    st.markdown("---")
    st.subheader("Filters")
    df = pd.read_csv("/home/kpit/Downloads/archive/matches.csv")
    filtered_data, win_lose_counts, stats = apply_filters(df)
    
    if filtered_data is not None:
        st.subheader("Filtered Data")
        st.write(filtered_data)
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if win_lose_counts["Count"][0] > 0:  # Check if there are more than one data point
                st.subheader("Win-Lose Pie Chart")
                st.altair_chart(plot_pie_chart(win_lose_counts))
            else:
                st.subheader("Not enough data to display chart")
        
        with col2:
            if stats is not None:
                st.subheader("Statistics")
                st.write(stats)
            else:
                st.subheader("No statistics to display")

# Teams page
def teams_page():
    st.markdown("---")
    st.subheader("Teams")
    # Add content for the Teams page here

# Main function
def main():
    st.title("Cricket Season Selection App")
    

    # Navigation option for Teams page near the subheader of Filters
    st.sidebar.subheader("Menu Ribbon")

    st.sidebar.write(" ")  # Adding some space
    st.sidebar.write(" ")
    st.sidebar.write(" ")  # Adding some space
    

    # Set query parameters based on button clicks
    if st.sidebar.button("Filters"):
        st.query_params["page"] = "Filters"
    if st.sidebar.button("Teams"):
        st.query_params["page"] = "Teams"

    # Get the value of the "page" query parameter
    page = st.query_params.get("page", "Filters")

    # Now you can use the value of "page" to determine which page to display
    if page == "Filters":
        # Display the Filters page
        filters_page() 
    elif page == "Teams":
        # Display the Teams page
        teams_page()

if __name__ == "__main__":
    main()
