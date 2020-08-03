import pandas as pd
import re 
import time
# main function to call the other function within it
def main():
    restart = True
    while restart:
        global city, month , days 
        city, month , days = taking_entry()   
        df = load_data(city,month,days)
        pop_time_travel(df)
        pop_stations(df)
        trip_info(df)
        user_info(df)
        while True:
            x = input("do you want to restart ? yes or no\n")
            if x.lower() in ["yes" , "no"]:
                break
        if x.lower() == "no":
            break


            
            
def taking_entry ():
    """
     Taking entry from the user.
     args:
         the function takes zero arguments
     returns:
        (str) city - name of the city the user entered
        (str) month - name of the month to filter data by if the user choose to or all
        (str) days - name of the day to filter data by if user choose to or all
     
    """
    # while loop to make sure the user is entering the right city name
    while True :
        city = input("please choose a city : Chicago , New York City , Washington\n").lower()
        if city in ["chicago", "new york city" , "washington"]:
            break
    # askinf if the user wants to apply a month filter
    month_filter  = input ("Do you want to filter the data by months or not ? yes or no?\n")
    # checking the user answer in all forms of agreement (yes,yeah,yup,yep)
    if re.search("^y[esahup]", month_filter):
    # if the user wants to apply a  month filter this while loop make sure he enters the right name
        while True :
            month = input("please, enter a month from the list :(January , February , March , April , May)\n").lower()
            if month in ["january" , "february" , "march" , "april" , "may"]:
                break
            else:
                print("Wrong entery please, enter a month from the list")
    #in case there is no month filter applied 
    else :
        month = "all"
    
    #asking if the user wants to apply a days filter
    days_filter = input ("Do you want to filter the data by days or not ? yes or no ?\n")
    #checking the user answer in all forms of agreement (yes,yeah,yup,yep)
    if re.search("^y[esahup]", days_filter):
     # if the user wants to apply a  day filter this while loop make sure he enters the right name
        while True :
            days = input("please, enter a day from the list :(Monday ,Tuesday ,Wednesday ,Thursday ,Friday,Saturday ,Sunday)\n").lower()
            if days in ["monday" ,"tuesday" ,"wednesday" ,"thursday" ,"friday","saturday" ,"sunday"]:
                break
            else:
                 print("Wrong entery please, enter a day from the list")
    #incase no days filter applied
    else :
        days = "all"
    return city,month,days



            
            
            
            
            
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
    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv' }
    #read the csv file related to the city name
    df = pd.read_csv(CITY_DATA[city])
    # converting the start time and end time into a date data type
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    #df["End Time"] = pd.to_datetime(df["End Time"])
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





def pop_time_travel(df):
    """
    calculate print the popular times of travel
    
    arg:
    (pandas dataframe) df - the dataframe containing the data
    """
    
    start = time.time()
    print("*"*40)
    print("*"*40)
    # calculate the most common hour
    hour = df["Hours"].mode()[0]
    print("the peak hour of the day : {}".format(hour))
    # condition to calc the highest demand day if there is no filter applied
    if days == "all":
        day = df["Week_Days"].mode()[0]
        print("the peak day of the week : {}".format(day))
    # condition to calc the highest demand month if there is no filter applied
    if month == "all":
        month_peak = df["Month"].mode()[0]
        print("the highest traffic month : {}".format(month_peak))
    print("this took {} seconds".format(time.time()-start))
    print("*"*40)

def pop_stations(df):
       """
    find and print the popular stations and routes
    
    arg:
    (pandas dataframe) df - the dataframe containing the data
    """
    start = time.time()
    # most pop start station
    ss = df["Start Station"].mode()[0]
    # most pop end station
    es = df["End Station"].mode()[0]
    # creating a data frame for routes 
    common_routs = df["Start Station"]+ " to " +df["End Station"]
    # most pop trip
    common_route = common_routs.mode()[0]
    print("*"*40)
    print("the most common start station : {}".format(ss))
    print("the most common end station : {}".format(es))
    print("the most common trip from {}".format(common_route))
    print("this took {} seconds".format(time.time()-start))
    print("*"*40)

