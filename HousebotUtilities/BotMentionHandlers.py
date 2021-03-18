import logging

from . import UserIdentification


async def greet(bot, message):
    if message_is_greeting(message):
        other_mentions = extract_other_mentions(bot, message)
        if not other_mentions:
            await message.channel.send(f"Greetings, {message.author.mention}.")
        else:
            await message.channel.send(f"Greetings, {other_mentions[0].mention}. Please type `!help` to see what I can do for you.")

        return True

    return False


def message_is_greeting(message):
    lowercase_message = message.content.strip().lower()
    greetings = [
        "hello",
        "hi",
        "greet",
        "moi",
        "moro",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how do you do",
        "welcome"
    ]

    return any(greeting in lowercase_message for greeting in greetings)        



async def thanks(bot, message):
    if message_is_thankyou(message):
        await message.channel.send(f"You're welcome, {message.author.mention}.")
        return True

    if message_is_yourewelcome(message):
        await message.channel.send(f"Thank you, {message.author.mention}.")
        return True        

    return False


def message_is_thankyou(message):
    lowercase_message = message.content.strip().lower()
    greetings = [
        "thanks",
        "thank you",
        "you have my gratitude",
        "you have our gratitude",
        "fuck you"
    ]

    return any(greeting in lowercase_message for greeting in greetings)


def message_is_yourewelcome(message):
    lowercase_message = message.content.strip().lower()
    greetings = [
        "you're welcome",
        "my pleasure"
    ]

    return any(greeting in lowercase_message for greeting in greetings)



async def identify_user(bot, message):

    deep_command = extract_deep_command(bot, message)
    if not deep_command:
        return False

    if is_command_to_identify_bot(deep_command):
        await message.channel.send(
            UserIdentification.identify_self(bot, message)
        )
        return True

    if is_command_to_identify_author(deep_command):
        await message.channel.send(
            UserIdentification.identify_author(message)
        )
        return True        

    other_mentions = extract_other_mentions(bot, message)
    if not other_mentions:
        return False

    if is_command_to_identify_user(deep_command):
        await message.channel.send(
            UserIdentification.identify_user(other_mentions[0], message)
        )
        return True        

    other_mentions = extract_other_mentions(bot, message)

    return False


def is_command_to_identify_bot(deep_command_words):
    deep_command = " ".join(deep_command_words)

    return deep_command.startswith((
        "identify yourself",
        "identify thyself",
        "who are you",
        "who the hell are you",
        "who the fuck are you",
        "what are you",
        "what the hell are you",
        "what the fuck are you",
    ))


def is_command_to_identify_author(deep_command_words):
    deep_command = " ".join(deep_command_words)

    return deep_command.startswith((
        "identify me",
        "identify us",
        "who am i",
        "who the hell am i",
        "who the fuck am i",
        "what am i",
        "what the hell am i",
        "what the fuck am i"
    ))


def is_command_to_identify_user(deep_command_words):
    deep_command = " ".join(deep_command_words)

    return deep_command.startswith((
        "identify ",
        "who is ",
        "who are ",
        "who be ",
        "who the hell is ",
        "who the fuck is ",
        "what the hell is ",
        "what the fuck is"
    ))    


def extract_other_mentions(bot, message):
    """
    Returns a list of any mentions in the message that did not target the bot.
    """
    other_mentions = [ mention for mention in message.mentions if mention != bot.user ]
    return other_mentions


def extract_deep_command(bot, message):
    """
    Attempt to extract a deep command from the message.
    A deep command must begin with a mention of the bot.

    Returns the command words as a list, or an empty list if
    no command words could be extracted.
    """

    # The message must start with the bot's mention or it's not considered
    # a deep command.
    bot_mentioned_string = f"<@!{bot.user.id}>"  # This seems to differ from bot.user.mention by the char '!'.

    if not message.content.strip().startswith(f"{bot_mentioned_string}"):
        return []

    # Collect the non-blank words of the command. The first word will always be
    # the bot's mention.
    words = [word.strip().lower() for word in message.content.strip().split(" ") if word.strip()]

    return words[1:]