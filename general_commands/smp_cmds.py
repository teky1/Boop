import utilities.smp_run as server
from threading import Thread
from objects.result_obj import Result
import asyncio

allowed_guilds = [817412054050799626, 748241629747347556, 811439515830714378]
# escape, amongus, boop testing server

async def _smp(ctx):
    args = ctx.message.content.split()
    print(server.server_running)
    if ctx.guild.id not in allowed_guilds:
        await ctx.send("This command is for a private discord.")
        return
    if len(args) > 2 or (len(args)==2 and args[1].lower() != "start"):
         await ctx.send("Correct format is `!smp` to view the status of the SMP or `!smp start` to start the SMP")
         return
    if len(args) == 1:
        if server.server_running:
            await ctx.send(f"The SMP is running on the IP: {server.server_ip.replace('tcp://', '')}")
        else:
            await ctx.send(f"The SMP is not currently running, do `!smp start` to start it.")
    else:
        if server.server_running:
            await ctx.send(f"The SMP is already running on the IP: {server.server_ip.replace('tcp://', '')}")
        else:
            result = Result()
            result.result = None
            server_thread = Thread(target=server.startServer, args=("D:/Joel/rileys-server/server/TEKY_RUN.bat", result))
            server_thread.start()
            await ctx.send("Starting server... (please wait like 30 seconds)")
            while result.result == None:
                await asyncio.sleep(1)
            await ctx.send(f"IP: {result.result.replace('tcp://', '')}\n\nNote: The server could take up to 5 minutes to start so give it a minute. If the server doesn't start after 5 minutes dm Teky")
