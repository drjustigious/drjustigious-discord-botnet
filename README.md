# drjustigious-discord-botnet
A highly experimental Discord bot.

> Based on this tutorial:
> https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal

<img width="546" alt="bot-intro-screenshot" src="https://user-images.githubusercontent.com/44530293/114562467-3211ca00-9c77-11eb-87bf-07399eb25989.png">

---

## 1. Runtime environment setup
The following environment variables must be defined for the bot to run. They can be defined in a `.env` file next to `drjbot.py`.

| Environment variable | Description |
|---|---|
|`DISCORD_TOKEN`| The bot's authentication token. Obtained from the Bot tab here: https://discord.com/developers/applications/. |

There are also several other optional environment variables that can be defined to enable further functionality, e.g. related to using the OpenWeatherMap API. See `sample.env` for an up-to-date list of supported environment variables.

## 2. Launching the bot
With the packages listed in *requirements.txt* installed in your current Python 3 virtual environment, just run `drjbot.py`.
```
python ./drjbot.py
```
