# Bomba_bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random, json, os

API_ID = 24196085
API_HASH = "d6021ffa5d25707aec43d6b860fb7ead"
BOT_TOKEN = "7633932908:AAFXKz-eqfBO84kEBSRzSU0kdXvViB68BD0"
ADMIN_ID = 7086597366

client = Client("bomba_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

users_data = {}

def save_data():
    with open("data.json", "w") as f:
        json.dump(users_data, f)

def load_data():
    global users_data
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            users_data = json.load(f)

@client.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = str(message.from_user.id)
    if user_id not in users_data:
        users_data[user_id] = {"balance": 15}
        save_data()
    name = message.from_user.first_name
    await message.reply(f"Салом {name}!\nХуш омадед ба Бомба Бот!\nШумо бонуси 15 сомонӣ гирифтед.")

@client.on_message(filters.command("balance"))
async def balance(client, message: Message):
    user_id = str(message.from_user.id)
    bal = users_data.get(user_id, {}).get("balance", 0)
    await message.reply(f"Боқимонда: {bal} сомонӣ")

@client.on_message(filters.command("deposit"))
async def deposit(client, message: Message):
    await message.reply("Барои амонатгузорӣ бо админ тамос гиред.")

@client.on_message(filters.command("withdraw"))
async def withdraw(client, message: Message):
    user_id = str(message.from_user.id)
    bal = users_data.get(user_id, {}).get("balance", 0)
    if bal < 350:
        await message.reply("Барои гирифтани пул ҳадди ақал 350 сомонӣ лозим аст.")
    else:
        await message.reply("Дархости гирифтани пул қабул шуд. Дар 24 соат пардохт мешавад.")

@client.on_message(filters.command("play"))
async def play(client, message: Message):
    user_id = str(message.from_user.id)
    bal = users_data.get(user_id, {}).get("balance", 0)
    if bal < 1:
        await message.reply("Барои бозӣ маблағи кофӣ нест!")
        return
    bombs = random.sample(range(25), 3)
    grid = ""
    for i in range(25):
        if i in bombs:
            grid += "💣 "
        else:
            grid += "💎 "
        if (i + 1) % 5 == 0:
            grid += "\n"
    users_data[user_id]["balance"] -= 1
    save_data()
    await message.reply(f"Натиҷаи бозӣ:\n{grid}\nШумо бохтед! -1 сомонӣ")

load_data()
client.run()
