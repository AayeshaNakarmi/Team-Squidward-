import streamlit as st
import pandas as pd
import constants
import matplotlib.pyplot as plt

emission_data = pd.read_csv("carbon.csv")

# Create an empty DataFrame to store user responses
user_responses_df = pd.DataFrame(columns=["Question", "Response"])  # Initialize an empty DataFrame

def introduction():
    st.header("Welcome to the Carbon Footprint Calculator!")
    st.write("This calculator will help you estimate your carbon footprint based on your daily activities.")

    st.header("Select Your Country🌎")
    user_country = st.selectbox("Select your country:", emission_data["Country Name"])
    st.session_state.user_country = user_country  # Store the user's country in session state

def transportation():
    global user_responses_df
    st.header("Transportation🚗")
    st.write("Let's learn about your transportation habits.")

    # Initialize session state attributes
    if "transportation_mode" not in st.session_state:
        st.session_state.transportation_mode = None
    if "car_type" not in st.session_state:
        st.session_state.car_type = None
    if "car_size" not in st.session_state:
        st.session_state.car_size = None
    if "transportation_frequency" not in st.session_state:
        st.session_state.transportation_frequency = None

    # Add questions about transportation here
    transportation_mode = st.selectbox("Select your primary mode of transportation:", ["Two-wheeler","Public Transport", "Bicycle","Car", "Walking"])
    st.session_state.transportation_mode = transportation_mode  # Store the transportation mode in session state
    
    if transportation_mode=="Car":
        car_type=st.selectbox("What type of car do you use?",["Petrol","Diesel","Electric"])
        st.session_state.car_type = car_type  

        car_size = st.selectbox("What is the size of your car?", ["Two-seater", "Regular", "SUV", "Minivan"])
        st.session_state.car_size = car_size 


    transportation_frequency = st.selectbox("How often do you use this mode of transportation?", ["Daily", "Weekly", "Monthly"])
    st.session_state.transportation_frequency = transportation_frequency 

    # Append the user's responses for the "Transportation" step to the DataFrame
    responses = [("Transportation Mode", transportation_mode)]
    if transportation_mode == "Car":
        responses.append(("Car Type", car_type))
        responses.append(("Car Size", car_size))
    responses.append(("Transportation Frequency", transportation_frequency))
    
    user_responses_df = pd.concat([user_responses_df, pd.DataFrame(responses, columns=["Question", "Response"])])  # Concatenate DataFrames



def electricity():

    st.header("Electricity💡")
    st.write("Let's learn about your electricity consumption.")

    # Add questions about electricity consumption here
    electricity_consumption = st.selectbox("Would you consider your electricity consumption to be:", ["Less than average", "Average", "More than average"])
    st.session_state.electricity_consumption=electricity_consumption

     # Append the user's responses for the "Electricity" step to the DataFrame
    global user_responses_df
    responses = [("Electricity Consumption", electricity_consumption)]
    user_responses_df = pd.concat([user_responses_df, pd.DataFrame(responses, columns=["Question", "Response"])])  # Concatenate DataFrames
    

def diet():
    st.header("Diet🥩")
    st.write("Let's learn about your diet habits.")

    # Add questions about diet here
    meat_consumption = st.selectbox("How often do you consume meat?", ["Rarely or Never", "Occasionally", "Regularly", "Frequently"])
    st.session_state.meat_consumption=meat_consumption

     # Append the user's responses for the "Diet" step to the DataFrame
    responses = [("Meat Consumption", meat_consumption)]
    global user_responses_df
    user_responses_df = pd.concat([user_responses_df, pd.DataFrame(responses, columns=["Question", "Response"])])  # Concatenate DataFrames

    
    



