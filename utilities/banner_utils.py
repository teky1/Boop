import math
import random
import discord

minsize = 50
minspacing = 3
border = 8
percycle = 1
theattempts = 3
attemptincrement = 1
coordx = 124
coordy = 248
ogpfpsize = 86

pfps = []


def dist(x, y, newx, newy):
    uhm = (x - newx) * (x - newx) + (y - newy) * (y - newy)
    uhm = math.sqrt(uhm)
    return uhm


def newdot():
    global pfps
    x = 2*minspacing+minsize+random.random()*(600-4*minspacing-2*minsize)
    y = 2 * minspacing + minsize + random.random() * (240 - 4 * minspacing - 2 * minsize)
    if dist(x, y, coordx, coordy) <= (minspacing + minsize * 1.5 + ogpfpsize):
        return

    for pfp in pfps:
        if dist(x, y, pfp[1], pfp[2]) <= minspacing + minsize + pfp[0]:
            return
    pfps.append([0, x, y])


def newdots():
    global pfps
    start = len(pfps)
    attempts = 0
    while len(pfps) < start + percycle:
        newdot()
        attempts += 1
        if attempts > 200:
            return


def makebig():
    global pfps
    finished = False
    attempts = 0
    while (finished is False) and (attempts <= theattempts):
        finished = True
        for thispfp in pfps:
            tooclose = False
            if dist(thispfp[1], thispfp[2], coordx, coordy) <= (minspacing + thispfp[0]*1.1 + ogpfpsize*1.1):
                tooclose = True
            elif(thispfp[1] < thispfp[0] + border) or (thispfp[2] < thispfp[0] + border) or \
                    (thispfp[1] > 600 - thispfp[0] - border) or (thispfp[2] > 240 - thispfp[0] - border):
                tooclose = True
            else:
                for pfp in pfps:
                    if thispfp != pfp:
                        if dist(thispfp[1], thispfp[2], pfp[1], pfp[2]) <= (minspacing + thispfp[0]*1.1 + pfp[0]*1.1):
                            tooclose = True
                        else:
                            finished = False
            if tooclose is False:
                thispfp[0] += attemptincrement
        attempts += 1


def tweak():
    global pfps
    xlist = []
    ylist = []
    for thispfp in pfps:
        avoidx = 0
        avoidy = 0
        for pfp in pfps:
            if thispfp != pfp:
                thedistance = dist(thispfp[1], thispfp[2], pfp[1], pfp[2])
                repel = 1/math.pow(thedistance - thispfp[0] - pfp[0], 2)
                xdist = thispfp[1]-pfp[1]
                ydist = thispfp[2]-pfp[2]
                if ydist >= 0:
                    angle = math.atan(xdist/ydist)
                else:
                    angle = math.atan(xdist/ydist) + math.pi
                avoidx += repel*math.sin(angle)
                avoidy += repel*math.cos(angle)
        xdist = thispfp[1] - coordx
        ydist = thispfp[2] - coordy
        if ydist >= 0:
            angle = math.atan(xdist / ydist)
        else:
            angle = math.atan(xdist / ydist) + math.pi

        ogrepel = math.pow(dist(thispfp[1], thispfp[2], coordx, coordy) - thispfp[0] - ogpfpsize, 2)
        avoidx += math.sin(angle)/ogrepel
        avoidy += math.cos(angle)/ogrepel

        avoidx += 1 / math.pow(thispfp[1] - thispfp[0] - 6, 2)
        avoidy += 1 / math.pow(thispfp[2] - thispfp[0] - 6, 2)
        avoidx += -1 / math.pow(600 - thispfp[1] - thispfp[0] - 6, 2)
        avoidy += -1 / math.pow(240 - thispfp[2] - thispfp[0] - 6, 2)
        xlist.append(avoidx * 10)
        ylist.append(avoidy * 10)
    for i in range(len(pfps)):
        pfps[i][1] += xlist[i]
        pfps[i][2] += ylist[i]


def generate():
    global pfps
    global minsize
    minsize = 50
    k = 0
    while k < 50:
        j = 0
        while j < 15:
            newdots()
            makebig()
            if minsize >= 12:
                minsize -= 0.5
            j += 1

        j = 0
        while j < 30:
            tweak()
            makebig()
            j += 1
        k += 1
    # return pfps


def check():
    global pfps
    for thispfp in pfps:
        if (thispfp[1] < thispfp[0] + border + 1) or (thispfp[2] < thispfp[0] + border + 1) or \
                (thispfp[1] > 600 - thispfp[0] - border - 1) or (thispfp[2] > 240 - thispfp[0] - border - 1):
            return 1
    return 0


async def importmenoballs(message):
    global pfps
    pfps = []
    generate()
    fails = 0
    while check():
        print("check failed!!")
        if fails == 0:
            await message.edit(message.content+" ... uhm")
        elif fails == 1:
            await message.edit(message.content+" ... uhm ... oh no")
        elif fails == 2:
            await message.edit(message.content+" ... uhm ... oh no ... this is hard ok :(")
        elif fails > 2:
            await message.edit(message.content + " ... uhm ... oh no ... this is hard ok :(" + (fails - 2) * " :(")
        fails += 1
        pfps = []
        generate()
    return pfps
