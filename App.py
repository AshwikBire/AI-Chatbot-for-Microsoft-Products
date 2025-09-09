# jarvis_advanced.py
import streamlit as st
import requests
import json
import datetime
import wikipedia
import webbrowser
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from bs4 import BeautifulSoup
from PIL import Image
import io
import base64
import time
from typing import Dict, List, Any, Optional
import random
import re
import urllib.parse
import yt_dlp
import subprocess
import os
from pathlib import Path
import speech_recognition as sr
import pyttsx3
import threading
from streamlit_autorefresh import st_autorefresh
import pytz
from timezonefinder import TimezoneFinder
import geocoder
import calendar
from datetime import timedelta

# Set page configuration
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced dark UI with black and red theme
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a1a 100%);
    }
    .main-header {
        font-size: 3.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(255,0,0,0.7);
        background: linear-gradient(90deg, #000000, #1a0000);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FF0000;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF4444;
        margin-bottom: 1rem;
        padding: 12px;
        border-left: 5px solid #FF0000;
        background: linear-gradient(90deg, rgba(255,0,0,0.1), transparent);
    }
    .chat-container {
        background-color: #1a1a1a;
        border-radius: 20px;
        padding: 25px;
        height: 550px;
        overflow-y: auto;
        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.4);
        border: 2px solid #FF0000;
    }
    .user-message {
        background: linear-gradient(90deg, #2B2B2B, #3a0000);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 15px 20px;
        margin: 15px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        border-right: 5px solid #FF0000;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);
        animation: slideInRight 0.3s ease;
    }
    .assistant-message {
        background: linear-gradient(90deg, #2B2B2B, #002a00);
        color: #FFFFFF;
        border-radius: 18px;
        padding: 15px 20px;
        margin: 15px 0;
        max-width: 80%;
        margin-right: auto;
        border-left: 5px solid #00FF00;
        box-shadow: 0 4px 12px rgba(0, 255, 0, 0.3);
        animation: slideInLeft 0.3s ease;
    }
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .command-button {
        background: linear-gradient(90deg, #FF0000, #cc0000);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 8px;
        cursor: pointer;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
    }
    .command-button:hover {
        background: linear-gradient(90deg, #cc0000, #990000);
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(255, 0, 0, 0.4);
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
        color: #FFFFFF;
    }
    .stSidebar {
        background-color: #1a1a1a;
        border-right: 3px solid #FF0000;
    }
    .linkedin-badge {
        background: linear-gradient(90deg, #0A66C2, #004182);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0, 102, 194, 0.4);
    }
    .feature-card {
        background: linear-gradient(135deg, #2B2B2B, #1a0000);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 15px rgba(255, 0, 0, 0.3);
        border: 2px solid #FF0000;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 25px rgba(255, 0, 0, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #2B2B2B, #1a0000);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 15px rgba(255, 0, 0, 0.3);
        border: 2px solid #FF0000;
        text-align: center;
    }
    .stTextInput>div>div>input {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    .stSelectbox>div>div>select {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF0000, #cc0000);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #cc0000, #990000);
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(255, 0, 0, 0.4);
    }
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF0000, #990000);
        border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #cc0000, #660000);
    }
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #FF0000, transparent);
        margin: 20px 0;
        border-radius: 3px;
    }
    .typing-indicator {
        display: flex;
        padding: 15px;
        justify-content: center;
    }
    .typing-dot {
        width: 10px;
        height: 10px;
        margin: 0 4px;
        background-color: #FF0000;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-15px); }
    }
    .status-bar {
        background: linear-gradient(90deg, #2B2B2B, #1a0000);
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #FF0000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .voice-button {
        background: linear-gradient(90deg, #FF0000, #cc0000);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
    }
    .voice-button:hover {
        background: linear-gradient(90deg, #cc0000, #990000);
        transform: scale(1.1);
        box-shadow: 0 6px 12px rgba(255, 0, 0, 0.4);
    }
    .voice-button.listening {
        animation: pulse 1.5s infinite;
    }
    .tab-content {
        padding: 20px;
        background: linear-gradient(135deg, #2B2B2B, #1a0000);
        border-radius: 15px;
        border: 2px solid #FF0000;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'weather': '89f979da701d3eb6f23b5550750a36d6',
        'news': '0b08be107dca45d3be30ca7e06544408'
    }
if 'youtube_playing' not in st.session_state:
    st.session_state.youtube_playing = False
if 'current_song' not in st.session_state:
    st.session_state.current_song = None
if 'is_typing' not in st.session_state:
    st.session_state.is_typing = False
if 'voice_recognition' not in st.session_state:
    st.session_state.voice_recognition = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Chat"
if 'system_status' not in st.session_state:
    st.session_state.system_status = {
        'cpu_usage': '25%',
        'memory_usage': '60%',
        'network_status': 'Connected',
        'last_update': datetime.datetime.now().strftime("%H:%M:%S")
    }

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, key="data_refresh")

class JarvisAssistant:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "4.0"
        self.weather_api_key = st.session_state.api_keys['weather']
        self.news_api_key = st.session_state.api_keys['news']
        self.greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! I'm here to help.",
            "Hello! Ready to assist with your tasks."
        ]
        self.ms_office_keywords = {
            'excel': ['excel', 'spreadsheet', 'formula', 'function', 'vlookup', 'pivot', 'chart'],
            'word': ['word', 'document', 'template', 'format', 'header', 'footer'],
            'powerpoint': ['powerpoint', 'presentation', 'slide', 'animation', 'transition'],
            'powerbi': ['powerbi', 'power bi', 'dashboard', 'visualization', 'data model']
        }
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female
        self.tts_engine.setProperty('rate', 180)  # Speed of speech
        
    def speak(self, text):
        """Convert text to speech"""
        def speak_thread():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        thread = threading.Thread(target=speak_thread)
        thread.start()
    
    def listen(self):
        """Listen to microphone input and convert to text"""
        try:
            with self.microphone as source:
                st.session_state.voice_recognition = True
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio)
            st.session_state.voice_recognition = False
            return text.lower()
        except sr.WaitTimeoutError:
            st.session_state.voice_recognition = False
            return "I didn't hear anything. Please try again."
        except sr.UnknownValueError:
            st.session_state.voice_recognition = False
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            st.session_state.voice_recognition = False
            return "Sorry, my speech service is down."
        except Exception as e:
            st.session_state.voice_recognition = False
            return f"Error: {str(e)}"
    
    def get_time(self, city=None):
        now = datetime.datetime.now()
        if city:
            try:
                # Get timezone for the city
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(city=city)
                if timezone_str:
                    tz = pytz.timezone(timezone_str)
                    city_time = datetime.datetime.now(tz)
                    return f"The current time in {city} is {city_time.strftime('%H:%M:%S')} on {city_time.strftime('%A, %B %d, %Y')}"
                else:
                    return f"Could not find timezone for {city}. The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%A, %B %d, %Y')}"
            except:
                return f"Could not get time for {city}. The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%A, %B %d, %Y')}"
        else:
            return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%A, %B %d, %Y')}"
    
    def get_weather(self, city: str = "Mumbai") -> str:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={self.weather_api_key}&q={city}&units=metric"
        
        try:
            response = requests.get(complete_url)
            data = response.json()
            
            if data["cod"] != "404":
                main = data["main"]
                weather = data["weather"][0]
                wind = data["wind"]
                
                temperature = main["temp"]
                feels_like = main["feels_like"]
                pressure = main["pressure"]
                humidity = main["humidity"]
                description = weather["description"].title()
                wind_speed = wind["speed"]
                
                # Get forecast
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.weather_api_key}&units=metric"
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()
                
                if forecast_data.get("list"):
                    tomorrow = forecast_data["list"][7]  # 24 hours from now
                    tomorrow_temp = tomorrow["main"]["temp"]
                    tomorrow_desc = tomorrow["weather"][0]["description"].title()
                    
                    return (f"Weather in {city}: {description}\n"
                            f"Temperature: {temperature}°C (Feels like {feels_like}°C)\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s\n"
                            f"Pressure: {pressure} hPa\n\n"
                            f"Tomorrow's forecast: {tomorrow_desc}, {tomorrow_temp}°C")
                else:
                    return (f"Weather in {city}: {description}\n"
                            f"Temperature: {temperature}°C (Feels like {feels_like}°C)\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s\n"
                            f"Pressure: {pressure} hPa")
            else:
                return "City not found. Please try again."
        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
    
    def get_news(self, category: str = "general", country: str = "in") -> List[Dict]:
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": country,
            "category": category,
            "apiKey": self.news_api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data["status"] == "ok":
                articles = data["articles"][:5]  # Get top 5 articles
                return articles
            else:
                return [{"title": "Error fetching news", "description": "Please try again later."}]
        except Exception as e:
            return [{"title": f"Error: {str(e)}", "description": "Failed to fetch news."}]
    
    def search_wikipedia(self, query: str) -> str:
        try:
            result = wikipedia.summary(query, sentences=3)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Please be more specific: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information on that topic."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_google(self, query: str) -> str:
        try:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find featured snippet or knowledge panel
            featured_snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
            if featured_snippet:
                return f"{featured_snippet.text}\n\nFor more information, I can open the search results in your browser."
            
            # Try to find regular search results
            search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd', limit=3)
            if search_results:
                result_text = "\n".join([result.text for result in search_results])
                return f"{result_text}\n\nFor more information, I can open the search results in your browser."
            
            return "I found some results but couldn't extract the information. Would you like me to open the search in your browser?"
        except Exception as e:
            return f"Error performing Google search: {str(e)}"
    
    def open_browser_search(self, query: str):
        search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        webbrowser.open(search_url)
        return f"Opening search results for '{query}' in your browser."
    
    def get_gold_price(self, city: str = "Mumbai") -> str:
        try:
            # This is a placeholder - in a real implementation, you would use a gold price API
            # For demonstration, we'll return mock data
            gold_prices = {
                "Mumbai": "₹5,800 per gram (24K)",
                "Delhi": "₹5,750 per gram (24K)",
                "Chennai": "₹5,820 per gram (24K)",
                "Kolkata": "₹5,770 per gram (24K)",
                "Bangalore": "₹5,790 per gram (24K)"
            }
            
            if city in gold_prices:
                return f"Gold price in {city}: {gold_prices[city]}"
            else:
                return f"Gold price information not available for {city}. Available cities: {', '.join(gold_prices.keys())}"
        except Exception as e:
            return f"Error fetching gold price: {str(e)}"
    
    def get_crypto_price(self, coin: str = "bitcoin") -> str:
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=inr"
            response = requests.get(url)
            data = response.json()
            
            if coin in data:
                price = data[coin]['inr']
                return f"Current {coin.capitalize()} price: ₹{price:,.2f}"
            else:
                return f"Could not find price for {coin}. Try 'bitcoin', 'ethereum', etc."
        except Exception as e:
            return f"Error fetching cryptocurrency price: {str(e)}"
    
    def search_ms_office_help(self, product: str, query: str) -> str:
        """Search for Microsoft Office help and formulas"""
        try:
            # Map products to their official documentation sites
            product_sites = {
                "excel": "https://support.microsoft.com/en-us/excel",
                "word": "https://support.microsoft.com/en-us/word",
                "powerpoint": "https://support.microsoft.com/en-us/powerpoint",
                "powerbi": "https://docs.microsoft.com/en-us/power-bi"
            }
            
            if product not in product_sites:
                return f"I don't have specific help for {product}. Try asking about Excel, Word, PowerPoint, or Power BI."
            
            # Create a search URL for the specific product
            search_query = f"{product} {query} site:support.microsoft.com"
            search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(search_query)}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find featured snippet or knowledge panel
            featured_snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
            if featured_snippet:
                return f"Here's what I found about {query} in {product}:\n\n{featured_snippet.text}\n\nFor more detailed information, I can open the official Microsoft support page in your browser."
            
            # Try to find regular search results
            search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd', limit=3)
            if search_results:
                result_text = "\n".join([result.text for result in search_results])
                return f"Here's what I found about {query} in {product}:\n\n{result_text}\n\nFor more detailed information, I can open the official Microsoft support page in your browser."
            
            return f"I couldn't find specific information about '{query}' in {product}. Would you like me to open the official Microsoft support page for {product}?"
        
        except Exception as e:
            return f"Error searching for {product} help: {str(e)}"
    
    def open_youtube_video(self, query: str):
        """Open a YouTube video based on the query"""
        try:
            search_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(youtube_url)
            return f"Opening YouTube search results for '{query}' in your browser."
        except Exception as e:
            return f"Error opening YouTube: {str(e)}"
    
    def play_youtube_video(self, query: str):
        """Play a YouTube video (simulated)"""
        try:
            # In a real implementation, you might use yt_dlp to get video info
            # For Streamlit, we can't directly play videos but can provide links
            search_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            # Simulate playing by storing the current song
            st.session_state.youtube_playing = True
            st.session_state.current_song = query
            
            return f"Now playing '{query}' on YouTube. I've opened the search results in your browser."
        except Exception as e:
            return f"Error playing YouTube video: {str(e)}"
    
    def stop_youtube_video(self):
        """Stop the currently playing YouTube video"""
        if st.session_state.youtube_playing:
            st.session_state.youtube_playing = False
            song = st.session_state.current_song
            st.session_state.current_song = None
            return f"Stopped playing '{song}'."
        else:
            return "No video is currently playing."
    
    def get_joke(self):
        """Get a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "How does a penguin build its house? Igloos it together!",
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ]
        return random.choice(jokes)
    
    def get_quote(self):
        """Get an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "Spread love everywhere you go. - Mother Teresa",
            "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
            "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Whoever is happy will make others happy too. - Anne Frank"
        ]
        return random.choice(quotes)
    
    def set_reminder(self, reminder_text, reminder_time):
        """Set a reminder (simulated)"""
        return f"Reminder set for {reminder_time}: {reminder_text}"
    
    def process_command(self, command: str):
        command = command.lower()
        action = None
        
        # Time queries
        if any(word in command for word in ["time", "clock", "current time"]):
            cities = ["mumbai", "delhi", "chennai", "kolkata", "bangalore", "london", "new york", "tokyo"]
            for city in cities:
                if city in command:
                    return self.get_time(city.title()), action
            return self.get_time(), action
        
        # Weather queries
        elif any(word in command for word in ["weather", "temperature", "forecast"]):
            cities = ["mumbai", "delhi", "chennai", "kolkata", "bangalore", "london", "new york", "tokyo"]
            for city in cities:
                if city in command:
                    return self.get_weather(city.title()), action
            return self.get_weather(), action  # Default to Mumbai
        
        # News queries
        elif any(word in command for word in ["news", "headlines", "update"]):
            articles = self.get_news()
            news_response = "Here are the top news headlines:\n\n"
            for i, article in enumerate(articles, 1):
                news_response += f"{i}. {article['title']}\n"
            return news_response, action
        
        # Wikipedia queries
        elif any(word in command for word in ["wikipedia", "wiki", "what is", "who is"]):
            query = command.replace("search", "").replace("wikipedia", "").replace("wiki", "").strip()
            if query:
                return self.search_wikipedia(query), action
            return "What would you like me to search on Wikipedia?", action
        
        # Google search queries
        elif any(word in command for word in ["search", "google", "find"]):
            query = command.replace("search", "").replace("google", "").replace("for", "").strip()
            if query:
                if "open" in command or "browser" in command:
                    action = f"open_browser:{query}"
                    return f"Opening search results for '{query}' in your browser.", action
                return self.search_google(query), action
            return "What would you like me to search for?", action
        
        # Gold price queries
        elif any(word in command for word in ["gold", "gold price", "gold rate"]):
            cities = ["mumbai", "delhi", "chennai", "kolkata", "bangalore"]
            for city in cities:
                if city in command:
                    return self.get_gold_price(city.title()), action
            return self.get_gold_price(), action  # Default to Mumbai
        
        # Crypto price queries
        elif any(word in command for word in ["crypto", "bitcoin", "ethereum", "dogecoin"]):
            coins = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]
            for coin in coins:
                if coin in command:
                    return self.get_crypto_price(coin), action
            return self.get_crypto_price(), action  # Default to bitcoin
        
        # Microsoft Office queries
        elif any(word in command for word in ["excel", "word", "powerpoint", "powerpoint", "power bi", "office"]):
            # Determine which product is being asked about
            product = None
            for p, keywords in self.ms_office_keywords.items():
                if any(keyword in command for keyword in keywords):
                    product = p
                    break
            
            if product:
                # Extract the query
                query = command
                for keyword in self.ms_office_keywords[product]:
                    query = query.replace(keyword, "")
                query = query.strip()
                
                if query:
                    return self.search_ms_office_help(product, query), action
                else:
                    return f"What would you like to know about {product}?", action
            else:
                return "Which Microsoft Office product are you asking about? (Excel, Word, PowerPoint, Power BI)", action
        
        # YouTube queries
        elif any(word in command for word in ["youtube", "video", "play", "song", "music"]):
            if "play" in command:
                query = command.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
                if query:
                    action = f"play_youtube:{query}"
                    return self.play_youtube_video(query), action
                else:
                    return "What would you like me to play on YouTube?", action
            elif "open youtube" in command:
                action = "open_youtube:"
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube in your browser.", action
            else:
                query = command.replace("search", "").replace("on youtube", "").replace("youtube", "").strip()
                if query:
                    action = f"open_youtube_search:{query}"
                    return self.open_youtube_video(query), action
                else:
                    return "What would you like me to search on YouTube?", action
        
        # Stop playing
        elif any(word in command for word in ["stop", "pause", "end"]):
            if st.session_state.youtube_playing:
                return self.stop_youtube_video(), action
            else:
                return "Nothing is currently playing.", action
        
        # Open browser
        elif any(word in command for word in ["open", "browser", "website"]):
            if "http" in command:
                url = re.search(r'(https?://\S+)', command)
                if url:
                    action = f"open_url:{url.group(1)}"
                    webbrowser.open(url.group(1))
                    return f"Opening {url.group(1)} in your browser.", action
            else:
                site = command.replace("open", "").replace("in browser", "").replace("browser", "").strip()
                if site:
                    if not site.startswith("http"):
                        site = "https://" + site
                    action = f"open_url:{site}"
                    webbrowser.open(site)
                    return f"Opening {site} in your browser.", action
                else:
                    return "Which website would you like me to open?", action
        
        # Joke command
        elif any(word in command for word in ["joke", "funny", "make me laugh"]):
            return self.get_joke(), action
        
        # Quote command
        elif any(word in command for word in ["quote", "inspiration", "motivation"]):
            return self.get_quote(), action
        
        # Reminder command
        elif any(word in command for word in ["remind", "reminder"]):
            # Simple reminder implementation
            return "I'll remind you about that. (Note: This is a simulated reminder. In a full implementation, this would be stored and triggered at the specified time.)", action
        
        # Greetings
        elif any(word in command for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greetings), action
        
        # Help
        elif any(word in command for word in ["help", "what can you do"]):
            return ("I can help you with:\n"
                   "- Telling time and date\n"
                   "- Weather information for major cities\n"
                   "- Latest news headlines\n"
                   "- Wikipedia searches\n"
                   "- Google searches\n"
                   "- Gold prices in major Indian cities\n"
                   "- Cryptocurrency prices\n"
                   "- Microsoft Office help (Excel, Word, PowerPoint, Power BI)\n"
                   "- YouTube video searches and playback\n"
                   "- Opening websites in your browser\n"
                   "- Telling jokes and inspirational quotes\n"
                   "- Setting reminders\n"
                   "- Voice commands\n"
                   "- And much more! Just ask me anything."), action
        
        # Default response
        else:
            return ("I'm not sure how to help with that. "
                   "Try asking about time, weather, news, Microsoft Office, or search for something. "
                   "You can also type 'help' to see what I can do."), action

# UI Components
def render_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='color: #FF0000; text-align: center;'>JARVIS AI</h1>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # User profile
        st.markdown("<h3 style='color: #FF4444;'>Your Profile</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
        with col2:
            st.write("**Ashwik Bire**")
            st.write("AI Enthusiast")
        
        # LinkedIn profile
        st.markdown(f"""
        <div class="linkedin-badge">
            <a href="https://www.linkedin.com/in/ashwik-bire-b2a000186" target="_blank" style="color: white; text-decoration: none;">
                <i class="fab fa-linkedin"></i> Connect on LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("<h3 style='color: #FF4444;'>Navigation</h3>", unsafe_allow_html=True)
        tabs = st.radio("", ["Chat", "Dashboard", "Settings", "Help"], key="nav_tabs")
        st.session_state.current_tab = tabs
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # System Status
        st.markdown("<h3 style='color: #FF4444;'>System Status</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="status-bar">
            <span>CPU Usage:</span>
            <span>{st.session_state.system_status['cpu_usage']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="status-bar">
            <span>Memory Usage:</span>
            <span>{st.session_state.system_status['memory_usage']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="status-bar">
            <span>Network:</span>
            <span>{st.session_state.system_status['network_status']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="status-bar">
            <span>Last Update:</span>
            <span>{st.session_state.system_status['last_update']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Voice Control
        st.markdown("<h3 style='color: #FF4444;'>Voice Control</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Start Listening", use_container_width=True):
                st.session_state.voice_recognition = True
                # Simulate voice recognition
                st.session_state.chat_history.append({"role": "user", "content": "[Voice command]"})
                response, action = assistant.process_command("what time is it")
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        with col2:
            if st.button("🔇 Stop Listening", use_container_width=True):
                st.session_state.voice_recognition = False
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("<h3 style='color: #FF4444;'>Quick Actions</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🕐 Time", use_container_width=True):
                response = assistant.get_time()
                st.session_state.chat_history.append({"role": "user", "content": "What time is it?"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            if st.button("🌤️ Weather", use_container_width=True):
                response = assistant.get_weather()
                st.session_state.chat_history.append({"role": "user", "content": "What's the weather like?"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with col2:
            if st.button("📰 News", use_container_width=True):
                articles = assistant.get_news()
                response = "Here are the top news headlines:\n\n"
                for i, article in enumerate(articles, 1):
                    response += f"{i}. {article['title']}\n"
                
                st.session_state.chat_history.append({"role": "user", "content": "Show me the news"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            if st.button("💰 Gold", use_container_width=True):
                response = assistant.get_gold_price()
                st.session_state.chat_history.append({"role": "user", "content": "What's the gold price in Mumbai?"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Settings
        st.markdown("<h3 style='color: #FF4444;'>Settings</h3>", unsafe_allow_html=True)
        st.session_state.api_keys['weather'] = st.text_input("Weather API Key", value=st.session_state.api_keys['weather'], type="password")
        st.session_state.api_keys['news'] = st.text_input("News API Key", value=st.session_state.api_keys['news'], type="password")
        
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### About JARVIS")
        st.info("JARVIS is an AI assistant designed to help with various tasks including weather, news, searches, Microsoft Office help, and more.")

def render_chat_interface():
    st.markdown('<div class="main-header">JARVIS AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Voice recognition status
    if st.session_state.voice_recognition:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="voice-button listening">🎤</div>
            <p style="color: #FF0000; font-weight: bold;">Listening...</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                # Convert line breaks to HTML for better formatting
                formatted_content = message["content"].replace('\n', '<br>')
                st.markdown(f'<div class="assistant-message"><strong>JARVIS:</strong> {formatted_content}</div>', unsafe_allow_html=True)
        
        # Show typing indicator if needed
        if st.session_state.is_typing:
            st.markdown('<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        user_input = st.text_input("Your message:", placeholder="Type your message here...", key="user_input", label_visibility="collapsed")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("Send", use_container_width=True)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎤", use_container_width=True):
            # Simulate voice input
            st.session_state.chat_history.append({"role": "user", "content": "[Voice command: What time is it?]"})
            response, action = assistant.process_command("what time is it")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Process input
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show typing indicator
        st.session_state.is_typing = True
        st.rerun()
        
        # Get assistant response
        response, action = assistant.process_command(user_input)
        
        # Hide typing indicator
        st.session_state.is_typing = False
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Handle actions (like opening browser)
        if action:
            action_type, action_value = action.split(":", 1) if ":" in action else (action, "")
            
            if action_type == "open_browser":
                assistant.open_browser_search(action_value)
            elif action_type == "open_youtube_search":
                assistant.open_youtube_video(action_value)
            elif action_type == "open_url":
                webbrowser.open(action_value)
        
        # Speak the response
        assistant.speak(response)
        
        # Rerun to update the chat display
        st.rerun()

def render_dashboard():
    st.markdown('<div class="main-header">JARVIS Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Current Time", datetime.datetime.now().strftime("%H:%M:%S"))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Get weather data
        weather_text = assistant.get_weather("Mumbai")
        temperature = weather_text.split("Temperature: ")[1].split("°C")[0] if "Temperature:" in weather_text else "N/A"
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mumbai Temperature", f"{temperature}°C")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        # Get gold price
        gold_text = assistant.get_gold_price("Mumbai")
        gold_price = gold_text.split(": ")[1] if ": " in gold_text else "N/A"
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Gold Price (Mumbai)", gold_price)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        # Get crypto price
        crypto_text = assistant.get_crypto_price("bitcoin")
        crypto_price = crypto_text.split(": ")[1] if ": " in crypto_text else "N/A"
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Bitcoin Price", crypto_price)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("<h2 style='color: #FF4444;'>Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌤️ Weather Info", use_container_width=True):
            response = assistant.get_weather()
            st.session_state.chat_history.append({"role": "user", "content": "What's the weather like?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    with col2:
        if st.button("📰 Latest News", use_container_width=True):
            articles = assistant.get_news()
            response = "Here are the top news headlines:\n\n"
            for i, article in enumerate(articles, 1):
                response += f"{i}. {article['title']}\n"
            
            st.session_state.chat_history.append({"role": "user", "content": "Show me the news"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    with col3:
        if st.button("💰 Gold Prices", use_container_width=True):
            response = assistant.get_gold_price()
            st.session_state.chat_history.append({"role": "user", "content": "What's the gold price in Mumbai?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("🔍 Web Search", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "I want to search for something"})
            st.session_state.chat_history.append({"role": "assistant", "content": "What would you like me to search for?"})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    with col5:
        if st.button("📊 Office Help", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "I need help with Microsoft Office"})
            st.session_state.chat_history.append({"role": "assistant", "content": "Which Microsoft Office product do you need help with? (Excel, Word, PowerPoint, Power BI)"})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    with col6:
        if st.button("🎵 YouTube", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "I want to watch something on YouTube"})
            st.session_state.chat_history.append({"role": "assistant", "content": "What would you like to watch on YouTube?"})
            st.session_state.current_tab = "Chat"
            st.rerun()
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # News section
    st.markdown("<h2 style='color: #FF4444;'>Latest News</h2>", unsafe_allow_html=True)
    articles = assistant.get_news()
    
    for i, article in enumerate(articles[:3]):
        with st.expander(f"{i+1}. {article['title']}"):
            st.write(article['description'] or "No description available")
            if article['url']:
                st.markdown(f"[Read more]({article['url']})")
    
    # Weather chart
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4444;'>Weather Forecast</h2>", unsafe_allow_html=True)
    
    # Sample data for chart
    days = ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5']
    temperatures = [32, 34, 33, 31, 30]
    humidity = [65, 70, 68, 72, 75]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temperatures, mode='lines+markers', name='Temperature (°C)', line=dict(color='#FF0000')))
    fig.add_trace(go.Scatter(x=days, y=humidity, mode='lines+markers', name='Humidity (%)', line=dict(color='#00FF00')))
    
    fig.update_layout(
        title='Mumbai Weather Forecast',
        yaxis_title='Values',
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font_color='#FFFFFF',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_settings():
    st.markdown('<div class="main-header">JARVIS Settings</div>', unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #FF4444;'>API Configuration</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.api_keys['weather'] = st.text_input("Weather API Key", value=st.session_state.api_keys['weather'], type="password")
    
    with col2:
        st.session_state.api_keys['news'] = st.text_input("News API Key", value=st.session_state.api_keys['news'], type="password")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4444;'>Appearance</h2>", unsafe_allow_html=True)
    
    theme = st.selectbox("Theme", ["Dark", "Light"], index=0)
    accent_color = st.color_picker("Accent Color", "#FF0000")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4444;'>Voice Settings</h2>", unsafe_allow_html=True)
    
    voice_options = ["Male", "Female"]
    voice = st.selectbox("Voice", voice_options, index=1)
    voice_speed = st.slider("Voice Speed", 50, 300, 180)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    if st.button("Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")
    
    if st.button("Reset to Defaults", use_container_width=True):
        st.session_state.api_keys = {
            'weather': '89f979da701d3eb6f23b5550750a36d6',
            'news': '0b08be107dca45d3be30ca7e06544408'
        }
        st.success("Settings reset to defaults!")

def render_help():
    st.markdown('<div class="main-header">JARVIS Help</div>', unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #FF4444;'>Getting Started</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="tab-content">
        <p>JARVIS is an AI assistant designed to help with various tasks. Here are some examples of what you can ask:</p>
        <ul>
            <li><strong>Time:</strong> "What time is it?" or "Time in London"</li>
            <li><strong>Weather:</strong> "What's the weather like?" or "Weather in Delhi"</li>
            <li><strong>News:</strong> "Show me the news" or "Latest headlines"</li>
            <li><strong>Search:</strong> "Search for artificial intelligence"</li>
            <li><strong>Wikipedia:</strong> "Wikipedia Albert Einstein"</li>
            <li><strong>Office Help:</strong> "Excel VLOOKUP formula" or "PowerPoint animation tips"</li>
            <li><strong>YouTube:</strong> "Play songs on YouTube" or "Search for tutorials"</li>
            <li><strong>Gold Prices:</strong> "Gold price in Mumbai"</li>
            <li><strong>Crypto:</strong> "Bitcoin price" or "Ethereum price"</li>
            <li><strong>Fun:</strong> "Tell me a joke" or "Inspirational quote"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4444;'>Voice Commands</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="tab-content">
        <p>You can use voice commands by clicking the microphone button. JARVIS will listen for your command and respond accordingly.</p>
        <p>Make sure your microphone is enabled and you're in a quiet environment for best results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4444;'>Troubleshooting</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="tab-content">
        <p><strong>Q: JARVIS isn't responding to my commands.</strong></p>
        <p>A: Make sure you're using supported commands. Type "help" to see a list of supported commands.</p>
        
        <p><strong>Q: The weather/news isn't loading.</strong></p>
        <p>A: Check your API keys in the Settings tab and make sure they're valid.</p>
        
        <p><strong>Q: Voice commands aren't working.</strong></p>
        <p>A: Make sure your microphone is enabled and you've given permission to the browser to use it.</p>
    </div>
    """, unsafe_allow_html=True)

# Main application
def main():
    # Initialize assistant
    global assistant
    assistant = JarvisAssistant()
    
    # Render sidebar
    render_sidebar()
    
    # Render main content based on selection
    if st.session_state.current_tab == "Chat":
        render_chat_interface()
    elif st.session_state.current_tab == "Dashboard":
        render_dashboard()
    elif st.session_state.current_tab == "Settings":
        render_settings()
    elif st.session_state.current_tab == "Help":
        render_help()

if __name__ == "__main__":
    main()