def clothing():
    st.header("Clothing and Shopping Habits👕")
    st.write("Let's learn about your clothing consumption and shopping habits.")

    # Add questions about clothing and shopping here
    fast_fashion = st.radio("Do you often buy fast fashion items?", ["Yes", "No"])
    st.session_state.fast_fashion=fast_fashion
    
    st.write("Which of the following do you consider while shopping for clothing? (Select all that apply)")
    
    sustainable_check = st.checkbox("Sustainability")
    st.session_state.sustainable_check=sustainable_check

    price_check = st.checkbox("Budget")
    st.session_state.price_check=price_check

    brand_check = st.checkbox("Brand Reputation and Values")
    st.session_state.brand_check=brand_check

    material_check = st.checkbox("Material quality")
    st.session_state.material_check=material_check

    style_check = st.checkbox("Style")
    st.session_state.style_check=style_check

    purchase_frequency = st.selectbox("How often do you buy new clothing items?", ["Rarely or Never", "Occasionally", "Regularly", "Frequently"])
    st.session_state.purchase_frequency=purchase_frequency

    # Append the user's responses for the "Clothing" step to the DataFrame
    responses = [
        ("Fast Fashion", fast_fashion),
        ("Sustainability Check", sustainable_check),
        ("Price Check", price_check),
        ("Brand Check", brand_check),
        ("Material Quality Check", material_check),
        ("Style Check", style_check),
        ("Purchase Frequency", purchase_frequency)
    ]
    global user_responses_df
    user_responses_df = pd.concat([user_responses_df, pd.DataFrame(responses, columns=["Question", "Response"])], ignore_index=True)  # Concatenate DataFrames



def housing():
    st.header("Housing🏠")
    st.write("Let's learn about your housing-related emissions.")

    # Add questions about housing here
    heating_source = st.selectbox("What is your primary heating source?", ["Electricity", "Natural Gas", "Oil", "Other"])
    st.session_state.heating_source=heating_source

    heating_usage = st.selectbox("How would you describe your average monthly heating usage?", ["Low", "Moderate", "High"])
    st.session_state.heating_usage=heating_usage

    appliances_usage = st.selectbox("How would you describe your average monthly electricity usage for appliances?", ["Low", "Moderate", "High"])
    st.session_state.appliances_usage=appliances_usage

    # Append the user's responses for the "Housing" step to the DataFrame
    responses = [
        ("Heating Source", heating_source),
        ("Heating Usage", heating_usage),
        ("Appliances Usage", appliances_usage)
    ]
    global user_responses_df
    user_responses_df = pd.concat([user_responses_df, pd.DataFrame(responses, columns=["Question", "Response"])], ignore_index=True)  # Concatenate DataFrames



def calculate_total_emissions():
    total_emissions=0.0

    emissions = []

    transportation_emission = transportation_emissions(st.session_state.transportation_mode, st.session_state.car_type, st.session_state.car_size)
    emissions.append(transportation_emission)

    electricity_emission = electricity_emissions(st.session_state.electricity_consumption)
    emissions.append(electricity_emission)

    meat_emission = diet_emissions(st.session_state.meat_consumption)
    emissions.append(meat_emission)

    clothing_emission = clothing_emissions()
    emissions.append(clothing_emission)

    housing_emission = housing_emissions(st.session_state.heating_source, st.session_state.heating_usage, st.session_state.appliances_usage)
    
    emissions.append(housing_emission)
    
    total_emissions += (transportation_emission+electricity_emission+meat_emission+clothing_emission+housing_emission)/1000

    # Consider transportation frequency while calculating emissions
    if st.session_state.transportation_frequency == "Daily":
        total_emissions *= 365
    elif st.session_state.transportation_frequency == "Weekly":
        total_emissions *=52
    else:
        total_emissions *= 12  # Monthly

    total_emissions = round(total_emissions, 2)
    st.session_state.total_emissions = total_emissions  # Initialize total_emissions in session_state

    st.write("Your total carbon emission: ",total_emissions)

     # Append the final result to the user_responses_df using pd.concat
    result_df = pd.DataFrame([["Total Emissions", total_emissions]], columns=["Question", "Response"])
    global user_responses_df
    user_responses_df = pd.concat([user_responses_df, result_df], ignore_index=True)

    # Save user responses to a CSV file
    user_responses_df.to_csv("user_responses.csv", index=False)  # Save the DataFrame to a CSV file
    return emissions, total_emissions

