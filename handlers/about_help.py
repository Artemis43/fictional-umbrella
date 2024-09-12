from aiogram import types
from middlewares.authorization import is_private_chat, is_user_member
from config import REQUIRED_CHANNELS

# Command to display help information
async def help(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        help_text = (
            "**PC Games Bot 🪄**\n\n"
            "**💫 How to Use:**\n\n"
            "|- Search for your game in the list using the keyboard\n\n"
            "|- Paste the game name after /get\n\n"
            "|- Send and get your files👌\n\n"
            "**NOTE:\n\n**"
            "`Files are in .bin form\nDue to Telegram's restrictions, they are split into 2 GB or 4 GB files. Merge them before install.`\n\nRefer: [Installation Guide](https://t.me/fitgirl_repacks_pc/969/970)\n\n"
            "**Happy Gaming 🔥**"
        )
        await message.reply(help_text, parse_mode='Markdown')

# Command to display help information
async def about(message: types.Message):
    if not is_private_chat(message):
        return
    user_id = message.from_user.id
    if not await is_user_member(user_id):
        join_message = "Welcome to PC Games Bot 🪄\n\nI have repacked PC game files downloaded from original sources 👾\n\nA new game uploaded every day 👻\n\nPlease join our update channels and help us grow our community 😉\n"
        for channel in REQUIRED_CHANNELS:
            join_message += f"{channel}\n"
        await message.reply(join_message)
    else:
        about_text = (
            "*PC Games Bot* 🥳\n\n"
            "Bots always amazed me, so I though of creating one. Managing my studies and creating this bot was difficult 🥲\n"
            "This bot still has a lot of scope for development and automation though\n\n"
            "Happy Gaming 💥"
        )
        await message.reply(about_text, parse_mode='Markdown')
