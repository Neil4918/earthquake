import json
import os
import random

import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv

import discord
from earthquake import *

load_dotenv()
bot = commands.Bot(command_prefix="--")

data = sets(
    os.getenv("token"), APIToken=os.getenv("APIToken"),
    channels="966357190774493254"
)


def setup():
    try:
        open(data.checkFile)
    except:
        with open(data.checkFile, "w") as outfile:
            json.dump({}, outfile, ensure_ascii=False, indent=4)
            print("建立 check.json 完成")

@bot.event
async def on_ready():
    print(f'{bot.user.name} | 查看終端\n')
    print("-"*15)
    print('\n目前登入身份:',bot.user, 'ID:',bot.user.id)
    print("-"*20)
    setup()
    if data.APIToken:
        earthquake.start()
        print("\n地震報告已啟動")
        embed = discord.Embed(title="系統通知",
                              color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(
            name=f"台灣地震報告系統", icon_url='https://seeklogo.com/images/T/taiwan-logo-55EA4050B8-seeklogo.com.png')
        embed.add_field(
            name="地震報告已啟用", value=f"所有報告皆由[中央氣象局](https://opendata.cwb.gov.tw)提供\n如此系統有任何BUG請通知 <@天神Zhuyuan> !", inline=True
            ).add_field(
            name="資訊", value=f"Tag身分組: <>\n是否啟用Tag: True\n獲取方法: <#966357190774493254> 的[此訊息](https://discord.com/channels/880221036174532658/880512671613583390/925757760925229066)", inline=True)  # 報告連結
        embed.set_footer(
            text=f"地震報告提供", icon_url='https://media.discordapp.net/attachments/345147297539162115/732527875839885312/ROC_CWB.png')
        channel = bot.get_channel(965625262853222490)
        await channel.send(embed=embed)
    else:
        print("請至 https://opendata.cwb.gov.tw/userLogin 獲取中央氣象局TOKEN並放置於 .env 檔案中")

intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

@tasks.loop(seconds=10)
async def earthquake():
    # 大型地震
    API = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={data.APIToken}&format=JSON&areaName="
    # 小型地震
    API2 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={data.APIToken}&format=JSON"

    b = requests.get(API).json()
    s = requests.get(API2).json()
    _API = b["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API2 = s["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]

    async def goTo(how, now):
        for ch in data.channels:
            await sosIn(bot.get_channel(ch), ({API: b, API2: s}[how]), data)
        with open(data.checkFile, 'w') as outfile:
            json.dump(now, outfile, ensure_ascii=False, indent=4)

    with open(data.checkFile, "r") as file:
        file = json.load(file)
    for i in [API, API2]:
        if not file.get(i):
            file[i] = ""
    if file[API] != _API:
        file[API] = _API
        await goTo(API, file)
    if file[API2] != _API2:
        file[API2] = _API2
        await goTo(API2, file)

bot.run(data.token)
