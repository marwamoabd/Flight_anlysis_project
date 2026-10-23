
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import base64

with open("flight_banner.png", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()

# 1. Page Configuration
st.set_page_config(page_title="Flight Analysis", layout="wide")

# 2. Read CSV and assign to dataframe 'df'
df = pd.read_csv("Cleaned_Flight_df.csv",index_col=0) 

# Page configuration
st.set_page_config(
    page_title="Flight Delay Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom colors and styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #F4F8FC;
        color: #17365D;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E3EDF9;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #17365D;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #D6E5F5;
        padding: 18px;
        border-radius: 12px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2474D2;
        color: white;
        border-radius: 8px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1557A5;
        color: white;
    }

    /* Dividers */
    hr {
        border-color: #D6E5F5;
    }
</style>
""", unsafe_allow_html=True)


# Navigation
st.sidebar.title("✈️ Flight Analysis")
st.sidebar.caption("Flight Delay EDA Project")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Airline Analysis",
        "Delay Analysis"
    ]
)


# HOME PAGE
if page == "Home":

    st.markdown(f"""
    <style>
    .hero-banner {{
        background:
            linear-gradient(
                90deg,
                rgba(10, 35, 75, 0.80),
                rgba(10, 35, 75, 0.12)
            ),
            url("data:image/png;base64,{image_base64}");

        background-size: cover;
        background-position: center;
        padding: 45px 35px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
    }}

    .hero-banner h1 {{
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }}

    .hero-banner p {{
        color: white;
        font-size: 18px;
    }}
    </style>

    <div class="hero-banner">
        <h1>Flight Analysis</h1>
        <p>
            Exploring flight operations, delays, and trends
            using historical flight data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Welcome to the Flight Delay Analysis Dashboard!

    This project explores historical flight data to discover patterns in
    airline operations, airport activity, flight delays, and performance.
    """)

        # Summary Cards
    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #D6E5F5;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(23, 54, 93, 0.08);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1.4, 1, 1])

    with col1:
        st.metric(
            label="✈️ Total Flights",
            value=f"{len(df):,}"
        )

    with col2:
        start_year = int(df['Year'].min())
        end_year = int(df['Year'].max())

        st.metric(
            label="🗓️ Years",
            value=f"{start_year} – {end_year}",
            help=f"{df['Year'].nunique()} distinct years in the dataset"
        )

    with col3:
        st.metric(
            label="📊 Unique Airlines",
            value=f"{df['UniqueCarrier'].nunique():,}"
        )

    with col4:
        origin_count = df['Origin'].nunique()
        dest_count = df['Dest'].nunique()

        st.metric(
            label="📍 Unique Airports",
            value=f"{len(set(df['Origin'].dropna()) | set(df['Dest'].dropna())):,}",
            help=f"Origins: {origin_count} | Destinations: {dest_count}"
        )


    st.divider()

    st.subheader("Explore the Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.info("✈️ **Airline Analysis**")
        st.write("Compare airlines and explore flight activity.")


    with col2:
        st.info("📊 **Delay Analysis**")
        st.write("Investigate departure and arrival delay patterns.")

    # Prepare monthly flight counts
    month_counts = (
        df.groupby('Month')
        .size()
        .reset_index(name='FlightCount')
    )

    # Prepare flight counts by day of week
    day_counts = (
        df.groupby('DayOfWeek')
        .size()
        .reset_index(name='FlightCount')
    )

    # Prepare correlation matrix
    duration_columns = [
        'Distance',
        'AirTime',
        'TaxiIn',
        'TaxiOut',
        'ActualElapsedTime'
    ]

    duration_corr = df[duration_columns].corr()    

    st.divider()

    st.header("Flight Patterns & Operational Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Number of Flights by Month
        fig1 = px.bar(
            month_counts,
            x='Month',
            y='FlightCount',
            title='Flight Volume Patterns'
        )
        st.plotly_chart(fig1, width="stretch")

    with col2:
        # Number of Flights by Day of Week
        fig2 = px.bar(
            day_counts,
            x='DayOfWeek',
            y='FlightCount',
            title='Weekly Flight Activity'
        )
        st.plotly_chart(fig2, width="stretch")

    with col3:
        # Correlation Between Flight Duration Variables
        fig3 = px.imshow(
            duration_corr,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            title='Flight Duration Relationships'
        )
        st.plotly_chart(fig3, width="stretch")

# AIRLINE ANALYSIS PAGE
elif page == "Airline Analysis":

    st.title("✈️ Airline Analysis")
    st.info("Explore airline activity, flight volume, and operational patterns.")

    # Summary Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Airlines",
        df['UniqueCarrier'].nunique()
    )

    col2.metric(
        "Average Airtime",
        f"{df['AirTime'].mean():.1f} min"
    )

    col3.metric(
        "Average Distance",
        f"{df['Distance'].mean():.1f} miles"
    )

    col4.metric(
        "Years Covered",
        f"{int(df['Year'].min())}–{int(df['Year'].max())}"
    )

    # Row 1: Flight Count | Average Arrival Delay
    col1, col2 = st.columns(2)

    with col1:
        carrier_counts = (
            df['UniqueCarrier']
            .value_counts()
            .rename_axis('UniqueCarrier')
            .reset_index(name='FlightCount')
        )

        fig1 = px.bar(
            carrier_counts,
            x='UniqueCarrier',
            y='FlightCount',
            title='Number of Flights by Airline',
            labels={
                'UniqueCarrier': 'Airline',
                'FlightCount': 'Number of Flights'
            }
        )

        st.plotly_chart(fig1, width="stretch")

    with col2:
        airline_delays = (
            df.groupby('UniqueCarrier')
            .agg(
                AverageDelay=('ArrDelay', 'mean'),
                MedianDelay=('ArrDelay', 'median'),
                Flights=('ArrDelay', 'count')
            )
            .reset_index()
            .sort_values('AverageDelay', ascending=False)
        )

        fig2 = px.bar(
            airline_delays,
            x='UniqueCarrier',
            y='AverageDelay',
            hover_data=['MedianDelay', 'Flights'],
            title='Average Arrival Delay by Airline',
            labels={
                'UniqueCarrier': 'Airline',
                'AverageDelay': 'Average Arrival Delay (minutes)'
            }
        )

        st.plotly_chart(fig2, width="stretch")

    # Row 2: Average Airtime | Flight Volume by Airline and Month
    col1, col2 = st.columns(2)

    with col1:
        airline_airtime = (
            df.groupby('UniqueCarrier')
            .agg(
                AvgAirTime=('AirTime', 'mean'),
                FlightCount=('AirTime', 'count')
            )
            .reset_index()
            .query('FlightCount >= 10')
            .sort_values('AvgAirTime', ascending=False)
        )

        fig3 = px.bar(
            airline_airtime,
            x='UniqueCarrier',
            y='AvgAirTime',
            hover_data=['FlightCount'],
            title='Average Airtime by Airline',
            labels={
                'UniqueCarrier': 'Airline',
                'AvgAirTime': 'Average Airtime (minutes)'
            }
        )

        st.plotly_chart(fig3, width="stretch")

    with col2:
        airline_month_volume = df.pivot_table(
            index='UniqueCarrier',
            columns='Month',
            values='FlightNum',
            aggfunc='count',
            fill_value=0
        )

        fig4 = px.imshow(
            airline_month_volume,
            labels={
                'x': 'Month',
                'y': 'Airline',
                'color': 'Flight Count'
            },
            title='Flight Volume by Airline and Month',
            aspect='auto',
            color_continuous_scale='Blues'
        )

        st.plotly_chart(fig4, width="stretch")

    # Row 3: Top 10 Airlines | Average Distance vs Airtime
    col1, col2 = st.columns(2)

    with col1:
        top_carriers = (
            df['UniqueCarrier']
            .value_counts()
            .head(10)
            .rename_axis('UniqueCarrier')
            .reset_index(name='FlightCount')
            .sort_values('FlightCount', ascending=True)
        )

        fig5 = px.bar(
            top_carriers,
            x='FlightCount',
            y='UniqueCarrier',
            orientation='h',
            color='UniqueCarrier',
            title='Top 10 Airlines by Flight Volume',
            labels={
                'FlightCount': 'Number of Flights',
                'UniqueCarrier': 'Airline'
            },
            color_discrete_sequence=px.colors.qualitative.Alphabet
        )

        fig5.update_layout(
            template='plotly_white',
            showlegend=False
        )

        st.plotly_chart(fig5, width="stretch")

    with col2:
        airline_stats = (
            df.groupby('UniqueCarrier')
            .agg(
                AvgDistance=('Distance', 'mean'),
                AvgAirTime=('AirTime', 'mean'),
                FlightCount=('FlightNum', 'count')
            )
            .reset_index()
        )

        fig6 = px.scatter(
            airline_stats,
            x='AvgDistance',
            y='AvgAirTime',
            size='FlightCount',
            color='UniqueCarrier',
            hover_name='UniqueCarrier',
            hover_data=['FlightCount'],
            title='Average Distance vs Airtime by Airline',
            labels={
                'AvgDistance': 'Average Distance (miles)',
                'AvgAirTime': 'Average Airtime (minutes)',
                'FlightCount': 'Number of Flights',
                'UniqueCarrier': 'Airline'
            },
            color_discrete_sequence=px.colors.qualitative.Alphabet
        )

        fig6.update_layout(template='plotly_white')

        st.plotly_chart(fig6, width="stretch")

    # Row 4: Full-width Airline Network Coverage
    st.subheader("Airline Network Coverage")

    airline_network = (
        df.groupby('UniqueCarrier')
        .agg(
            UniqueOrigins=('Origin', 'nunique'),
            UniqueDestinations=('Dest', 'nunique'),
            FlightCount=('FlightNum', 'count')
        )
        .reset_index()
    )

    fig7 = px.scatter(
        airline_network,
        x='UniqueOrigins',
        y='UniqueDestinations',
        size='FlightCount',
        color='UniqueCarrier',
        hover_name='UniqueCarrier',
        hover_data=[
            'FlightCount',
            'UniqueOrigins',
            'UniqueDestinations'
        ],
        title='Airline Network Coverage',
        labels={
            'UniqueOrigins': 'Number of Unique Origin Airports',
            'UniqueDestinations': 'Number of Unique Destination Airports',
            'FlightCount': 'Number of Flights',
            'UniqueCarrier': 'Airline'
        },
        color_discrete_sequence=px.colors.qualitative.Alphabet
    )

    fig7.update_layout(
        template='plotly_white',
        legend_title_text='Airline',
        height=550
    )

    st.plotly_chart(fig7, width="stretch")

    # Airline Code Reference
    st.divider()
    st.subheader("Airline Code Reference")
    st.write("Look up the full name associated with each airline code.")

    airline_names = {
        '9E': 'Endeavor Air',
        'AA': 'American Airlines',
        'AQ': 'Aloha Airlines',
        'AS': 'Alaska Airlines',
        'B6': 'JetBlue Airways',
        'CO': 'Continental Airlines',
        'DH': 'Atlantic Coast Airlines',
        'DL': 'Delta Air Lines',
        'EA': 'Eastern Air Lines',
        'EV': 'ExpressJet Airlines',
        'F9': 'Frontier Airlines',
        'FL': 'AirTran Airways',
        'HA': 'Hawaiian Airlines',
        'HP': 'America West Airlines',
        'MQ': 'American Eagle Airlines',
        'NW': 'Northwest Airlines',
        'OH': 'Comair',
        'OO': 'SkyWest Airlines',
        'PA (1)': 'Pan American World Airways',
        'PI': 'Piedmont Airlines',
        'PS': 'Pacific Southwest Airlines',
        'TW': 'Trans World Airlines',
        'UA': 'United Airlines',
        'US': 'US Airways',
        'WN': 'Southwest Airlines',
        'XE': 'ExpressJet Airlines',
        'YV': 'Mesa Airlines',
        'TZ': 'ATA Airlines',
        'ML (1)': 'AirTran Airways (historical code)'
    }

    airline_reference = pd.DataFrame(
        sorted(df['UniqueCarrier'].dropna().unique()),
        columns=['Airline Code']
    )

    airline_reference['Airline Name'] = (
        airline_reference['Airline Code']
        .map(airline_names)
        .fillna('Name to be verified')
    )

    st.dataframe(
        airline_reference,
        hide_index=True,
        width="stretch"
    )


# DELAY ANALYSIS PAGE
elif page == "Delay Analysis":

    st.title("📊 Delay Analysis")

    st.info("Investigate departure delays, arrival delays, and factors "
        "associated with flight delays")

    avg_arr_delay = df['ArrDelay'].mean()
    avg_dep_delay = df['DepDelay'].mean()

    arrival_delay_rate = (df['ArrDelay'] > 0).mean() * 100

    severe_delay_rate = (df['ArrDelay'] >= 60).mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Arrival Delay", f"{avg_arr_delay:.1f} min")
    col2.metric("Average Departure Delay", f"{avg_dep_delay:.1f} min")
    col3.metric("Arrival Delay Rate", f"{arrival_delay_rate:.1f}%")
    col4.metric("Severe Delay Rate (60+ min)", f"{severe_delay_rate:.1f}%")

 # Create Arrival Status
    df['ArrivalStatus'] = np.select(
        [
            df['ArrDelay'] < 0,
            df['ArrDelay'] == 0,
            df['ArrDelay'] > 0
        ],
        ['Early', 'On Time', 'Delayed'],
        default='Unknown'
    )

    # Prepare data for the pie chart
    arrival_counts = (
        df['ArrivalStatus']
        .value_counts()
        .rename_axis('ArrivalStatus')
        .reset_index(name='FlightCount')
    )

    # Prepare monthly arrival delay data
    monthly_delay = (
        df.groupby('Month')['ArrDelay']
        .mean()
        .reset_index()
    )

    # Row 1: Arrival and Departure Delay Distributions
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(
            df,
            x='ArrDelay',
            nbins=50,
            title='Distribution of Arrival Delays',
            labels={'ArrDelay': 'Arrival Delay (minutes)'}
        )
        st.plotly_chart(fig1, width="stretch")

    with col2:
        fig2 = px.histogram(
            df,
            x='DepDelay',
            nbins=50,
            title='Distribution of Departure Delays',
            labels={'DepDelay': 'Departure Delay (minutes)'}
        )
        st.plotly_chart(fig2, width="stretch")

    # Row 2: Arrival Status and Monthly Arrival Delay
    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.pie(
            arrival_counts,
            names='ArrivalStatus',
            values='FlightCount',
            title='Proportion of Arrival Statuses',
            color='ArrivalStatus',
            color_discrete_map={
                'Early': 'green',
                'On Time': 'blue',
                'Delayed': 'red',
                'Unknown': 'gray'
            }
        )

        fig3.update_traces(
            textposition='inside',
            textinfo='percent'
        )

        st.plotly_chart(fig3, width="stretch")

    with col4:
        fig4 = px.line(
            monthly_delay,
            x='Month',
            y='ArrDelay',
            markers=True,
            title='Average Arrival Delay by Month',
            labels={
                'Month': 'Month',
                'ArrDelay': 'Average Arrival Delay (minutes)'
            }
        )

        fig4.update_xaxes(
            tickmode='linear',
            dtick=1
        )

        st.plotly_chart(fig4, width="stretch")

            # Origin Airports with Highest Average Departure Delays
    st.divider()
    st.subheader("🛫 Origin Airports with Highest Average Departure Delays")

    origin_delays = (
        df.groupby('Origin')['DepDelay']
        .agg(
            AverageDelay='mean',
            Flights='count'
        )
        .reset_index()
        .query('Flights >= 30')
        .nlargest(15, 'AverageDelay')
    )

    fig5 = px.bar(
        origin_delays.sort_values('AverageDelay', ascending=True),
        x='AverageDelay',
        y='Origin',
        orientation='h',
        hover_data=['Flights'],
        title='Origin Airports with Highest Average Departure Delays',
        labels={
            'Origin': 'Origin Airport',
            'AverageDelay': 'Average Departure Delay (minutes)',
            'Flights': 'Number of Flights'
        },
        color='AverageDelay',
        color_continuous_scale='Blues'
    )

    fig5.update_layout(
        template='plotly_white',
        yaxis_title='Origin Airport',
        coloraxis_showscale=False
    )

    st.plotly_chart(fig5, width="stretch")

    # Airport Code Reference
    st.divider()
    st.subheader("📍 Airport Code Reference")
    st.write("Use this guide to identify the airports shown in the chart.")

    airport_names = {
        'COS': 'Colorado Springs Airport',
        'OMA': 'Eppley Airfield (Omaha)',
        'MHT': 'Manchester-Boston Regional Airport',
        'IAD': 'Washington Dulles International Airport',
        'LGA': 'LaGuardia Airport',
        'ISP': 'Long Island MacArthur Airport',
        'MIA': 'Miami International Airport',
        'EWB': 'New Bedford Regional Airport',
        'SAT': 'San Antonio International Airport',
        'TUL': 'Tulsa International Airport',
        'RIC': 'Richmond International Airport',
        'CAE': 'Columbia Metropolitan Airport',
        'ELP': 'El Paso International Airport',
        'ANC': 'Ted Stevens Anchorage International Airport',
        'SJU': 'Luis Muñoz Marín International Airport'
    }

    airport_reference = pd.DataFrame(
        list(airport_names.items()),
        columns=['Airport Code', 'Airport Name']
    )

    st.dataframe(
        airport_reference,
        hide_index=True,
        width="stretch"
    )
