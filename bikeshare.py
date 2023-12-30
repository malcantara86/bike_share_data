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
        choice = input("Choose the number of the city you want to analyze: "+
                     "\n[1] Chicago \n [2] New York City \n [3] Washington\nChoice: ")
        
        if choice == '1':
            city = 'chicago'
        elif choice == '2':
            city = 'new york city'
        elif choice == '3':
            city = 'washington'
        else:
            city = 'invalid city'
        
        # validate city to make sure we have the correct data
        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid city.")
            continue
        else:
            break

    # ask use if he/she wants to filter by month or day
    while True:
        filter_choice = input("\nWould you like to filter the data by:\n[1] month\n[2] day\n[3] Select all (no filter)?\nChoice: ")

        if filter_choice == '1':
            filter = 'month'
        elif filter_choice == '2':
            filter = 'day'
        elif filter_choice == '3':
            filter = 'all'
        else:
            filter = 'invalid'

        # make sure user selects within the choices
        if filter not in ('month', 'day', 'all'):
            print("Please enter a valid number within the choices.")
            continue
        else:
            break       

    if filter == 'month':
        # get user input for month (all, january, february, ... , june)
        while True:
            month_choice = input("\nChoose the number of which month you want to analyze for " + city.title() + 
                        "\n[1] January\n[2] February\n[3] March\n[4] April\n[5] May\n[6] June\nChoice: ")

            if month_choice == '1':
                month = 'january'
            elif month_choice == '2':
                month = 'february'
            elif month_choice == '3':
                month = 'march'
            elif month_choice == '4':
                month = 'april'
            elif month_choice == '5':
                month = 'may'
            elif month_choice == '6':
                month = 'june'                
            else:
                month = 'invalid'
            
            # make sure user selects within the choices
            if month not in ('january', 'february', 'march', 'april', 'may', 
                            'june', 'all'):
                print("Please enter a valid number within the choices.")
                continue
            else:
                break

    elif filter == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day_choice = input("\nChoose a day to analyze:" +
                        "\n[1] Monday\n[2] Tuesday\n[3] Wednesday\n[4] Thursday\n[5] Friday\n[6] Saturday\n[7] Sunday\nChoice: ")
            
            if day_choice == '1':
                day = 'monday'
            elif day_choice == '2':
                day = 'tuesday'
            elif day_choice == '3':
                day = 'wednesday'
            elif day_choice == '4':
                day = 'thursday'
            elif day_choice == '5':
                day = 'friday'
            elif day_choice == '6':
                day = 'saturday'
            elif day_choice == '7':
                day = 'sunday'              
            else:
                day = 'invalid'
            
            # invalid input handling for month
            if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                        'saturday', 'sunday'):
                print("Please enter a valid number within the choices.")
                continue
            else:
                break

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


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)

        choice = input("\nWould you like to analyze more data? [y/n]")
        if choice.lower() != 'y':
            break


if __name__ == "__main__":
	main()
