from time import strftime, localtime


async def begin():
    print(f"bot started {strftime('%I:%M %p, %m/%d', localtime())}")  # use %c for a full, pre-made date
