import discord
from discord.ext import commands

import requests
from lxml import html

code_map = {
    "Code Orange": 16753920,
    "Code Red": 15400960,
    "Code Yellow": 16766720,
    "Code Blue": 255,
    "Code Green": 32768
}

async def _hcpss(ctx: commands.Context):

    parsed_site = html.fromstring(requests.get("http://status.hcpss.org").text)
    status = parsed_site.xpath('//*[@id="status-block"]/div/h2')[0].getchildren()


    response = {
        "title": "HCPSS Status",
        "description": status[0].text,
        "url": "https://status.hcpss.org",
        "color": code_map[status[1].text],
        "thumbnail": {
            "url": "https://hcpss.me/images/hcpss-logo-outlined.png"
        },
        "fields": [
            {
                "name": status[1].text,
                "value": status[2].text
            }
        ]
    }

    embed = discord.Embed.from_dict(response)
    await ctx.send(embed=embed)
