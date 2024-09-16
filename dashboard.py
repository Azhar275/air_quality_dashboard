import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import streamlit as st
sns.set(style='dark')


def create_pollutant_df(main_df, pollutant):
    pollutant_df = main_df.groupby(by=['month']).agg({
        pollutant : 'mean'
    }).reset_index()
    return pollutant_df

def create_latest_rain_df(main_df):
    rain_df = main_df.groupby(by=['month']).agg({
        'RAIN' : 'mean'
    }).reset_index().sort_values(by="month", ascending=True)
    return rain_df

def create_compared_rain_df(year_data_df, year):
    rain_df = year_data_df.groupby(by=['station']).agg({
        'RAIN' : 'mean'
    }).reset_index().sort_values(by="station")
    return rain_df

def create_pollutant_count_list(main_df, year, station):
    columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

    pm25_count = main_df.groupby(by=['station', 'year', 'month', 'day']).agg({
        'PM2.5' : 'mean'
    }).query("`PM2.5` >= 50").reset_index().groupby(by=['station', 'year']).agg({
        'PM2.5' : 'count'
    }).reset_index()
    pm25_count = pm25_count[(pm25_count["year"] == year) & (pm25_count["station"] == station)]["PM2.5"]
    if len(pm25_count) > 0 :
        pm25_count = pm25_count[0]
    else :
        pm25_count = 0

    pm10_count = main_df.groupby(by=['station', 'year', 'month', 'day']).agg({
        'PM10' : 'mean'
    }).query("`PM10` >= 50").reset_index().groupby(by=['station', 'year']).agg({
        'PM10' : 'count'
    }).reset_index()
    pm10_count = pm10_count[(pm10_count["year"] == year) & (pm10_count["station"] == station)]["PM10"]
    if len(pm10_count) > 0 :
        pm10_count = pm10_count[0]
    else :
        pm10_count = 0

    so2_count = main_df.groupby(by=['station', 'year', 'month', 'day']).agg({
        'SO2_ppb' : 'mean'
    }).query("`SO2_ppb` >= 20").reset_index().groupby(by=['station', 'year']).agg({
        'SO2_ppb' : 'count'
    }).reset_index()
    so2_count = so2_count[(so2_count["year"] == year) & (so2_count["station"] == station)]["SO2_ppb"]
    if len(so2_count) > 0 :
        so2_count = so2_count[0]
    else :
        so2_count = 0

    no2_count = main_df.groupby(by=['station', 'year', 'month', 'day']).agg({
        'NO2' : 'mean'
    }).query("`NO2` >= 25").reset_index().groupby(by=['station', 'year']).agg({
        'NO2' : 'count'
    }).reset_index()
    no2_count = no2_count[(no2_count["year"] == year) & (no2_count["station"] == station)]["NO2"]
    if len(no2_count) > 0 :
        no2_count = no2_count[0]
    else :
        no2_count = 0

    co_count = main_df.groupby(by=['station', 'year', 'month', 'day']).agg({
        'CO_ppm' : 'mean'
    }).query("`CO_ppm` >= 6").reset_index().groupby(by=['station', 'year']).agg({
        'CO_ppm' : 'count'
    }).reset_index()
    co_count = co_count[(co_count["year"] == year) & (co_count["station"] == station)]["CO_ppm"]
    if len(co_count) > 0 :
        co_count = co_count[0]
    else :
        co_count = 0

    o3_count = main_df.query("`O3_ppb` >= 100").groupby(by=['station', 'year', 'month', 'day']).agg({
        'O3_ppb' : 'count'
    }).query("`O3_ppb` >= 8").groupby(by=['station', 'year']).agg({
        'O3_ppb' : 'sum'
    }).reset_index()
    o3_count = o3_count[(o3_count["year"] == year) & (o3_count["station"] == station)]["O3_ppb"]
    if len(o3_count) > 0 :
        o3_count = o3_count[0]
    else :
        o3_count = 0

    values = [pm25_count, pm10_count, so2_count, no2_count, co_count, o3_count]
    dict = {'pollutants' : columns, 'day_count' : values}
    df = pd.DataFrame(dict)

    return(df)


all_df = pd.read_csv("all_df_data.csv")
min_year = all_df["year"].min()
max_year = all_df["year"].max()
station_list = all_df['station'].unique()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("icon.jpeg", use_column_width=True)
    
    station = st.selectbox(
        "Choose your Station",
        station_list,
    )

    st.write("You selected:", station)

    year = st.selectbox(
        "Choose the year",
        [i for i in range(min_year, max_year+1)]
    )

    st.write("You selected:", year)

main_df = all_df[(all_df["station"] == station) & 
                (all_df["year"] == year)]
year_data_df = all_df[(all_df["year"] == year)]

st.header(station +' Air Quality Dashboard :partly_sunny_rain:')

st.subheader('Pollutant Concentration in '+str(year))

pollutant = st.selectbox(
    "Choose the pollutant",
    ('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3')
)

pollutant_df = create_pollutant_df(main_df, pollutant)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    pollutant_df["month"],
    pollutant_df[pollutant],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_ylabel(pollutant + " Mean (ug/m3)", fontsize=20)
ax.set_xlabel("Month", fontsize=15)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Rain Data in '+str(year))


latest_rain_df = create_latest_rain_df(main_df)
compared_rain_df = create_compared_rain_df(year_data_df, year)
pollutant_count_list = create_pollutant_count_list(main_df, year, station).sort_values(by="day_count", ascending=False)
print(pollutant_count_list)

col1, col2 = st.columns(2)

with col1:
    rain_mean = round(latest_rain_df.RAIN.mean(), 3)
    st.metric("Rain Average "+str(year), value=str(rain_mean)+" mm")
 
with col2:
    max_rain = latest_rain_df["RAIN"].max()
    highest_month = calendar.month_name[int(latest_rain_df[(latest_rain_df["RAIN"] == max_rain)]["month"])]
    st.metric("Month with Highest Rain", value=highest_month + " ("+str(round(max_rain, 3))+" mm)")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    latest_rain_df["month"],
    latest_rain_df['RAIN'],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title(station + " Rain Every Month", loc="center", fontsize=20)
ax.set_ylabel("Rain Mean (mm)", fontsize=20)
ax.set_xlabel("Month", fontsize=15)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))

colors = []

for i in station_list :
    if i == station:
        colors.append("#90CAF9")
    else :
        colors.append("#D3D3D3")

sns.barplot(
    y="RAIN", 
    x="station",
    data=compared_rain_df,
    palette=colors,
    ax=ax
)
ax.set_title(station + " Comparison with Others in "+ str(year), loc="center", fontsize=20)
ax.set_ylabel("Rain Precipitation Average (mm)", fontsize=20)
ax.set_xlabel("Station", fontsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader(station+ ' Dangerous Pollutant Level in '+ str(year) )

col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="day_count", 
        x="pollutants",
        data=pollutant_count_list.head(3),
        palette=colors,
        ax=ax
    )
    ax.set_title("The Most Dangerous Pollutant", loc="center", fontsize=50)
    ax.set_ylabel("Number of Days Reach Dangerous", fontsize=30)
    ax.set_xlabel("Pollutant", fontsize=35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#D3D3D3", "#D3D3D3", "#90CAF9"]
 
    sns.barplot(
        y="day_count", 
        x="pollutants",
        data=pollutant_count_list.tail(3),
        palette=colors,
        ax=ax
    )
    ax.set_title("The Safest Pollutant", loc="center", fontsize=50)
    ax.set_ylabel("Number of Days Reach Dangerous", fontsize=30)
    ax.set_xlabel("Pollutant", fontsize=35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
