import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Defining lists globally to check if user input entered is valid:
cities = ['chicago', 'new york', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

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
            city = input('Enter the city name to be explored: (chicago, new york or washington)\n').lower()
            if city in cities:
                print('\nInput Accepted...')
                break
            else:
                print('\nKindly enter the correct city name!')

    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('Enter the month according to which data should be filtered: (January to June)\nNote: Enter "all" for no filter\n').lower()
            if month in months:
                print('\nInput Accepted...')
                break
            else:
                print('\nKindly enter the correct month or enter "all" to explore data for all months!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Enter the day according to which data should be filtered: (Monday to Sunday)\nNote: Enter "all" for no filter\n').lower()
            if day in days:
                print('\nInput Accepted...')
                break
            else:
                print('\nKindly enter the correct day or enter "all" to explore data for all days!')

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
	#Load data into df based on the city entered by user:
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime object:
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns:
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable:
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

	# convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
	#Extract month from Start Time column:
    df['month'] = df['Start Time'].dt.month
	#Check for maximum occurrences in new month column:
    common_month = df['month'].mode()[0]
    print('Most Common Month of travel is:', common_month)

    # display the most common day of week
	#Extract day name from Start Time column:
    df['weekday'] = df['Start Time'].dt.weekday_name
	#Check for maximum occurrences in new weekday column:
    common_day = df['weekday'].mode()[0]
    print('\nMost Common Day of travel is: ', common_day)

    # display the most common start hour
	#Extract hours from Start Time column:
    df['hours1'] = df['Start Time'].dt.hour
    #Check for maximum occurrences in new hours1 column:
    common_hours = df['hours1'].mode()[0]
    print('\nMost Common Hour of travel is:', common_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stns = df['Start Station'].value_counts().idxmax()
    print('\nThe Most Common Start Station is: ', start_stns)

    # display most commonly used end station
    end_stns = df['End Station'].value_counts().idxmax()
    print('\nThe Most Common End Station is: ', end_stns)

    # display most frequent combination of start station and end station trip
	#Define start_end_stns as combinantion of start & end station
    start_end_stns = df['Start Station'] + ', ' + df['End Station']
    #Find mode of start_end_stns i.e. most occuring combination..
    common_start_end_stns = start_end_stns.mode()
	#Print the most frequently occurring combinantion of start and end stations:
    print('\nThe Most Common Start & End Station combination is:\n{}'.format(common_start_end_stns[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The Total travel time of all trips is: ', total_time)

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('The Average travel time of all trips is: ', avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_user_data(df):
    """Displays raw user data depending upon user input."""

    #Global setting to enable all columns to be displayed
    pd.set_option('display.max_columns', None)
    #Fetch the number of rows in data
    row_count = df.shape[0]

    #For loop to keep printing the next 5 rows depending upon user input
    for i in range(0, row_count, 5):
        print('\nPrinting the raw data...')
        print(df.iloc[i: i + 5, : ])
        answer = input('\nDo you want to print the next 5 rows?\nPlease enter "yes" or "no"\n').lower()
        if answer != 'yes':
            break


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of different types of users are: ')
    user_count = df['User Type'].value_counts()
	#Using for loop to print the index & count of each type of user:
    for i, count in enumerate(user_count):
        print('{} : {} '.format(user_count.index[i], count))

	#Display counts of gender
	#In washington.csv, there are no columns for gender & birth year.
	#Check if data has 'Gender' column:
    if 'Gender' in df.columns:
    # Display counts of gender
        print('\nThe count of people based on gender are: ')
        gender_count = df['Gender'].value_counts()
        #Using for loop to print the index & count of each gender:
        for i, count in enumerate(gender_count):
            print('{} : {} '.format(gender_count.index[i], count))

	#Display earliest, most recent, and most common year of birth
	#Check if df has 'Birth Year' column:
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        #earliest year:
        earliest = birth_year.min()
        print('\nThe earliest year of birth is: ', int(earliest))
        #most_recent year:
        most_recent = birth_year.max()
        print('The most recent year pf birth is: ', int(most_recent))
        #Most_common year:
        most_common = birth_year.value_counts().idxmax()
        print('The most common year of birth is: ', int(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_user_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
