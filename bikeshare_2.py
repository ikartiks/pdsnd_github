import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
days = ['monday', 'tuesday', 'wednesday', 'thursday','friday','saturday', 'sunday']



def get_filters():

    

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please enter a city: ").lower()
            if(city in CITY_DATA.keys()):
                break
            print("Oops!  That was no valid city.  Try again...")
        except Exception as e:
            print("Oops!  That was no valid city.  Try again...")


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a month: ").lower()
            if(month in months or month == 'all'):
                break
            print("Oops!  That was no valid month.  Try again...")
        except Exception as e:
            print("Oops!  That was no valid month.  Try again...")



    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter a day: ").lower()
            if(day in days or day  == 'all'):
                break
            print("Oops!  That was no valid day.  Try again...")
        except Exception as e:
            print("Oops!  That was no valid day.  Try again...")


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

    df = pd.read_csv(CITY_DATA[city])

    #print(df['Start Time'].dtype)

    df['stratDate'] = pd.to_datetime(df['Start Time'])
    
    if month != 'all':
        df = df[df['stratDate'].dt.month == months.index(month)+1]
    
    if day != 'all':
        df = df[df['stratDate'].dt.day_of_week == days.index(day)]
    #print(df.describe())
    #print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    monthIndex = (df['stratDate'].dt.month.mode()[0])
    print("most common month {}".format(months[monthIndex-1]))

    # display the most common day of week
    print("most common day {}".format(days[df['stratDate'].dt.dayofweek.mode()[0]]))

    # display the most common start hour
    print("most common hour {}".format(df['stratDate'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ("Start station is {}".format(df['Start Station'].mode()))


    # display most commonly used end station
    print ("End station is {}".format(df['End Station'].mode()))


    # display most frequent combination of start station and end station trip
    counts = df.groupby(["Start Station", "End Station"])["End Station"].count().reset_index(name="count")
    
    counts = counts.sort_values('count', ascending=False)
    #print(counts)
    print("start + end {}".format(counts.iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['endDate'] = pd.to_datetime(df['End Time'])
    df['travel_time_mins'] = (df['endDate'] - df['stratDate']).dt.total_seconds() / 60 

    # display total travel time
    print("total travel time - {} mins".format(df['travel_time_mins'].sum()))

    # display mean travel time
    print("mean travel time - {} mins".format(df['travel_time_mins'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print (df['User Type'].value_counts())


    # Display counts of gender
    if 'Gender' in df.columns:
        print (df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print ("Earliest - {}, Recent - {} and most common birth year - {}".format(df['Birth Year'].min(),df['Birth Year'].max(),df['Birth Year'].mode()))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no')
    start_loc = 0
    while (view_data.lower() == 'yes'):
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()

        #print('{} {} {}'.format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
