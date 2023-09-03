import functions
from langchain.llms import Clarifai
import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import functions

from constants import (
    transportation_emission_factors,
    electricity_emission_factors,
    diet_emission_factors,
    housing_emission_factors,
)

def recommendation():
    st.header("Recommendation")

        

    ######################################################################################################
    # In this section, we set the user authentication, user and app ID, model details, and the URL of 
    # the text we want as an input. Change these strings to run your own example.
    ######################################################################################################

    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = 'f2383ffd276f4981ae6df4dd60196902'
    # Specify the correct user_id/app_id pairings
    # Since you're making inferences outside your app's scope
    USER_ID = 'meta'
    APP_ID = 'Llama-2'
    # Change these to whatever model and text URL you want to use
    MODEL_ID = 'llama2-13b-chat'
    MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

    ############################################################################
    # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
    ############################################################################

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            url=TEXT_FILE_URL
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Completion:\n")
    print(output.data.text.raw)


    
    template = """Consider these:
    primary transportation source: {transportation_mode}, if it is car, it is {car_type} car, of size {car_size},
    and transportation usage frequency is: {transportation_frequency}
    usage of electricity: {electricity_consumption},
    meat consumption: {meat_consumption},
    fast fashion: {fast_fashion},
    for clothing, these things are considered: {sustainable_check}, {price_check}, {brand_check}, {material_check}, {style_check},
    clothing purchase frequency is: {purchase_frequency},
    heating source: {heating_source},
    heating usage: {heating_usage},
    electrical appliance usage: {appliances_usage}
    calculate the carbon emission in metric ton based on these data. it doesn't have to be perfectly accurate but create an estimate. Also tell how much it is more or less than the {country}'s average co2 per capita. Write it as "Your total carbon emission is". 
    also give me ideas on how to reduce my carbon footprint.
    """


    
    llm=Clarifai(pat='f2383ffd276f4981ae6df4dd60196902',user_id='meta',app_id='Llama-2',model_id='llama2-13b-chat')

    # generating response using LLM
    response = llm(template.format(
    transportation_mode=st.session_state.transportation_mode,
    car_type=st.session_state.car_type,
    car_size=st.session_state.car_size,
    transportation_frequency=st.session_state.transportation_frequency,
    electricity_consumption=st.session_state.electricity_consumption,
    meat_consumption=st.session_state.meat_consumption,
    fast_fashion=st.session_state.fast_fashion,
    sustainable_check=st.session_state.sustainable_check,
    price_check=st.session_state.price_check,
    brand_check=st.session_state.brand_check,
    material_check=st.session_state.material_check,
    style_check=st.session_state.style_check,
    purchase_frequency=st.session_state.purchase_frequency,
    heating_source=st.session_state.heating_source,
    heating_usage=st.session_state.heating_usage,
    appliances_usage=st.session_state.appliances_usage,
    country=st.session_state.user_country
    ))

    # print(response)
    return response


 
    
# def visualization():
   
#     # # User inputs (you can add these using st.sidebar components)
#     # user_transportation_mode = st.selectbox("Select Transportation Mode", list(transportation_emission_factors.keys()))
#     # user_electricity_usage = st.selectbox("Select Electricity Usage", list(electricity_emission_factors.keys()))
#     # user_diet = st.selectbox("Select Diet", list(diet_emission_factors.keys()))
#     # user_heating_source = st.selectbox("Select Heating Source", list(housing_emission_factors["heating_source"].keys()))
#     # user_heating_usage = st.selectbox("Select Heating Usage", list(housing_emission_factors["heating_usage"].keys()))
#     # user_appliances_usage = st.selectbox("Select Appliances Usage", list(housing_emission_factors["electrical_appliances_usage"].keys()))

#     # Calculate total emissions
#     emissions = {
#         "Transportation": functions.transportation_emissions,
#         "Electricity": functions.electricity_emissions,
#         "Diet": functions.diet_emissions,
#         "Heating Source": functions.housing_emissions,
#         "Heating Usage": functions.h,
#         "Appliances Usage": functions.
#     }
#     # Create a Streamlit section for visualizations
#     st.header("Visualizations")

#     # Create a simple pie chart using Matplotlib
#     fig, ax = plt.subplots()
#     ax.pie(emissions.values(), labels=emissions.keys(), autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     ax.set_title("Carbon Emissions by Sector")

#     # Display the chart in Streamlit
#     st.pyplot(fig)

#     # Display the calculated emissions for each sector to the user
#     st.subheader("Carbon Emissions by Sector")
#     for sector, emission in emissions.items():
#         st.write(f"{sector}: {emission:.2f} kg CO2e")


    # # Assuming you have received emissions data from GPT-4 as a string
    # gpt4_response = """
    # Emissions data received from GPT-4:
    # Transportation: 5.2 kg CO2e
    # Electricity: 2.8 kg CO2e
    # Meat Consumption: 3.5 kg CO2e
    # Other: 1.9 kg CO2e
    # """

    # # Extract emissions data from the GPT-4 response
    # emissions_data = {}
    # lines = gpt4_response.split('\n')
    # for line in lines:
    #     if ':' in line:
    #         category, value = line.split(':')
    #         # Extract numerical values and convert them to floats
    #         category = category.strip()
    #         value = value.strip().split(' ')[0]  # Extract the numeric part and remove units
    #         try:
    #             emissions_data[category] = float(value)
    #         except ValueError:
    #             # Handle any conversion errors gracefully
    #             st.warning(f"Failed to convert value for {category} to float.")
    #             emissions_data[category] = 0.0  # Set a default value

    # # Create a Streamlit sidebar to display user inputs and recommendations
    # st.sidebar.header("User Inputs and Recommendations")
    # # Include your user inputs and recommendations here using st.sidebar components

    # # Create a Streamlit section for visualizations
    # st.header("Visualizations")

    # # Create a simple pie chart using Matplotlib
    # fig, ax = plt.subplots()
    # ax.pie(emissions_data.values(), labels=emissions_data.keys(), autopct='%1.1f%%', startangle=90)
    # ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax.set_title("Carbon Emissions by Category")

    # # Display the chart in Streamlit
    # st.pyplot(fig)

    # # Display the GPT-4 response containing emissions data
    # st.subheader("Emissions Data from GPT-4")
    # st.write(gpt4_response)

    # # Assuming you have LLM-generated recommendations, you can include them here.
    # st.subheader("LLM Recommendations")