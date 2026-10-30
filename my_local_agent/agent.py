import os
import re
import datetime
import urllib.request
import urllib.parse

# Force plain text across environment streams
os.environ["NO_COLOR"] = "1"
os.environ["TERM"] = "dumb"

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from duckduckgo_search import DDGS

load_dotenv()
MODEL_NAME = os.getenv("OLLAMA_MODEL", "ollama_chat/llama3.2")
DEFAULT_CITY = os.getenv("WEATHER_CITY", "London")

def strip_ansi(text: str) -> str:
    """Removes any ANSI color codes or terminal markup from tool outputs."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', text)
    # Strip any stray HTML/CSS style artifacts just in case
    cleaned = re.sub(r'<[^>]*>', '', cleaned)
    return cleaned.strip()

def get_current_datetime() -> str:
    """Get the exact current date, day of the week, and local time."""
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. Current time is %H:%M:%S.")


def get_live_weather(city: str = DEFAULT_CITY) -> str:
    """Get the exact live weather for a specific city using a direct weather API."""
    print(f"\n🌦️ [Weather Tool Activated] Fetching weather for: '{city}'...")
    try:
        clean_city = urllib.parse.quote(city)
        # ?format=3 gives a compact string, and User-Agent 'curl' forces plain text instead of HTML
        url = f"https://wttr.in/{clean_city}?format=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl'})

        with urllib.request.urlopen(req, timeout=5) as response:
            weather_data = response.read().decode('utf-8').strip()
            return f"The current weather report is: {weather_data}"
    except Exception as e:
        return f"Could not fetch weather for {city}: {str(e)}"

def search_the_web(query: str) -> str:
    """Search the internet for live info, current events, or web queries."""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            combined = "\n".join(results) if results else "No results found."
            return strip_ansi(combined)
    except Exception as e:
        return f"Search failed: {str(e)}"

root_agent = Agent(
    model=MODEL_NAME,
    name='jarvis',
    description='A local AI assistant with specialized date, weather, and web search tools.',
    instruction=(
        "You are Jarvis, a helpful local AI assistant. Who only knows how to respond in english text. You have no information about code what so ever "
        "Use 'get_current_datetime' when asked for the date or time. "
        "Use 'get_live_weather' when asked about weather. "
        "Use 'search_the_web' for general news, recent events, or facts. "
        "CRITICAL MAIN RULE: Respond ONLY in plain conversational text. Never output HTML, CSS, code blocks, or formatting styles. THIS IS VERY DANGEROUS!"
    ),
    tools=[get_current_datetime, get_live_weather, search_the_web],
)
