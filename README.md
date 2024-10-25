**Project Overview**
=====================

This repository contains a dashboard project that utilizes the [air quality dataset](https://github.com/marceloreis/HTI/tree/master) dataset to provide insights and visualizations about the air quality in some station in Beijing, China from 2013 until 2017.

You can access the dashboard using this [link](https://air-quality-dashboard-bh5qs9cb47ngyms6pmmytj.streamlit.app/)

**Dataset**
==========

The dataset used in this project is the [air quality dataset](https://github.com/marceloreis/HTI/tree/master). This dataset contains information such as :
- year: year of data in this row 
- month: month of data in this row 
- day: day of data in this row 
- hour: hour of data in this row 
- PM2.5: PM2.5 concentration (ug/m^3)
- PM10: PM10 concentration (ug/m^3)
- SO2: SO2 concentration (ug/m^3)
- NO2: NO2 concentration (ug/m^3)
- CO: CO concentration (ug/m^3)
- O3: O3 concentration (ug/m^3)
- TEMP: temperature (degree Celsius) 
- PRES: pressure (hPa)
- DEWP: dew point temperature (degree Celsius)
- RAIN: precipitation (mm)
- wd: wind direction
- WSPM: wind speed (m/s)
- station: name of the air-quality monitoring site

For detailed info, please check [the dataset information](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)

**Dashboard Explanation**
=====================

The dashboard is designed to provide an interactive and intuitive way to explore the air quality dataset. The dashboard will visualize how is the pollutants condition in certain station in certain year. The dashboard also visualize the rain precipitation every year and how is the comparison between one station and the others. It also will tell what pollutants are dangerous and safe in certain station.

**Technical Details**
=====================

The dashboard is built using Python and deployed using Streamlit. The dashboard repository is consists of some file:

* **all_df_data.csv**: contains the complete and processed data of the air quality dataset (including addition column that convert some pollutant into another unit such as ppb and ppm)
* **dashboard.py**: contains the code for dashboard
* **requirements.txt**: contains the library that need to be installed before running the dashboard
