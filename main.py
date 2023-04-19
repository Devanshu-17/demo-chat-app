import streamlit as st
from streamlit_chat import message
import requests

# Set up MediaWiki API endpoint
wiki_url = "https://en.wikipedia.org/w/api.php"

st.sidebar.title("Tourist Chatbot")
st.sidebar.markdown(
    """
    This is a simple chatbot that can answer questions about the weather and give you Wikipedia results.

    The weather data is provided by [OpenWeather](https://openweathermap.org/).

    The Wikipedia results are provided by [MediaWiki](https://www.mediawiki.org/wiki/API:Main_page).

    """
)
st.sidebar.header("Note: To get the weather for a city, you need to specifically ask [Temperature of <city name>]")

def get_wiki_results(query):
    # Set parameters for MediaWiki API request
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srprop": "",
        "utf8": "",
        "formatversion": "2",
    }
    # Send API request and parse results
    response = requests.get(wiki_url, params=params)
    data = response.json()
    results = data["query"]["search"]
    return results


def get_weather(city_name):
    # first, get the coordinates of the city using the OpenWeather geocoding API
    api_key = "836387f978d917ff377bc10c387b150c"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url).json()

    # check if we got a valid response from the API
    if len(response) == 0:
        return "Sorry, I could not find the city you requested."

    # get the coordinates of the city from the API response
    lat = response[0]["lat"]
    lon = response[0]["lon"]

    # now, use the coordinates to get the current weather from the OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    # check if we got a valid response from the API
    if response["cod"] != 200:
        return "Sorry, I could not get the weather for the city you requested."

    # get the temperature and description from the API response
    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]

    # format the response message
    msg = f"The temperature in {city_name.title()} is {temp:.1f}°C and the weather is {desc}."
    return msg


# Set up Streamlit app
st.title("Tourist Chatbot")

# Initialize chat widget
message("Hi! I'm your Tourist Chatbot. Ask me anything!")

# while True:
user_input = st.text_input("You:", key="input_1")
if user_input:
    if "temperature of" in user_input.lower():
        city_name = user_input.lower().replace("temperature of", "").strip()
        weather_msg = get_weather(city_name)
        message(weather_msg, is_user=False)
    else:
        results = get_wiki_results(user_input)
        if len(results) > 0:
            message("Here are some results:", is_user=False)
            for result in results:
                message("- " + result["title"], is_user=False)
        else:
            message("Sorry, I couldn't find any results.", is_user=False)
