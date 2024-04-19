import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your preprocessed data
data = pd.read_csv("final_dataset.csv")


# Main function to run the web app
def main():
    st.title('HCHO Analysis Web App')

    st.sidebar.title('Explore Data')
    locations = data['Location'].unique()
    selected_locations = st.sidebar.multiselect('Select Locations', locations, locations)

    st.sidebar.subheader('Visualizations')
    if st.sidebar.checkbox('Histogram'):
        plot_histogram(selected_locations)
    if st.sidebar.checkbox('Time Series Analysis'):
        plot_time_series(selected_locations)
    if st.sidebar.checkbox('Scatter Plot with External Factors'):
        plot_scatter(selected_locations)


def plot_histogram(locations):
    fig = px.histogram(data[data['Location'].isin(locations)], x='HCHO Reading', title='HCHO Distribution')
    st.plotly_chart(fig)


def plot_time_series(locations):
    fig = px.line(data[data['Location'].isin(locations)], x='Current Date', y='HCHO Reading', color='Location',
                  title='HCHO Time Series')
    st.plotly_chart(fig)


def plot_scatter(locations):
    selected_factor = st.selectbox('Select External Factor', ['PRECIPITATION', 'WD10M', 'Elevation'])
    fig = px.scatter(data[data['Location'].isin(locations)], x=selected_factor, y='HCHO Reading', color='Location',
                     title=f'Scatter Plot: {selected_factor} vs HCHO')
    st.plotly_chart(fig)


if __name__ == '__main__':
    main()
