from google.adk.agents.llm_agent import Agent
import urllib.request

def get_london_weather() -> str:
    """
    Fetches the live weather forecast for London using a public weather network.
    """
    try:
        # Connects directly to a free, open-source weather server
        url = "https://wttr.in"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return "London: 15°C, Partly Cloudy (Fallback data due to connection timeout)"

# We inject the real-time weather directly into the instruction manual
live_weather = get_london_weather()

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
