import discord
from discord.ext import commands
import json

TOKEN = "YOUR_BOT_TOKEN"  # ใส่ Token ของบอทที่นี่

# โหลดเลขประจำตัวจากไฟล์ (ถ้ามี)
try:
    with open("user_ids.json", "r") as f:
        user_ids = json.load(f)
except FileNotFoundError:
    user_ids = {}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    global user_ids
    
    # ถ้าผู้ใช้ยังไม่มีเลข ให้กำหนด
    if str(member.id) not in user_ids:
        new_id = len(user_ids) + 1
        user_ids[str(member.id)] = f"{new_id:03}"  # เลข 3 หลัก เช่น 001, 002
        
        # บันทึกลงไฟล์
        with open("user_ids.json", "w") as f:
            json.dump(user_ids, f, indent=4)
        
    # เปลี่ยนชื่อเล่นให้ผู้ใช้
    try:
        await member.edit(nick=f"[{user_ids[str(member.id)]}] {member.name}")
    except discord.Forbidden:
        print(f"❌ ไม่มีสิทธิ์เปลี่ยนชื่อ {member.name}")

bot.run(TOKEN)
