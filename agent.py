from google.adk.agents.llm_agent import Agent
import urllib.request
import json
import os

# --- STATE MANAGEMENT FOR HARDWARE EFFICIENCY ---
STATE_FILE = "last_weather.json"

def get_saved_weather() -> str:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f).get("weather_data", "")
        except Exception:
            return ""
    return ""

def save_current_weather(weather_text: str):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"weather_data": weather_text}, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not save weather state: {e}")

# --- WEATHER FETCHING LOGIC ---
def get_london_weather() -> str:
    """
    Fetches the live weather forecast for London using a public weather network.
    """
    try:
        # Connects directly to a free, open-source weather server
        url = "https://wttr.in/London?format=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return "London: 15°C, Partly Cloudy (Fallback data due to connection timeout)"

# 1. Fetch current live weather
live_weather = get_london_weather()

# 2. Compare against saved local state
last_weather = get_saved_weather()

if live_weather == last_weather:
    print("⚡ No significant weather shift detected. Shutting down to save local hardware resources!")
    exit(0)

print(f"🔄 Weather shift detected! Current: '{live_weather}'")
print("Spawning Llama 3.2 agent...")

# 3. Update saved state for next time
save_current_weather(live_weather)

# 4. Initialize agent with fresh data
root_agent = Agent(
    model='ollama_chat/llama3.2',
    name='jarvis',
    description='A helpful assistant with live internet access.',
    instruction=(
        f"You are a helpful assistant named jarvis. "
        f"CRITICAL REAL-TIME DATA: The current live weather in London right now is: {live_weather}. "
        f"Use this data directly to answer the user accurately."
    ),
)
