import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Initialize NLTK's Sentiment Intensity Analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Create a function to initialize and retrieve session state
def get_session_state():
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = []

    return st.session_state.feedback_data


def feedback():
    st.title("Feedback Form")

    # Rating Questions
    st.header("1. Awareness")

    awareness = st.radio("How aware are you with the concept of 'Carbon Footprint'?", ['Very aware', "Somewhat aware", "Not very aware", "Not aware at all"])
    concern = st.radio("How concerned are you about your personal carbon footprint and its impact on the environment?", ["Very concerned", "Somewhat concerned", "Not very concerned", "Not concerned at all"])

    # Survey Questions
    st.header("2. Actions Taken")
    actions = st.multiselect("Have you taken any specific actions in your daily life to reduce your carbon footprint? (Select all that apply)",
                         ["Using energy-efficient appliances", "Reducing energy consumption (e.g., turning off lights, adjusting thermostat)",
                          "Reducing car travel or using public transportation", "Carpooling or ridesharing", "Using a bike or walking for short trips",
                          "Reducing, reusing, and recycling", "Eating a more plant-based diet", "Other (please specify)"])

    other_action = st.text_input("Other actions:", "")

    st.header("3. Willingness to Reduce")

    willingness = st.slider("On a scale of 1 to 5 (1 being not willing at all and 5 being very willing), how willing are you to take steps to reduce your carbon footprint?", 1, 5)

    motivation = st.multiselect("What motivates you the most to reduce your carbon footprint? (Select all that apply)",
                            ["Environmental concern", "Cost savings", "Government incentives or regulations", "Peer influence", "Personal health", "Other (please specify)"])
    other_motivation = st.text_input("Other motivations:", "")

    st.header("4. Barriers to Reducing Carbon Footprint")

    barriers = st.text_area("What challenges or barriers do you face when trying to reduce your carbon footprint?", "")

    # Section 5: Suggestions for Improvement
    st.header("5. Suggestions for Improvement")

    improvements = st.text_area("How can our system or organization help you better understand and reduce your carbon footprint?", "")

    # Section 6: Additional Comments
    st.header("6. Feedback")

    additional_feedback = st.text_area("Is there anything else you would like to share regarding your views on carbon footprint and reducing it?", "")


    # Sentiment Analysis

    if st.button("Submit"):
        feedback = {
            "Awareness": awareness,
            "Concern": concern,
            "Actions Taken": actions,
            "Willingness to Improve": willingness,
            "Reason for motivation": motivation,
            "Other Reasons": other_motivation,
            "Barriers" : barriers,
            "Suggestion" : improvements,
            "Feedback" : additional_feedback}
        

        def analyze_sentiment(text):
            sentiment_scores = sia.polarity_scores(text)
            compound_score = sentiment_scores["compound"]
            if compound_score >= 0.05:
                return "Positive"
            elif compound_score <= -0.05:
                return "Negative"
            else:
                return "Neutral"
            
        sentiment_result = ""
        if additional_feedback:
            sentiment_result = analyze_sentiment(additional_feedback)
            st.write(f"Sentiment: {sentiment_result}")
        else:
            st.warning("Please enter additional comments for sentiment analysis.")


        feedback_data = get_session_state()
        feedback_data.append(feedback)
        st.success("Thank you for your feedback!")

         # Append feedback data to the existing CSV file
        feedback_df = pd.DataFrame(feedback_data)
        feedback_df.to_csv("feedback_data.csv", mode='a', header=not st.session_state.get('csv_exists', False), index=False)

        # Set a flag to indicate that the CSV file exists (to avoid recreating the header)
        st.session_state.csv_exists = True