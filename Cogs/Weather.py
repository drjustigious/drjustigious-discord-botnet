import os
import json
import logging

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
            await ctx.send(f"<@{ctx.author.id}>, please give the name of the town whose weather you're interested in. Type `{self.bot.command_prefix}help weather` for details.")
            return

        if not self.towns_by_name:
            await ctx.send(f"Sorry <@{ctx.author.id}>, I'm having problems accessing the weather report data right now.")
            return

        target_town, matching_percentage = self.resolve_target_town(town)
        if not target_town:
            await ctx.send(f"Sorry <@{ctx.author.id}>, I couldn't identify a town based on that input.")
            return

        # Seems like we have a reasonable guess for the town the user asked about.
        town_resolution_comment = f"<@{ctx.author.id}>, here's the weather forecast for {target_town['name']}."
        if matching_percentage < 100:
            town_resolution_comment = f"<@{ctx.author.id}>, I'm {matching_percentage}% sure you meant a town called {target_town['name']}, here's their weather forecast."

        weather_forecast = await self.fetch_weather_forecast(target_town)
        message = f"{town_resolution_comment}\n```\n{weather_forecast}```"

        await ctx.send(message)


    async def fetch_weather_forecast(self, target_town):
        return "Some\nlines\nof randomness.\n"