def show_results():
    global user_responses_df
    st.header("Results")

    if "user_country" not in st.session_state:
        st.error("Please complete the Introduction section first.")
        return
    
    user_country = st.session_state.user_country

    # Calculate the country's average emission
    country_average = emission_data[emission_data["Country Name"] == user_country]["2020"].values[0]

    
    st.write(f"Your estimated carbon footprint: {st.session_state.total_emissions} metric ton CO2")

    if pd.notna(country_average):
        # country_average = country_average[0]
        st.write(f"{user_country}'s average carbon footprint: {country_average:.2f} metric ton CO2")
    else:
        st.write(f"Average data not available for {user_country}.")
        

    difference = st.session_state.total_emissions - country_average
    if difference > 0:
        st.write(f"Your footprint is {difference:.2f} metric ton CO2 higher than the average.")
    elif difference < 0:
        st.write(f"Your footprint is {-difference:.2f} metric ton CO2 lower than the average.")
    else:
        st.write("Your footprint is exactly equal to the average.")

    



    
def transportation_emissions(transportation_mode, car_type, car_size):
    emission_factor = constants.transportation_emission_factors[transportation_mode]

    if transportation_mode == "Car" and car_type in emission_factor:
        car_emission_factor = emission_factor[car_type]
        if car_type == "Electric":
            return 0.0  # Electric cars have zero emissions
        elif car_size in car_emission_factor:
            return car_emission_factor[car_size]  # Return the appropriate emission factor
    else:
        return emission_factor  # Emission factor for non-car transportation modes

def electricity_emissions(electricity_consumption):
    emission_factor=constants.electricity_emission_factors[electricity_consumption]
    return emission_factor


def diet_emissions(meat_consumption):
    emission_factor=constants.diet_emission_factors[meat_consumption]
    return emission_factor

def clothing_emissions():
    clothing_emissions = 0.0

    for factor, value in constants.clothing_emission_factors.items():
        if factor == "purchase_frequency" and st.session_state.purchase_frequency:
            purchase_frequency_emission = value[st.session_state.purchase_frequency]
            clothing_emissions += purchase_frequency_emission
        
        if factor == "fast_fashion" and st.session_state.fast_fashion:
            fast_fashion_emission = value[st.session_state.fast_fashion]
            clothing_emissions += fast_fashion_emission
        
        if factor in st.session_state:
            factor_selection = st.session_state[factor]  # Get the user's selection for the factor
            factor_emission = value[factor_selection]    # Get the corresponding emission factor
            clothing_emissions += factor_emission        # Add the emission factor to the total

    
    return clothing_emissions


def housing_emissions(heating_source, heating_usage, appliances_usage):
    emission_factor = 0.0

    for factor_type, factor_values in constants.housing_emission_factors.items():
        if factor_type == "heating_source" and heating_source in factor_values:
            emission_factor += factor_values[heating_source]
        if factor_type == "heating_usage" and heating_usage in factor_values:
            emission_factor += factor_values[heating_usage]
        if factor_type == "electrical_appliances_usage" and appliances_usage in factor_values:
            emission_factor += factor_values[appliances_usage]

    return emission_factor


def visualize_emissions():
    st.header("Visualizations")

    emissions, total_emission = calculate_total_emissions()

    # Labels for the pie chart
    labels = ["Transportation", "Electricity", "Diet", "Clothing", "Housing"]

    # Emission values for each category
    emission_values = [emissions[0], emissions[1], emissions[2], emissions[3], emissions[4]]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(emission_values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart in Streamlit
    st.pyplot(fig)


def visualization():



    # Calculate total emissions
    emissions = {
        "Transportation":transportation_emissions(st.session_state.transportation_mode, st.session_state.car_type, st.session_state.car_size),
        "Electricity":electricity_emissions(st.session_state.electricity_consumption),
        "Diet":diet_emissions(st.session_state.meat_consumption),
        "Clothing": clothing_emissions(),
        "Housing": housing_emissions(st.session_state.heating_source, st.session_state.heating_usage, st.session_state.appliances_usage),

    }
    # Create a Streamlit section for visualizations
    st.header("Visualizations")

    # Create a simple pie chart using Matplotlib
    fig, ax = plt.subplots()
    ax.pie(emissions.values(), labels=emissions.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Carbon Emissions by Sector")

    # Display the chart in Streamlit
    st.pyplot(fig)

    # Display the calculated emissions for each sector to the user
    st.subheader("Carbon Emissions by Sector")
    for sector, emission in emissions.items():
        st.write(f"{sector}: {emission:.2f} metric ton CO2e")


