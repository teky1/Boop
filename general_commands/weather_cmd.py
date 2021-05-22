import discord
import json
import requests

def ktof(t):
    return t*(9/5)-459.67

def getWeatherImg(code):
    return f"http://openweathermap.org/img/wn/{code}@2x.png"

def makeReq(query):
    with open("other_keys.json") as json_file:
        key = json.load(json_file)["weather"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={key}"
    result = requests.get(url).json()
    if result["cod"] == 200:
        return {
            "success": True,
            "city": result["name"],
            "weather": result["weather"][0]["description"].title(),
            "temp": ktof(result["main"]["temp"]),
            "high": ktof(result["main"]["temp_max"]),
            "low": ktof(result["main"]["temp_min"]),
            "clouds": f'{result["clouds"]["all"]}%',
            'humidity': f'{result["main"]["humidity"]}%',
            "image": getWeatherImg(result["weather"][0]["icon"])
        }
    print(result)
    return {"success": False}

async def _weather(ctx):
    async with ctx.typing():
        r = makeReq("ellicott city")
        if r["success"]:
            embed = discord.Embed(title=r["weather"])
            embed.set_author(name=r["city"])
            embed.set_thumbnail(url=r["image"])
            embed.add_field(name="Temp", value=f"{round(r['temp'])}°F", inline=True)
            embed.add_field(name="High", value=f"{round(r['high'])}°F", inline=True)
            embed.add_field(name="Low", value=f"{round(r['low'])}°F", inline=True)
            embed.add_field(name="Clouds", value=r["clouds"], inline=True)
            embed.add_field(name="Humidity", value=r["humidity"], inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Uh oh! Something went wrong :P")