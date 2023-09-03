import streamlit as st
import functions
import recommendation
import feedback


def main():
    st.title("Carbon Footprint Calculator")

    st.sidebar.title("Navigation")
    navigation_expanded = st.sidebar.checkbox("Show Navigation")

    if navigation_expanded:
        current_step = st.sidebar.radio("Go to:", ["Welcome", "Transportation", "Electricity", "Diet", "Clothing","Housing", "Results","Visualization","Recommendation","Feedback"])

        if current_step == "Welcome":
            functions.introduction()
        elif current_step == "Transportation":
            functions.transportation()
        elif current_step == "Electricity":
            functions.electricity()
        elif current_step == "Diet":
            functions.diet()
        elif current_step == "Clothing":
            functions.clothing()
        elif current_step == "Housing":
            functions.housing()
        elif current_step == "Results":
            functions.calculate_total_emissions()
            functions.show_results()
        elif current_step == "Visualization":
            functions.visualization()
        elif current_step=="Recommendation":
            recommendation_response=recommendation.recommendation()
            st.write(recommendation_response)
        elif current_step=="Feedback":
            feedback.feedback()

if __name__ == "__main__":
    main()