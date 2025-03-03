import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
import random

# ✅ Access Hugging Face Secret API Key
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

def get_travel_options(source, destination, travel_date):
    system_prompt = SystemMessage(
        content="""
        You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with 
        estimated costs, duration, and relevant travel tips. Also, consider travel date for availability and 
        price fluctuations. Suggest top tourist attractions and travel tips too.
        """
    )
    user_prompt = HumanMessage(
        content=f"""
        I am traveling from {source} to {destination} on {travel_date}. 
        Suggest travel options with estimated cost, duration, and important details.
        """
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
    
    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

def get_destination_facts(destination):
    system_prompt = SystemMessage(
        content="""
        You are an AI expert in geography and travel. Provide detailed information on what makes a location famous.
        Include historical significance, cultural highlights, food specialties, landmarks, and unique aspects.
        The response should be structured with headings like 'Features', 'History', and 'Examples'.
        """
    )
    user_prompt = HumanMessage(
        content=f"What is famous in {destination}?"
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
    
    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No information available."
    except Exception as e:
        return f"❌ Error fetching destination details: {str(e)}"

# 🌎 Streamlit UI Configuration
st.set_page_config(page_title="AI Travel Guru 🌟", page_icon="✈️", layout="wide")

# 🎭 Fun Header
st.markdown("""
    <div style='text-align: center;'>
        <h1>🌍 AI Travel Guru 🚀</h1>
        <h4>"Plan Smarter, Travel Better!" ✈️🌟</h4>
    </div>
    <hr>
""", unsafe_allow_html=True)

# 🚀 User Input Section
source = st.text_input("📍 Enter Departure City", placeholder="E.g., Hyderabad")
destination = st.text_input("🎯 Enter Destination", placeholder="E.g., Durgi")
travel_date = st.date_input("📅 Pick Your Travel Date", min_value=datetime.today())

if st.button("🌟 Find My Best Routes! 🛫"):
    if source.strip() and destination.strip():
        with st.spinner(random.choice(["⏳ Checking flight schedules...", "🚆 Finding the fastest train routes...", "🚗 Calculating cab fares...", "🛩️ Fetching flight prices..."])):
            travel_info = get_travel_options(source, destination, travel_date)
            st.success("🌟 Your AI-Powered Travel Guide:")
            st.markdown(travel_info)
        
        with st.spinner("📍 Fetching what makes this place famous..."):
            destination_info = get_destination_facts(destination)
            st.subheader(f"🌟 What is Famous in {destination}?")
            st.markdown(destination_info)
    else:
        st.warning("⚠️ Please enter both source and destination locations to proceed!")

# 🎉 Fun Footer
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <p>🚀 Built with ❤️ using Streamlit & Powered by Google Gemini 🌍✨</p>
        <p>💡 Travel more, worry less! 🌟</p>
    </div>
""", unsafe_allow_html=True)
