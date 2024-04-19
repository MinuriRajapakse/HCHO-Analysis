import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf

# Load your preprocessed data
data = pd.read_csv("final_dataset.csv")


# Main function to run the web app
def main():
    st.set_page_config(page_title="HCHO Analysis - Sri Lanka", layout="wide")

    st.markdown("<div style='text-align: center;'><h1>HCHO Analysis - Sri Lanka</h1></div>", unsafe_allow_html=True)

    st.sidebar.title('Explore Data')
    locations = data['Location'].unique()
    selected_locations = st.sidebar.multiselect('Select Locations', locations, locations)

    variables = [col for col in data.columns.tolist() if col != "HCHO Reading"]
    selected_variables = st.sidebar.multiselect('Select Variables', variables)

    if selected_variables:
        plot_data(selected_locations, selected_variables)

    st.sidebar.subheader('Visualizations')
    if st.sidebar.checkbox('Time Series Analysis'):
        plot_time_series(selected_locations)

    st.markdown("---")

    # Add map to show locations
    st.subheader("Location Map")
    plot_location_map(selected_locations)

    st.sidebar.subheader('Statistical Summary')
    show_stats(selected_locations)

    st.sidebar.subheader('Data Table')
    show_data_table(selected_locations)

    st.sidebar.subheader('Insights')
    show_insights()


def plot_time_series(locations):
    for location in locations:
        st.subheader(f"Time Series Analysis for {location}")
        location_data = data[data['Location'] == location].copy()
        location_data['Current Date'] = pd.to_datetime(location_data['Current Date'])
        location_data.set_index('Current Date', inplace=True)

        # Line Chart
        st.write("### Line Chart")
        fig_line = px.line(location_data, x=location_data.index, y='HCHO Reading', title='HCHO Time Series')
        st.plotly_chart(fig_line, use_container_width=True)

        # Seasonal Decomposition Plot
        st.write("### Seasonal Decomposition Plot")
        decomposition = seasonal_decompose(location_data['HCHO Reading'], model='additive', period=30)
        fig_seasonal = decomposition.plot()
        st.pyplot(fig_seasonal)

        # Autocorrelation Plot
        st.write("### Autocorrelation Plot")
        plot_acf(location_data['HCHO Reading'], title='Autocorrelation Plot')
        st.pyplot()


def show_stats(locations):
    stats_df = data[data['Location'].isin(locations)]['HCHO Reading'].describe().reset_index()
    st.subheader("Statistical Summary")
    st.dataframe(stats_df.rename(columns={'index': 'Statistic'}))


def show_data_table(locations):
    st.subheader("Detailed Data Table")
    st.dataframe(data[data['Location'].isin(locations)])


def show_insights():
    st.subheader("Insights")
    st.write('- Explore the HCHO distribution across different locations.')
    st.write('- Observe trends in HCHO levels over time.')
    st.write('- Investigate correlations between HCHO levels and external factors.')
    st.write('- Analyze statistical summary metrics for selected locations.')
    st.write('- Examine detailed data in the data table.')


def plot_data(locations, variables):
    for variable in variables:
        if variable != 'Location':
            selected_graph = st.sidebar.selectbox('Select Graph Type', ['Line Chart', 'Scatter Plot', 'Histogram'])

            if selected_graph == 'Line Chart':
                if variable == 'Current Date':
                    fig = px.line(data[data['Location'].isin(locations)], x=variable, y='HCHO Reading',
                                  color='Location', title=f'{variable} vs HCHO')
                else:
                    fig = px.line(data[data['Location'].isin(locations)], x=variable, y='HCHO Reading',
                                  color='Location', title=f'{variable} vs HCHO')
            elif selected_graph == 'Scatter Plot':
                fig = px.scatter(data[data['Location'].isin(locations)], x=variable, y='HCHO Reading', color='Location',
                                 title=f'{variable} vs HCHO')
            elif selected_graph == 'Histogram':
                fig = px.histogram(data[data['Location'].isin(locations)], x=variable, title=f'{variable} Distribution')

            fig.update_layout(title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)


def plot_location_map(locations):
    fig = px.scatter_mapbox(data[data['Location'].isin(locations)], lat='Latitude', lon='Longitude',
                            hover_name='Location',
                            color_discrete_sequence=['red'], zoom=8, height=500)
    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()
