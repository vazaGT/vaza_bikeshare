import time
import pandas as pd
import numpy as np
import tabulate as tabulate
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please type the name of the city to explore!\nChicago, New York City or Washington: ').lower()
    # holds the user's choice for the city they want to see data for
    while city not in CITY_DATA.keys():
        city = input('Please type the name of the city to explore!\nChicago, New York City or Washington: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Type a month from January to June or "all": ').lower()
    # holds the user's choice for the month they want to see data for
    while month not in months:
        month = input('Type a month from January to June or "all": ').lower()
    print('Choose a day of the week: ')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Type a day of the week or "all": ').lower()
    # holds the user's choice for the day they want to see data for

    while day not in weekdays:
        day = input('Type a day of the week or "all": ').lower()
    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])
    df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].apply(pd.to_datetime)
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Trip'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']

    if month != 'all':
        # filter by month of the week to create a new dataframe
        df = df[df['Month'] == month.capitalize()]
    # filter by day if applicable
    if day != 'all':
        # filter by day of the week to create a new dataframe
        df = df[df['Day'] == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displays the most common month
    most_common_month = df['Month'].mode()[0]  # holds the name of the month with most trips
    print(f'The most common month is: {most_common_month}')

    # displays the most common day of week
    most_common_day = df['Day'].mode()[0]  # holds the name of the day with most trips
    print(f'The most common day is: {most_common_day}')

    # displays the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]  # holds the hour at which the most of the trips starts
    print(f'The most common start hour is: {most_common_hour}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station

    sstations = df.groupby(['Start Station'])['Start Station'].count()
    smaxval = sstations.values.max()  # holds the maximum value in the series
    smaxindex = sstations.idxmax()  # holds the index of the maximum value of the series
    print(f'The most common Start Station is:  {smaxindex} with {smaxval} trips')

    # displays most commonly used end station
    estations = df.groupby(['End Station'])['End Station'].count()
    emaxval = estations.values.max()  # holds the maximum value in the series
    emaxindex = estations.idxmax()  # holds the index of the maximum value of the series
    print(f'The most common End Station is:  {emaxindex} with {emaxval} trips')

    # displays most frequent combination of start station and end station trip
    trip = df.groupby(['Trip'])['Trip'].count()
    trmaxval = trip.values.max()  # holds the maximum value in the series
    trindex = trip.idxmax()  # holds the index of the maximum value of the series
    print(f'The most popular trip is:  {trindex} with {trmaxval} trips')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and the average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    total_trip_duration = int(df[
                                  'Trip Duration'].sum() / 3600)  # holds the integer value of the sum of all trips durations converted to hours
    print(f'The total trip duration is:  {total_trip_duration} hours')

    # displays mean travel time
    avg_trip_duration = int(
        df['Trip Duration'].mean() / 60)  # holds the integer value of the average trip duration converted to minutes
    print(f'The average trip duration is:  {avg_trip_duration} minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print(f'{user_types.index[0]} - {df["User Type"].value_counts()[0]}')
    print(f'{user_types.index[1]} - {df["User Type"].value_counts()[1]}')
    print('\n')

    # Displays counts of gender
    try:
        gender_types = df['Gender'].value_counts()  # holds pandas series with the count of the users from each gender
        print(gender_types.index[0], gender_types[0])
        print(gender_types.index[1], gender_types[1])
        print('\n')

        # Display earliest, most recent, and most common year of birth

        earliest_birth_year = int(df['Birth Year'].min())
        print(f'The earliest birth year is: {earliest_birth_year}')

        recent_birth_year = int(df['Birth Year'].max())
        print(f'The most recent birth year is: {recent_birth_year}')

        median_birth_year = int(df['Birth Year'].median())
        print(f'The most common birth year is: {median_birth_year}')
    except:
        print('There is no gender data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def print_data_frame(df):
    """
    Prints parts of the dataframe if requested by the user
    Args:
        (Pandas DataFrame) df -  containing city data filtered by month and day

    Returns: prints out 5 lines form the dataframe

    """

    i = df.shape[0]  # holds the number of the rows of the dataframe
    lines_counter = 0
    choice = ['yes', 'no']  # holds the valid options for the user's input
    show_table = input('Would you like to see the dataframe? Type "yes" or "no": ')  # takes the user's input
    while show_table.lower() not in choice:
        show_table = input('Would you like to see the dataframe? Type "yes" or "no": ')
    if show_table.lower() == 'yes':
        print(df[lines_counter:lines_counter + 5])
        while counter < i:
            # prints out next 5 lines from the dataframe or quits printing as per the user's preference
            meer = input('Do you want 5 more?')  # user's continuation input
            if meer == 'yes':
                lines_counter += 5
                print(df[lines_counter:lines_counter + 5])
            elif meer == "no":
                break
            else:
                print('Invalid entry: Type "yes" or "no"')
                continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data_frame(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
