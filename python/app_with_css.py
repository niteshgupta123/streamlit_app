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

alt.themes.enable("dark")

# Function to apply all filters and calculate win-lose counts
def apply_filters(df):
    season = st.sidebar.selectbox("Select Season", df['season'].unique(), help="Choose the cricket season")
    team = st.sidebar.selectbox("Select Team", pd.concat([df['team1'], df['team2']]).unique(), help="Choose the cricket team")
    winner = st.sidebar.selectbox("Select Winner", df['winner'].unique(), help="Choose the winning team")
    apply_button = st.sidebar.button("Apply Filters", help="Apply the selected filters")
    
    if apply_button:
        filtered_data = df[(df['season'] == season) & ((df['team1'] == team) | (df['team2'] == team))]
        
        # Calculate win-lose counts
        win_counts = filtered_data[filtered_data['winner'] == team].shape[0]
        lose_counts = filtered_data[filtered_data['winner'] != team].shape[0]
        win_lose_counts = {'Result': ['Win', 'Lose'], 'Count': [win_counts, lose_counts]}
        
        return filtered_data, win_lose_counts
    else:
        return None, None

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

# Main function
def main():
    st.title("Cricket Season Selection App")
    st.markdown("""
    <style>
    .stApp {
        background-color: darkgrey;
    }
    .sidebar .sidebar-content {
        background-color: black;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Filters")
    df = pd.read_csv("/home/kpit/Downloads/archive/matches.csv")
    filtered_data, win_lose_counts = apply_filters(df)
    
    if filtered_data is not None:
        st.subheader("Filtered Data")
        st.write(filtered_data)
        st.markdown("---")
        if win_lose_counts["Count"][0] > 1:  # Check if there are more than one data point
            st.subheader("Win-Lose Pie Chart")
            st.altair_chart(plot_pie_chart(win_lose_counts))
        else:
            st.subheader("Not enough data to display chart")

if __name__ == "__main__":
    main()
