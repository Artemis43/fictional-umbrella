from aiogram import types
from middlewares.authorization import is_private_chat, is_user_member
from config import REQUIRED_CHANNELS

# Command to display help information
async def help(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every 3 hours 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        help_text = (
            "**PC Games Bot 🪄**\n\n"
            "**💫 How to Use:**\n\n"
            "|- Search for your game in the list\n\n"
            "|- Tap on the game name to copy it\n\n"
            "|- Long press on /get\n\n"
            "|- Paste the game name after /get\n\n"
            "|- Send and get your files👌\n\n"
            "**NOTE:\n\n**"
            "`Files are in .bin form\nDue to Telegram's restrictions, they are split into 2 GB or 4 GB files. Merge them before install.`\n\nRefer: [Click here](https://t.me/fitgirl_repacks_pc/969/970)\n\n"
            "**Happy Gaming 🔥**"
        )
        await message.reply(help_text, parse_mode='Markdown')

# Command to display help information
async def about(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every 3 hours 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        about_text = (
            "**PC Games Bot 🪄**\n\nBots always amazed me. You really never know how few lines of code could change the way you do things\n\n"
            "I was introduced to FG-repacks very recently, and the very first problem I encountered was the time needed for downloading of files... 😑\n"
            "So, here it is. I made this bot to save your time downloading torrents 🙌\n\nHope this helps those curious and enthusiastic gamers out there 😄\n\nIn the end, I always recommend purchasing these games 👾\n\n"
            "This is the first bot I made. It took me 20 long days to make this bot working as it is now. The games are added automatically at regular intervals and our Archive is ever-growing 🔥\n\n"
            "Platform - `Render`\n"
            "Usage limit - `0.1 CPU|512 MB (RAM)`\n\n"
            "Happy Gaming 💥"
        )
        await message.reply(about_text, parse_mode='Markdown')
