import pandas as pd
import re 
import time
import streamlit as st
import matplotlib.pyplot as plt

"# Bikeshare Data exploration"

city = st.selectbox("Choose a city", ("Chicago", "New York City", "Washington"))
month_filter = st.checkbox("Month filter")
if month_filter:
    month = st.selectbox("Choose a month", ("January" , "February" , "March" , "April" , "May")) 
    time.sleep(1.5)
else:
    month = "all"
days_filter = st.checkbox("Day filter")
if days_filter:
    days =st.selectbox("Choose a day", ("Monday" ,"Tuesday" ,"Wednesday" ,"Thursday" ,"Friday","Saturday" ,"Sunday"))
    time.sleep(1.5)
else:
    days = "all"

def load_data(city, month, days):
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
   
    # load data file into a dataframe
    CITY_DATA = { 'Chicago': 'chicago.csv',
                  'New York City': 'new_york_city.csv',
                  'Washington': 'washington.csv' }
    #read the csv file related to the city name
    df = pd.read_csv(CITY_DATA[city])
    # converting the start time and end time into a date data type
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # adding month column
    df["Month"] = df["Start Time"].dt.month_name(locale = "English")
    df["Hours"] = df["Start Time"].dt.hour
    # adding week day column
    df["Week_Days"] = df["Start Time"].dt.day_name()
    if month != "all":
        df = df[df["Month"] ==  month.title()]
    if days != "all":
        df = df[df["Week_Days"] ==  days.title()]
    return df

df = load_data(city,month,days)
df = df.drop("Unnamed: 0" ,axis = 1)
  
"## Sample of the raw data ", df.head(5) 

"# Time travel:"

"## Plot of the trips per hour:" 

chart_data0 = df["Hours"].value_counts()
st.bar_chart(chart_data0)
hour = df["Hours"].mode()[0]
"## The busiest hour in the day is %s:00" %hour 
if days == "all":
    
    "## Plot of the trips per day: "  
    day = df["Week_Days"].mode()[0]
    chart_data = df["Week_Days"].value_counts()
    "### the busiest day in the week is ",day
    st.bar_chart(chart_data)
    

if month == "all":
    
    "## plot of the trips per month:"
    month_peak = df["Month"].mode()[0]
    chart_data1 = df["Month"].value_counts()
    st.bar_chart(chart_data1)
    "### the highest trafic is in: ", month_peak
   

"# Popoular stations and routs:"
ss = df["Start Station"].mode()[0]
es = df["End Station"].mode()[0]
common_routs = df["Start Station"]+ " to " +df["End Station"]
common_route = common_routs.mode()[0]
"## The most popular starting station in %s city :"%city,ss
"## The most popular ending destination in %s city :"%city,es
"## The most popular trip in %s city :"%city,common_route

"# Trips duration:"
max_trip = round(df["Trip Duration"].max()/(60*60),1)
total_trips = round(df["Trip Duration"].sum()/(60*60),1)
avg_trip = round(df["Trip Duration"].mean()/60,1)
"## The longest trip in %s city in hours:"%city,max_trip
"## The total duration of trips in %s city is:"%city,total_trips
"## The average trip duration in %s city is :"%city,avg_trip

"# Users info:"
user_type = df["User Type"].value_counts()
"## Users distribution in %s city by type :"%city, user_type
if "Gender" in df:
        gender = df["Gender"].value_counts()
        "## Users distributiion in %s city by gender :"%city, gender
if "Birth Year" in df:
        common_birth = int(df["Birth Year"].mode()[0])
        youngest = int(df["Birth Year"].max())
        oldest = int(df["Birth Year"].min())
"## The most common year of birth  in %s city is: "%city,common_birth
"## The earliest year of birth in %s city is:"%city,oldest
"## The most recent year of birth %s city :"%city,youngest
