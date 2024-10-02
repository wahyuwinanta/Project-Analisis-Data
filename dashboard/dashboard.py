import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Bike Sharing Analysis Dashboard')

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df_hour = load_data()

st.sidebar.title("Navigation")
option = st.sidebar.selectbox('Select a question to analyze:', 
                              ('How does weather condition affect bike rentals?', 
                               'What is the seasonal impact on bike rentals?',
                               'How does registered vs casual users compare?'))

# Visualization 1: Weather condition vs bike rentals
if option == 'How does weather condition affect bike rentals?':
    st.subheader("Weather Condition vs Bike Rentals")

    weather_mapping = {
        1: 'Clear, Few clouds',
        2: 'Mist, Cloudy',
        3: 'Light Snow, Rain',
        4: 'Heavy Rain, Snow, Fog'
    }
    df_hour['weather_name'] = df_hour['weathersit'].map(weather_mapping)

    avg_rentals_by_weather = df_hour.groupby('weather_name')['cnt'].mean()
    
    fig, ax = plt.subplots()
    avg_rentals_by_weather.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Average Bike Rentals by Weather Condition')
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Average Rentals')
    
    st.pyplot(fig)

# Visualization 2: Seasonal impact on bike rentals
elif option == 'What is the seasonal impact on bike rentals?':
    st.subheader("Seasonal Impact on Bike Rentals")

    # Mapping seasons
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Fall', 4: 'Summer'}
    df_hour['season_name'] = df_hour['season'].map(season_mapping)

    # Group by season and sum the rental counts
    total_rentals_by_season = df_hour.groupby('season_name')['cnt'].sum()

    # Create a figure with figsize similar to the notebook
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot the line chart
    total_rentals_by_season.plot(kind='line', marker='o', color='purple', ax=ax)
    
    # Setting titles and labels
    ax.set_title('Total Bike Rentals by Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Rentals')
    
    # Add grid for better visualization
    ax.grid()

    # Adjust the layout to ensure everything fits well
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)



# Visualization 3: Registered vs Casual users
else:
    st.subheader("Registered vs Casual Users in Bike Rentals")

    avg_rentals_by_user_type = df_hour[['casual', 'registered']].mean()

    fig, ax = plt.subplots()
    avg_rentals_by_user_type.plot(kind='bar', color=['lightblue', 'salmon'], ax=ax)
    ax.set_title('Average Bike Rentals by User Type')
    ax.set_xlabel('User Type')
    ax.set_ylabel('Average Rentals')

    st.pyplot(fig)
