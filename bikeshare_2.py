import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_raw_data(df):
    
    i = 0
    raw = input("Do you want to see the raw data? (yes/no)").lower()
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5]) # Displays the next five rows
            i += 5
            raw = input("Do you want to see more rows? (yes/no)").lower()
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def get_filters():
    
    month = ''
    day = ''

    while True:
        valid_values = ["month","day","both","none"]
        filter_type = input("Would like to filter by month or day or not using filter at all? (if so type 'none') ").lower()
        if filter_type in valid_values:
            break
        else:
            print("Invalid Input, please choose a valid value ")
    # get user input for month (all, january, february, ... , june)
    if filter_type == "month":
        while True:
            months = {"january":1, "february":2, "march":3, "april":4, "may":5, "june":6}
            month = input("Please Enter a month ").lower()
            if month in months.keys():
                month = months[month]
                break
            elif month == "all":
                break
            else:
                print("Invalid Input, please choose a month ")
        day = "all"
    elif filter_type == "day":
        while True:
            day = input("Please Enter a day, please type your response as an integer (e.g: Saturday:1) ")
            if int(day) in [1,2,3,4,5,6,7]:
                day = int(day)
                break
            elif day == "all":
                break
            else:
                print("Invalid Input, please choose a day or type 'all' ")
        month = "all"

    elif filter_type == "both":
        while True:
            months = {"january":1, "february":2, "march":3, "april":4, "may":5, "june":6}
            month = input("Please Enter a month ").lower()
            if month in months.keys():
                month = months[month]
                break
            elif month == "all":
                break
            else:
                print("Invalid Input, please choose a month ")
        while True:
            day = input("Please Enter a day, please type your response as an integer (e.g: Saturday:1) ")
            if int(day) in [1,2,3,4,5,6,7]:
                day = int(day)
                break
            elif day == "all":
                break
            else:
                print("Invalid Input, please choose a day or type 'all' ")
    else:
        day = "all"
        month = "all"
    # get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*40)
    return month, day


def load_data(city, month, day):
    print(city,month,day)
    
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    if month == "all" and day == "all":
        pass
    elif month != "all" and day == "all":
        df = df[df["Start Time"].dt.month == month]
    elif month == "all" and day != "all":
        df = df[df["Start Time"].dt.weekday == day]
    else:
        df = df[df["Start Time"].dt.month == month]
        df = df[df["Start Time"].dt.weekday == day]

    return df


def time_stats(df):
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df["Start Time"].dt.month.mode()[0]
    months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June"}
    print(f"The most common month is: {months[top_month]}")

    # display the most common day of week
    top_day = df["Start Time"].dt.weekday.mode()[0]
    days = {5: "Saturday", 6: "Sunday", 7: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    print(f"The most common day is: {days[top_day]}")

    # display the most common start hour
    top_hour = df["Start Time"].dt.hour.mode()[0]
    print(f"The most common start hour is:{top_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_ss = df["Start Station"].mode()[0]
    print(f"The most commonly used start station is {top_ss}")

    # display most commonly used end station
    top_es = df["End Station"].mode()[0]
    print(f"The most commonly used end station is {top_es}")

    # display most frequent combination of start station and end station trip
    pair_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    top_pairs = pair_counts.nlargest(1, 'Count')

    x = top_pairs["Start Station"].head(1).item()
    y = top_pairs["End Station"].head(1).item()
    print(f"The most frequent trip is from '{x}' to '{y}'")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = round(df["Trip Duration"].sum())
    print(f"The total travel time in seconds is: {total}")

    # display mean travel time
    mean = round(df["Trip Duration"].mean())
    print(f"The mean travel time in seconds is: {mean}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
   
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df["User Type"].value_counts())

    # Display counts of gender
    if city == "washington":
        print("The database of this city does not provide Gender")
    else:
        print(df["Gender"].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city == "washington":
        print("The database of this city does not provide Birth Year")
    else:
        print(f"The earliest year of birth is: {df["Birth Year"].min()}")
        print(f"The most recent year of birth is: {df["Birth Year"].max()}")
        print(f"The most common year of birth is: {df["Birth Year"].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ["chicago", "new york city", "washington"]
        city = input("Please Enter the city: (Chicago, New York City, Washington) ").lower()
        if city in cities:
            df = pd.read_csv(CITY_DATA[city])
            display_raw_data(df)

            month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

        else:
            print("Invalid Input, please choose one of these cities: (Chicago, New York City, Washington) ")



if __name__ == "__main__":
    main()
