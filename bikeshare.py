import calendar
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    month = 'all'
    day = 'all'
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Choose the number of the city you want to analyze: "+
                     "\nChicago\nNew York City\nWashington\nChoice: ")
        city = city.lower()
               
        # validate city to make sure we have the correct data
        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid city.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nChoose the number of which month you want to analyze for " + city.title() + 
                    "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nAll\nChoice: ")
        month = month.lower()
      
        # make sure user selects within the choices
        if month not in ('january', 'february', 'march', 'april', 'may', 
                        'june', 'all'):
            print("Please enter a valid number within the choices.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nChoose a day to analyze:" +
                    "\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday\nAll\nChoice: ")
        day = day.lower()
               
        # invalid input handling for month
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday', 'all'):
            print("Please enter a valid number within the choices.")
            continue
        else:
            break

    print('========================================================================================')
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
    # read the data of the selected city, and add it to panda's dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extraction of month and day and create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    
    # filter by month if month is selected
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    # filter by day if day is selected
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) 
        df = df[df['Weekday'] == day]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for', city.title(), '...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = calendar.month_name[df['Month'].mode()[0]]

    print('The most popular month: ', most_popular_month, '\n')


    # display the most common day of week    
    most_popular_day = calendar.day_name[df['Weekday'].mode()[0]]
    print('The most common day of the week: ', most_popular_day, '\n')

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = int(df['Start Hour'].mode()[0])
    
    if popular_hour >= 12:
        if (popular_hour == 12):
            most_popular_hour_text = '12 PM'
        else:
            most_popular_hour_text = str((popular_hour%12)) + " PM"
    else:
        most_popular_hour_text = str(popular_hour) + " AM"

    print('The most common start hour: ', most_popular_hour_text, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('========================================================================================')


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip for', city.title(), '...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].value_counts().idxmax(), '\n')

    # display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].value_counts().idxmax(), '\n')

    # display most frequent combination of start station and end station trip
    # create new col and combine start and end stations

    df['Combined Station'] = 'Start station: ' + df['Start Station'] + ' End Station: ' + df['End Station']

    print('Most commonly used combination: ', 
          df['Combined Station'].value_counts().idxmax(), '\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('========================================================================================')


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration for', city.title(), '...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = df['Trip Duration'].sum()
    
    total_time_in_hr = round(total_time_sec / 60 / 60 ,0)
    
    # print total travel time
    print('Total travel time: ', total_time_in_hr, 'hours\n')

    # display mean travel time
    total_mean_in_sec = df['Trip Duration'].mean()
    total_mean_in_minutes = round(total_mean_in_sec / 60  ,0)    

    if total_mean_in_minutes < 60:
        print('Mean travel time: ', total_mean_in_minutes, 'minutes.\n\n')
    else:
        total_mean_in_hrs = round(total_mean_in_minutes / 60 ,1)
        print('Mean travel time: ', total_mean_in_hrs, 'hours.\n\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('========================================================================================')


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for', city.title(), '...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].values
   
    # count the occurences of each different user types
    num_of_subscribers  = (user_types == 'Subscriber').sum()
    num_of_customers = (user_types == 'Customer').sum()
    
    # print user type counts
    print('Number of subscribers: ',num_of_subscribers,'\n')
    print('Number of customers: ',num_of_customers,'\n')

    # Display earliest, most recent, and most common year of birth
    # Don't process if city is Washington, since Gender is not available

    if city.title() != 'Washington':
        # get gender
        gender = df['Gender'].values       
        # count the number of each gender
        num_of_male  = (gender == 'Male').sum()
        num_of_female = (gender == 'Female').sum()
        
        # print number of users for each gender
        print('Number of male users: ', num_of_male,'\n')
        print('Number of female users: ', num_of_female,'\n')
        
        # get birth year
        birth_year = df['Birth Year'].values
        
        # use numpy to exlude NaN
        unique_birth_year = np.unique(birth_year[~np.isnan(birth_year)])
        
        # the maximum value for birth year will be the most recent
        most_recent_birth_year = unique_birth_year.max()
        
        # the minimum value for birth year will be the earliest
        earliest_birth_year = unique_birth_year.min()
        
        # print most recent and earliest birth year
        print('Most recent birth year of users: ', most_recent_birth_year ,'\n')
        print('Earliest birth year of users: ', earliest_birth_year,'\n')   
        
        # display most common birth year
        print('Most common birth year of users: ', df['Birth Year'].value_counts().idxmax(), '\n')
    
    else:
        print('Gender and birth year data are not available for Washington.')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('========================================================================================')

def display_raw_data(df):
    """ Displays 5 lines of raw data at a time when yes is selected."""
    # define index i, start at line 1
    i = 1
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
        if view_data.lower() == 'yes':
            # print current 5 lines
            print(df[i:i+5])
            i = i+5
            
        else:
            # break when no is selected
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        display_raw_data(df)

        choice = input("\nWould you like to analyze more data? [y/n]")
        if choice.lower() != 'y':
            break


if __name__ == "__main__":
	main()
