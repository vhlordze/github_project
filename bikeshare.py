import string
import datetime as dt
import time
import pandas as pd
import numpy as np
#refactoring this code

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

MONTHS = {'all': 'all', 'january': 'january',
          'february': 'february', 'march': 'march', 'april': 'april', 'may': 'may', 'june': 'june'}
DAYS = {'all': 'all', 'monday': 'monday', 'tuesday': 'tuesday', 'wednesday': 'wednesday',
        'thursday': 'thursday', 'friday': 'friday', 'saturday': 'saturday', 'sunday': 'sunday'}


def clean_input(user_input):
    """" Removes punctuation marks from input provided by user"""
    user_input = user_input.strip('\n')
    translator = str.maketrans('', '', string.punctuation)
    return user_input.translate(translator)


def get_part_of_datetime(date_time, part):
    """ Returns either the year, month, day or hour of a given date"""
    date_time = dt.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    if part == 'year':
        return date_time.strftime('%Y')
    elif part == 'month':
        return date_time.strftime('%B')
    elif part == 'day_of_week':
        return date_time.strftime('%A')
    elif part == 'hour':
        return date_time.strftime('%H')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    valid_input = False
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not valid_input:
        city = input('\n Please select a city, Available cities are chicago, new york city, washington.\n')
        city = clean_input(city.lower())
        if city in ['chicago', 'new york city', 'washington']:
            valid_input = True
        else:
            print("Invalid city entered. Available cities are " + ','.join(CITY_DATA.keys()))

    # get user input for month (all, january, february, ... , june)
    valid_input = False

    while not valid_input:
        month = input('\n Please select a month, Available values are all, january, february, ..., june.\n')
        month = clean_input(month.lower())
        if month in MONTHS.keys():
            valid_input = True
        else:
            print("Invalid month entered. Available months are  " + ','.join(MONTHS.keys()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_input = False

    while not valid_input:
        day = input('\n Please enter day, Available values are all, monday, tuesday, ... sunday.\n')
        day = clean_input(day.lower())
        if day in DAYS.keys():
            valid_input = True
        else:
            print("Invalid day entered. Available days are  " + ','.join(DAYS.keys()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data_to_use = CITY_DATA[city]
    df = pd.read_csv(data_to_use)
    # drop rows containing NAN fields
    df2 = df.dropna()

    # Ensure the Start and End Time are Date
    pd.to_datetime(df2['Start Time'])
    pd.to_datetime(df2['End Time'])
    df = df2.sort_values(by='Start Time')

    # For each Start Time create additional columns to store year, month, day_of_week and hour
    # df['Start Year'] = df['Start Time'].apply(lambda x: get_part_of_datetime(x, 'year'))
    df['Start Month'] = df['Start Time'].apply(lambda x: get_part_of_datetime(x, 'month'))
    df['Start Day'] = df['Start Time'].apply(lambda x: get_part_of_datetime(x, 'day_of_week'))
    df['Start Hour'] = df['Start Time'].apply(lambda x: get_part_of_datetime(x, 'hour'))

    # filter month if month is not all
    if month.title() != 'All':
        df = df.loc[df['Start Month'] == month.title()]

    # filter day if day is not all
    if day.title() != 'All':
        df = df.loc[df['Start Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        common_month = df['Start Month'].value_counts()[df['Start Month'].value_counts()
                                                        == df['Start Month'].value_counts().max()]
        print(common_month)
        print('\n')
        # display the most common day of week
        day_of_week = df['Start Day'].value_counts()[df['Start Day'].value_counts()
                                                     == df['Start Day'].value_counts().max()]
        print(day_of_week)
        print('\n')
        # display the most common start hour
        most_common_hour = df['Start Hour'].value_counts()[df['Start Hour'].value_counts()
                                                           == df['Start Hour'].value_counts().max()]
        print(most_common_hour)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('Sorry there was an error whiles processing your request')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        most_common_start_station = df['Start Station'].value_counts()[df['Start Station'].value_counts()
                                                                       == df['Start Station'].value_counts().max()]

        print(most_common_start_station)
        print('\n')
        # display most commonly used end station
        most_common_end_station = df['End Station'].value_counts()[df['End Station'].value_counts()
                                                                   == df['End Station'].value_counts().max()]
        print(most_common_end_station)
        print('\n')

        # display most frequent combination of start station and end station trip
        df['Start End Stations'] = df[['Start Station', 'End Station']].apply(lambda x: ' - '.join(x), axis=1)
        most_common_start_end_station = df['Start End Stations'].value_counts()[df['Start End Stations'].value_counts()
                                                                                == df['Start End Stations'].
                                                                                value_counts().max()]
        print(most_common_start_end_station)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('Sorry there was an error whiles processing your request')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    try:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        total = df['Trip Duration'].sum()
        print('The total travel duration is ' + str(total))
        print('\n')
        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print('Total mean travel time is: ' + str(mean_travel_time))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('Sorry there was an error whiles processing your request')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types)
        print('\n')
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)
        print('\n')
        # Display earliest, most recent, and most common year of birth

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('Sorry there was an error whiles processing your request')


def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
