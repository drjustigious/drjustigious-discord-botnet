import datetime
import json

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATA_KEY_LENGTH = 16


def identify_user(user, message):
    """
    Returns a Discord message string identifying the given user or server member.
    """
    if user.bot:
        response = f"{message.author.mention} The entity {user.mention} is a bot "
    else:
        response = f"{message.author.mention} The entity {user.mention} is a human "

    if user.display_name == user.name:
        response += f"showing their true name."
    else:
        response += f"hiding their true name `{user.name}`."

    data = collect_user_data(user)

    rendered_data = []
    for key in data.keys():
        rendered_data.append(f"{key.ljust(DATA_KEY_LENGTH)}: {data[key]}")
    joined_data = "\n".join(rendered_data)

    response += f"\n```\n{joined_data}\n```"

    return response


def identify_author(message):
    """
    Returns a Discord message string identifying the author of the given message.
    """
    user = message.author

    if user.bot:
        response = f"{message.author.mention} You are a bot "
    else:
        response = f"{message.author.mention} You are a human "

    if user.display_name == user.name:
        response += f"showing your true name."
    else:
        response += f"hiding your true name `{user.name}`."

    data = collect_user_data(user)

    rendered_data = []
    for key in data.keys():
        rendered_data.append(f"{key.ljust(DATA_KEY_LENGTH)}: {data[key]}")
    joined_data = "\n".join(rendered_data)

    response += f"\n```\n{joined_data}\n```"

    return response


def collect_user_data(user):
    data = {
        "Shown name": user.display_name,
        "Username": user.name,
        "Discriminator": user.discriminator,
        "User ID": user.id,
        "Account created": user.created_at.strftime(DATETIME_FORMAT)+" UTC"
    }

    if hasattr(user, "joined_at"):
        data["Joined server"] = user.joined_at.strftime(DATETIME_FORMAT)+" UTC"

    if hasattr(user, "roles"):
        roles = [role.name for role in user.roles]
        data["Server roles"] = ", ".join(roles)

    return data

def identify_self(bot, message):
    """
    Returns a Discord message string identifying the bot itself.
    """
    response = f"{message.author.mention} I am the house bot **{bot.user.display_name}**."
    data = {
        "Shown name": bot.user.display_name,
        "Username": bot.user.name,
        "Discriminator": bot.user.discriminator,
        "User ID": bot.user.id,
        "Account created": bot.user.created_at.strftime(DATETIME_FORMAT)+" UTC",
        "Code revision": bot.version_string,
        "Online since": bot.online_since.strftime(DATETIME_FORMAT)+" UTC",
        "Uptime": calculate_uptime(bot)
    }

    #response += f"```\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```"
    rendered_data = []
    for key in data.keys():
        rendered_data.append(f"{key.ljust(DATA_KEY_LENGTH)}: {data[key]}")
    joined_data = "\n".join(rendered_data)

    response += f"\n```\n{joined_data}\n```"

    return response


def calculate_uptime(bot):
    uptime = datetime.datetime.utcnow() - bot.online_since
    uptime_minutes = int(round(uptime.total_seconds()/60))

    if uptime_minutes > 120:
        uptime_hours = uptime_minutes // 60
        return f"{uptime_hours} hours"

    return f"{uptime_minutes} minutes"