def trips_info(df):
       """
    calculate and print the trips durations
    
    arg:
    (pandas dataframe) df - the dataframe containing the data
    """
    start = time.time()
    #calculate the max trip duration in hrs
    max_trip = df["Trip Duration"].max()/(60*60)
    #calculate the total duration of trips in hours
    total_trips = df["Trip Duration"].sum()/(60*60)
    #the duration of each trip in average 
    avg_trip = df["Trip Duration"].mean()/60
    print("*"*40)
    print("the longest trip duration in hours = {}".format(round(max_trip)))
    print("the total time travelled in hours = {}".format(round(total_trips)))
    print("the average trip duration in minutes = {}".format(round(avg_trip)))
    print("this took {} seconds".format(time.time()-start))
    print("*"*40)

def user_info(df):
        """
    calculate and print the users information
    
    arg:
    (pandas dataframe) df - the dataframe containing the data
    """
    start = time.time()
    print("*"*40)
    # checking of gender col in the dataframe
    if "Gender" in df:
        #count the values in  gender df
        gender = df["Gender"].value_counts()   
        print("the number of users entered their gender = {}".format(gender.sum()))
        print("the number of male users = {} and they represent {} % of users ".format(gender[0],round(gender[0]/gender.sum()*100)))
        print("the number of female users = {} and they represent {} % of users".format(gender[1],round(gender[1]/gender.sum()*100)))
    #checking if the year of birth col is in the dataframe
    if "Birth Year" in df:
        #get the most common year of birth
        birth = df["Birth Year"].mode()[0]
        #get the most recent year of birth
        #it gives funny answers sometimes 
        youngest = df["Birth Year"].max()
        #get the earliest year of birth
        #gives funny answers 
        oldest = df["Birth Year"].min()
        print("the most common year of birth is  {}".format(int(birth)))
        print("the earliest year of birth is  {}".format(int(oldest)))
        print("the most recent year of birth is  {}".format(int(youngest)))
    user_type = df["User Type"].value_counts()
    print("the number of subscribers = {}".format(user_type[0]))
    print("the number of customers = {}".format(user_type[1]))      
   
    print("this took {} seconds".format(time.time()-start))
    print("*"*40)
    print("*"*40)
    
def taking_entry ():
    """
     Taking entry from the user.
     args:
         the function takes zero arguments
     returns:
        (str) city - name of the city the user entered
        (str) month - name of the month to filter data by if the user choose to or all
        (str) days - name of the day to filter data by if user choose to or all
     
    """
    # while loop to make sure the user is entering the right city name
    while True :
        city = input("please choose a city : Chicago , New York City , Washington\n").lower()
        if city in ["chicago", "new york city" , "washington"]:
            break
    # askinf if the user wants to apply a month filter
    month_filter  = input ("Do you want to filter the data by months or not ? yes or no?\n")
    # checking the user answer in all forms of agreement (yes,yeah,yup,yep)
    if re.search("^y[esahup]", month_filter):
    # if the user wants to apply a  month filter this while loop make sure he enters the right name
        while True :
            month = input("please, enter a month from the list :(January , February , March , April , May)\n").lower()
            if month in ["january" , "february" , "march" , "april" , "may"]:
                break
            else:
                print("Wrong entery please, enter a month from the list")
    #in case there is no month filter applied 
    else :
        month = "all"
    
    #asking if the user wants to apply a days filter
    days_filter = input ("Do you want to filter the data by days or not ? yes or no ?\n")
    #checking the user answer in all forms of agreement (yes,yeah,yup,yep)
    if re.search("^y[esahup]", days_filter):
     # if the user wants to apply a  day filter this while loop make sure he enters the right name
        while True :
            days = input("please, enter a day from the list :(Monday ,Tuesday ,Wednesday ,Thursday ,Friday,Saturday ,Sunday)\n").lower()
            if days in ["monday" ,"tuesday" ,"wednesday" ,"thursday" ,"friday","saturday" ,"sunday"]:
                break
            else:
                 print("Wrong entery please, enter a day from the list")
    #incase no days filter applied
    else :
        days = "all"
    return city,month,days



main()