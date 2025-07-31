import os
import requests
from google import genai
from google.genai import types

# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# WEATHER_API_KEY = ""
# WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

client = genai.Client(api_key=GEMINI_API_KEY)

WEATHER_TOOL = types.Tool(
    function_declarations=[
        {
            "name": "get_weather",
            "description": "Provides the current weather conditions, including temperature and precipitation forecast, for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city and state, e.g., 'San Francisco, CA' or 'Honolulu, HI'"
                    }
                },
                "required": ["city"]
            }
        }
    ]
)

GENERATION_CONFIG = types.GenerateContentConfig(tools=[WEATHER_TOOL])
MODEL = "gemini-1.5-flash"

def get_weather_from_api(city: str) -> str:
    """Calls the weather API and returns a formatted weather string."""
    print(f"[Weather API] Fetching weather for {city}...")
    try:
        response = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": city}
        )
        response.raise_for_status()
        weather_data = response.json()
        condition = weather_data['current']['condition']['text']
        temp_c = weather_data['current']['temp_c']
        weather_info = f"{condition}, {temp_c}°C"
        print(f"[Weather API] {city}: {weather_info}")
        return weather_info
    except requests.exceptions.RequestException as e:
        print(f"[Weather API] Error: {e}")
        return "Error fetching weather data."
    except KeyError:
        print("[Weather API] Error: Invalid response format.")
        return "Error parsing weather data."


def run_gemini_conversation(user_prompt: str):
    """Starts a conversation with Gemini, handling function calls."""
    print(f"[User] {user_prompt}")

    # 1. Send the initial prompt to Gemini
    initial_response = client.models.generate_content(
        model=MODEL,
        contents=[types.Content(role="user", parts=[types.Part(text=user_prompt)])],
        config=GENERATION_CONFIG
    )

    part = initial_response.candidates[0].content.parts[0]

    # 2. Check if Gemini requested a tool call
    if not part.function_call:
        print("\n[Gemini] No tool call, raw response:")
        print(initial_response.text)
        return

    function_call = part.function_call
    city = function_call.args.get("city")

    if not city:
        print("\n[Gemini] Tool call requested, but 'city' argument is missing.")
        return

    print(f"[Gemini requested tool] {function_call.name}(city='{city}')")

    # 3. Call the actual tool (our weather function)
    weather_info = get_weather_from_api(city)

    # 4. Send the tool's response back to Gemini
    final_response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            types.Content(role="model", parts=[part]), # Gemini's request
            types.Content(
                role="function",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            response={"weather_info": weather_info}
                        )
                    )
                ]
            )
        ],
        config=GENERATION_CONFIG
    )

    print("\n[Gemini Final Answer]")
    print(final_response.text)


if __name__ == "__main__":
    # Using a more direct prompt to test the tool call for Honolulu.
    user_query = "Do I need an umbrella in Honolulu, HI?"
    run_gemini_conversation(user_query)