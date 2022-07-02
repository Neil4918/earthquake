import discord
import datetime


class sets:
    __slots__ = ["checkFile", "channels", "Tags", "APIToken", "token"]

    def __init__(self, token, APIToken=None, **kwargs):
        self.checkFile = kwargs.get("checkFile", "check.json")
        self.channels = list(map(int, kwargs.get("channels", "").split()))
        self.APIToken = APIToken
        self.token = token


def checkSos(ac):
    return {
        "0": "⚪",
        "1": "⚪",
        "2": "🟡",
        "3": "🟢",
        "4": "🟢",
        "5": "🔴",
        "6": "🟤",
        "7": "🟤",
        "8": "🟣",
        "9": "⚫"
    }[str(int(ac))] + " "

def checkSos_txt(ac_txt):
    return {
        "0": "無感",
        "1": "微震",
        "2": "輕震",
        "3": "弱震",
        "4": "中震",
        "5": "強震",
        "6": "烈震",
        "7": "劇震",
        "8": "劇震",
        "9": "劇震"
    }[str(int(ac_txt))] + ""


async def sosIn(channel, data, sets: sets):
    try:
        inp = data["records"]["earthquake"][0]
        inpInfo = inp["earthquakeInfo"]

        helpAwa = inp["web"]  # 資料連結
        earthquakeNo = inp["earthquakeNo"]  # 幾號地震

        location = inpInfo["epiCenter"]["location"]  # 發生地點
        originTime = inpInfo["originTime"]  # 發生時間
        magnitudeType = inpInfo["magnitude"]["magnitudeType"]  # 規模單位
        magnitudeValue = inpInfo["magnitude"]["magnitudeValue"]  # 規模大小
        value = inpInfo["depth"]["value"]  # 地震深度
        unit = inpInfo["depth"]["unit"]  # 深度單位
        urlicon = inp["reportImageURI"]  # 深度單位
        cha = checkSos(magnitudeValue)
        cha_txt = checkSos_txt(magnitudeValue)
        embed = discord.Embed(title=data['records']['datasetDescription'],
                              color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(
            name="台灣地震報告系統", icon_url='https://seeklogo.com/images/T/taiwan-logo-55EA4050B8-seeklogo.com.png')
        embed.set_image(url=f"{urlicon}")
        embed.add_field(
            name="報告連結", value=f"[中央氣象局]({helpAwa})", inline=True)  # 報告連結
        embed.add_field(name="編號", value=f"{earthquakeNo}", inline=True)  # 編號
        embed.add_field(name="震央位置", value=f"{location}", inline=True)  # 震央位置
        embed.add_field(
            name="發生時間", value=f"{originTime}", inline=True)  # 發生時間
        embed.add_field(name=f"{magnitudeType}",
                        value=f"{str(cha)}{magnitudeValue} ({cha_txt})", inline=True)  # 規模
        embed.add_field(name="深度", value=f"{value}{unit}", inline=True)  # 發生時間
        embed.set_footer(
            text="地震報告提供", icon_url='https://media.discordapp.net/attachments/345147297539162115/732527875839885312/ROC_CWB.png')

        inp2 = inp["intensity"]["shakingArea"]
        for i in range(1, 10):
            for a in inp2:
                if str(i) in a["areaDesc"]:
                    if "最大震度" in a["areaDesc"]:
                        ai1 = a['areaDesc']
                        ai2 = a['areaName']
                        embed.add_field(name=f" {ai1} :",
                                        value=f"{ai2}", inline=False)
        await channel.send(f"<>\n:house_abandoned: **{cha_txt}** 報告!", embed=embed)
    except Exception as err:
        print(err)