# App.py (Streamlit-compatible version)
import streamlit as st
import requests
import json
import datetime
import wikipedia
import webbrowser
import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Any
import random
import re
import urllib.parse

# Set page configuration
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark UI with black and red theme
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .main-header {
        font-size: 3rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(255,0,0,0.5);
    }
    .chat-container {
        background-color: #1a1a1a;
        border-radius: 15px;
        padding: 20px;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
        border: 2px solid #FF0000;
    }
    .user-message {
        background: linear-gradient(90deg, #2B2B2B, #3a0000);
        color: #FFFFFF;
        border-radius: 15px;
        padding: 12px 18px;
        margin: 12px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        border-right: 4px solid #FF0000;
    }
    .assistant-message {
        background: linear-gradient(90deg, #2B2B2B, #002a00);
        color: #FFFFFF;
        border-radius: 15px;
        padding: 12px 18px;
        margin: 12px 0;
        max-width: 80%;
        margin-right: auto;
        border-left: 4px solid #00FF00;
    }
    .command-button {
        background: linear-gradient(90deg, #FF0000, #cc0000);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px;
        cursor: pointer;
        width: 100%;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
        color: #FFFFFF;
    }
    .stSidebar {
        background-color: #1a1a1a;
        border-right: 2px solid #FF0000;
    }
    .linkedin-badge {
        background: linear-gradient(90deg, #0A66C2, #004182);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin-top: 20px;
    }
    .feature-card {
        background: linear-gradient(135deg, #2B2B2B, #1a0000);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
        border: 1px solid #FF0000;
    }
    .stTextInput>div>div>input {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #FF0000;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF0000, #cc0000);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF0000, #990000);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'weather': '89f979da701d3eb6f23b5550750a36d6',
        'news': '0b08be107dca45d3be30ca7e06544408'
    }

class JarvisAssistant:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "3.0"
        self.weather_api_key = st.session_state.api_keys['weather']
        self.news_api_key = st.session_state.api_keys['news']
        self.greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! I'm here to help.",
            "Hello! Ready to assist with your tasks."
        ]
        
    def get_time(self):
        now = datetime.datetime.now()
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
                pressure = main["pressure"]
                humidity = main["humidity"]
                description = weather["description"].title()
                wind_speed = wind["speed"]
                
                return (f"Weather in {city}: {description}\n"
                        f"Temperature: {temperature}°C\n"
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
                articles = data["articles"][:5]
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
            
            featured_snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
            if featured_snippet:
                return f"{featured_snippet.text}\n\nFor more information, I can open the search results in your browser."
            
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
    
    def search_ms_office_help(self, product: str, query: str) -> str:
        try:
            product_sites = {
                "excel": "https://support.microsoft.com/en-us/excel",
                "word": "https://support.microsoft.com/en-us/word",
                "powerpoint": "https://support.microsoft.com/en-us/powerpoint",
                "powerbi": "https://docs.microsoft.com/en-us/power-bi"
            }
            
            if product not in product_sites:
                return f"I don't have specific help for {product}. Try asking about Excel, Word, PowerPoint, or Power BI."
            
            search_query = f"{product} {query} site:support.microsoft.com"
            search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(search_query)}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            featured_snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
            if featured_snippet:
                return f"Here's what I found about {query} in {product}:\n\n{featured_snippet.text}\n\nFor more detailed information, I can open the official Microsoft support page in your browser."
            
            search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd', limit=3)
            if search_results:
                result_text = "\n".join([result.text for result in search_results])
                return f"Here's what I found about {query} in {product}:\n\n{result_text}\n\nFor more detailed information, I can open the official Microsoft support page in your browser."
            
            return f"I couldn't find specific information about '{query}' in {product}. Would you like me to open the official Microsoft support page for {product}?"
        
        except Exception as e:
            return f"Error searching for {product} help: {str(e)}"
    
    def open_youtube_video(self, query: str):
        try:
            search_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(youtube_url)
            return f"Opening YouTube search results for '{query}' in your browser."
        except Exception as e:
            return f"Error opening YouTube: {str(e)}"
    
    def process_command(self, command: str):
        command = command.lower()
        action = None
        
        # Time queries
        if any(word in command for word in ["time", "clock", "current time"]):
            return self.get_time(), action
        
        # Weather queries
        elif any(word in command for word in ["weather", "temperature", "forecast"]):
            cities = ["mumbai", "delhi", "chennai", "kolkata", "bangalore"]
            for city in cities:
                if city in command:
                    return self.get_weather(city.title()), action
            return self.get_weather(), action
        
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
            return self.get_gold_price(), action
        
        # Microsoft Office queries
        elif any(word in command for word in ["excel", "word", "powerpoint", "powerpoint", "power bi", "office"]):
            product = None
            ms_office_keywords = {
                'excel': ['excel', 'spreadsheet', 'formula', 'function', 'vlookup', 'pivot', 'chart'],
                'word': ['word', 'document', 'template', 'format', 'header', 'footer'],
                'powerpoint': ['powerpoint', 'presentation', 'slide', 'animation', 'transition'],
                'powerbi': ['powerbi', 'power bi', 'dashboard', 'visualization', 'data model']
            }
            
            for p, keywords in ms_office_keywords.items():
                if any(keyword in command for keyword in keywords):
                    product = p
                    break
            
            if product:
                query = command
                for keyword in ms_office_keywords[product]:
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
                    return self.open_youtube_video(query), action
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
        
        # Greetings
        elif any(word in command for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greetings), action
        
        # Help
        elif any(word in command for word in ["help", "what can you do"]):
            return ("I can help you with:\n"
                   "- Telling time and date\n"
                   "- Weather information for major Indian cities\n"
                   "- Latest news headlines\n"
                   "- Wikipedia searches\n"
                   "- Google searches\n"
                   "- Gold prices in major Indian cities\n"
                   "- Microsoft Office help (Excel, Word, PowerPoint, Power BI)\n"
                   "- YouTube video searches and playback\n"
                   "- Opening websites in your browser\n"
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
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        
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
        <div style="background: linear-gradient(90deg, #0A66C2, #004182); color: white; padding: 12px; border-radius: 8px; text-align: center; margin-top: 20px;">
            <a href="https://www.linkedin.com/in/ashwik-bire-b2a000186" target="_blank" style="color: white; text-decoration: none;">
                Connect on LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        
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
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # Settings
        st.markdown("<h3 style='color: #FF4444;'>Settings</h3>", unsafe_allow_html=True)
        st.session_state.api_keys['weather'] = st.text_input("Weather API Key", value=st.session_state.api_keys['weather'], type="password")
        st.session_state.api_keys['news'] = st.text_input("News API Key", value=st.session_state.api_keys['news'], type="password")
        
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        st.markdown("### About JARVIS")
        st.info("JARVIS is an AI assistant designed to help with various tasks including weather, news, searches, Microsoft Office help, and more.")

def render_chat_interface():
    st.markdown('<div class="main-header">JARVIS AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                formatted_content = message["content"].replace('\n', '<br>')
                st.markdown(f'<div class="assistant-message"><strong>JARVIS:</strong> {formatted_content}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Your message:", placeholder="Type your message here...", key="user_input", label_visibility="collapsed")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("Send", use_container_width=True)
    
    # Process input
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get assistant response
        response, action = assistant.process_command(user_input)
        
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
        
        # Rerun to update the chat display
        st.rerun()

# Main application
def main():
    # Initialize assistant
    global assistant
    assistant = JarvisAssistant()
    
    # Navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose Mode", ["Chat", "Dashboard"])
    
    # Render sidebar
    render_sidebar()
    
    # Render main content based on selection
    if app_mode == "Chat":
        render_chat_interface()
    elif app_mode == "Dashboard":
        st.markdown('<div class="main-header">JARVIS Dashboard</div>', unsafe_allow_html=True)
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Current Time", datetime.datetime.now().strftime("%H:%M:%S"))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            weather_text = assistant.get_weather("Mumbai")
            temperature = weather_text.split("Temperature: ")[1].split("°C")[0] if "Temperature:" in weather_text else "N/A"
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Mumbai Temperature", f"{temperature}°C")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            gold_text = assistant.get_gold_price("Mumbai")
            gold_price = gold_text.split(": ")[1] if ": " in gold_text else "N/A"
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("Gold Price (Mumbai)", gold_price)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.metric("News Updates", "5 Today")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #FF0000, transparent); margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        # News section
        st.markdown("<h2 style='color: #FF4444;'>Latest News</h2>", unsafe_allow_html=True)
        articles = assistant.get_news()
        
        for i, article in enumerate(articles[:3]):
            with st.expander(f"{i+1}. {article['title']}"):
                st.write(article['description'] or "No description available")
                if article['url']:
                    st.markdown(f"[Read more]({article['url']})")

if __name__ == "__main__":
    main()
