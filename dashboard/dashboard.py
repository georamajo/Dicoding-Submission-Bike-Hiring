import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set(style='dark')
st.set_page_config(page_title="Dashboard Bike-Sharing",
                   page_icon="bar_chart:",
                   layout="wide")
#load data
df = pd.read_csv("https://raw.githubusercontent.com/georamajo/Dicoding-Submission-Bike-Hiring/main/dashboard/cleanned_bike.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# Helper function
def create_monthly_bikers_df(df):
    monthly_bikers_df = df.groupby(['mnth_day', 'weathersit_day']).agg({
        'cnt_day': 'sum'
    })
    monthly_bikers_df = monthly_bikers_df.reset_index()
    monthly_bikers_df.rename(columns={
        "mnth_day": "month",
        "cnt_day": "total_bikers",
        "weathersit_day": "weather_condition"
    }, inplace=True)

    month_mapping = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    monthly_bikers_df['month'] = monthly_bikers_df['month'].map(month_mapping)

    return monthly_bikers_df

def create_seasonly_bikers_df(df):
    seasonly_bikers_df = df.groupby('season_day').agg({
        'cnt_day' : 'sum'
    })
    seasonly_bikers_df = seasonly_bikers_df.reset_index()
    seasonly_bikers_df.rename(columns={
        'cnt_day' : 'total_bikers',
    }, inplace=True)

    seasonly_bikers_df['season_day'] = pd.Categorical(seasonly_bikers_df['season_day'],categories=['musim gugur', 'musim dingin', 'musim semi', 'musim panas'])
    seasonly_bikers_df = seasonly_bikers_df.sort_values('season_day')
    return seasonly_bikers_df

def create_hourly_bikers_df(df):
    hourly_bikers_df = df.groupby('hr').agg({
        'cnt_hour' : 'sum'
    })
    hourly_bikers_df = hourly_bikers_df.reset_index()
    hourly_bikers_df.rename(columns={
        'cnt_hour' : 'total_bikers',
        'hr' : 'hour'
    }, inplace=True)

    return hourly_bikers_df 

# Sidebar
min_date = df["dteday"].min()
max_date = df["dteday"].max()
with st.sidebar:
    st.image("https://raw.githubusercontent.com/georamajo/Dicoding-Submission-Bike-Hiring/main/image/bycycle.png")
    st.sidebar.title("Menu")
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

# Menghubungkan filter
main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

# Menyiapkan berbagai dataframe
monthly_bikers_df = create_monthly_bikers_df(main_df)
seasonly_bikers_df = create_seasonly_bikers_df(main_df)
hourly_bikers_df = create_hourly_bikers_df(main_df)

# Header
st.title("Dashboard Bike-Sharing")
st.subheader("Dicoding Submission")

col1, col2 = st.columns(2)

with col1:
    total_bikers = main_df['cnt_day'].sum()
    total_formatted_bikers = f"{total_bikers:,}".replace(",", ".")
    st.metric("Total Bikers", value=total_formatted_bikers)
with col2:
    total_hours = main_df['cnt_hour'].sum()
    total_formatted_hours = f"{total_hours:,}".replace(",", ".")
    st.metric("Total Hours", value=total_formatted_hours)

st.markdown("---")

# Chart
fig1 = px.line(monthly_bikers_df,
              x='month',
              y='total_bikers',
              color='weather_condition',
              color_discrete_sequence=["orangered", "skyblue", "gray", "blue" ],
              markers=True,
              title="Jumlah Bikers per Bulan Berdasarkan Kondisi Cuaca ").update_layout(xaxis_title='', yaxis_title='Total Bikers')
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(seasonly_bikers_df,
              x='season_day',
              y='total_bikers',
              color='season_day',
              color_discrete_sequence=["peru", "lightskyblue", "olive", "orangered"],
              title='Jumlah Bikers berdasarkan Musim').update_layout(xaxis_title='', yaxis_title='Total Bikers')

fig3 = px.bar(hourly_bikers_df,
              x='hour',
              y='total_bikers',
              color_discrete_sequence=["teal"],
              title='Jumlah Bikers per Jam').update_layout(xaxis_title='', yaxis_title='Total Bikers')

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig2, use_container_width=True)
right_column.plotly_chart(fig3, use_container_width=True)
