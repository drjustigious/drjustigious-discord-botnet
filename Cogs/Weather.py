import os
import json
import logging
import requests

import fuzzywuzzy.process
from discord.ext import commands


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.towns_by_name = self.load_openweathermap_cities()


    def load_openweathermap_cities(self):
        """
        Construct a lookup dictionary for weather forecast cities (towns).
        """
        CITY_ID_FILE = os.getenv('OPENWEATHER_CITY_ID_FILE', "")
        if not CITY_ID_FILE:
            logging.warn("Could not construct weather report city table, the environment variable 'OPENWEATHER_CITY_ID_FILE' was not set.")
            return {}

        list_towns = []
        with open(CITY_ID_FILE) as jsonfile:
            list_towns = json.load(jsonfile)

        towns_by_name = {
            town["name"].lower().strip(): town for town in list_towns
        }

        return towns_by_name


    def resolve_target_town(self, town_name: str):
        """
        Given a town name, look up the closest match in the pre-loaded
        lookup table for the town details ('self.towns_by_name').
        """

        # Normalize the given town name into a query key.
        query_key = town_name.lower().strip()

        # Queries with just one letter don't make much sense.
        if len(query_key) <= 1:
            return None
        
        # Use fuzzy logic to determine the most probable city name.
        most_probable_key, matching_percentage = fuzzywuzzy.process.extractOne(
            query_key,
            self.towns_by_name.keys()
        )

        logging.debug(f"The closest key match to the town name '{town_name}' was '{most_probable_key}' at {matching_percentage}% matching ratio.")

        return self.towns_by_name[most_probable_key], matching_percentage
    

    @commands.command()
    async def weather(self, ctx, *, town: str = None):
        """
        Forecast weather for the given town in Finland.

        Arguments
        ---------
        town: str
            The name (or part of the name) of the town.

        Example
        -------
        !weather Turku
        """

        if not town:
            await ctx.send(f"{ctx.author.mention}, please give the name of the town you'd like a weather report for. Type `{self.bot.command_prefix}help weather` for details.")
            return

        if not self.towns_by_name:
            await ctx.send(f"Sorry {ctx.author.mention}, I'm having problems accessing the weather report data right now.")
            return

        target_town, matching_percentage = self.resolve_target_town(town)
        if not target_town:
            await ctx.send(f"Sorry {ctx.author.mention}, I couldn't identify a town based on that input.")
            return

        # Seems like we have a reasonable guess for the town the user asked about.
        town_resolution_comment = f"{ctx.author.mention} Here's the weather forecast for {target_town['name']}."
        if matching_percentage < 100:
            town_resolution_comment = f"{ctx.author.mention} I'm {matching_percentage}% sure you meant a town called {target_town['name']}, here's their weather forecast."

        weather_forecast = await self.fetch_weather_forecast(target_town)
        message = f"{town_resolution_comment}\n```\n{weather_forecast}```"

        await ctx.send(message)


    async def fetch_weather_forecast(self, target_town):

        api_key = os.getenv("OPENWEATHER_API_KEY")

        url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&id={target_town['id']}&appid={api_key}"
        response = requests.get(url=url)
        if not response.ok:
            logging.error(f"Error getting weather data: {response.status_code} {response.reason}\n{response.text}")
            return f"Error getting weather data: {response.status_code} {response.reason}. Somebody should check the bot's logs for details."

        report_lines = self.process_weather_report(
            response.json()
        )

        report_message = "\n".join(report_lines)
        return report_message


    def process_weather_report(self, data):
        target_timestamps = [
            "00:00:00",
            "06:00:00",
            "12:00:00",
            "18:00:00",
        ]

        num_reports = 4

        target_entries = [
            entry for entry in data.get("list", []) if any (
                timestamp in entry.get("dt_txt") for timestamp in target_timestamps
            )
        ][:num_reports]

        report_lines = []
        for entry in target_entries:
            report_lines.append(
                self.render_weather_report_datapoint(entry)
            )

        return report_lines


    def render_weather_report_datapoint(self, entry):
        line = f"[{entry.get('dt_txt', 'unknown time')}]\n"

        main = entry.get("main", {})
        temperature = f"{main.get('temp', '??')} °C"
        pressure = f"{main.get('pressure', '??')} hPa"
        humidity = f"{main.get('humidity', '??')}%"
        line += f"  T = {temperature}, P = {pressure}, RH = {humidity}\n"

        wind = entry.get("wind", {})
        degrees = wind.get('deg', 0)
        line += f"  wind: {wind.get('speed', '??')} m/s from {degrees}° ({self.describe_compass_angle(degrees)})\n"

        clouds = entry.get("clouds", {})
        line += f"  {clouds.get('all', '??')}% cloudy\n"

        got_precipitation = False

        if "snow" in entry:
            snow = entry["snow"]
            lst = list(snow.values())
            amount = lst[0] if lst else 0.00
            line += f"  snow {amount} mm in 3 h\n"
            got_precipitation = True

        if "rain" in entry:
            rain = entry["rain"]
            lst = list(rain.values())
            amount = lst[0] if lst else 0.00
            line += f"  rain {amount} mm in 3 h\n"
            got_precipitation = True

        if not got_precipitation:
            line += f"  no precipitation\n"

        weather_descriptions = entry.get("weather", [])
        description_strings = []
        for description in weather_descriptions:
            description_strings.append(
                description.get('description', 'undescribed weather')
            )

        line += "  "+", ".join(description_strings)

        return line


    def describe_compass_angle(self, degrees):
        index = int(degrees/22.5 + 0.5)
        choices = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

        return choices[(index % 16)]