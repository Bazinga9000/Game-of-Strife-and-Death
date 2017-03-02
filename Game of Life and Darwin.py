import pygame,random,copy,time,operator,math,json,datetime,multiprocessing
from threading import Thread



if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((1300,760))

    grid = [[0 for i in range(16)] for j in range(8)]
    gridtocol = {0 : (255,255,255), 1 : (204,0,0), 2 : (0,0,204), 3 : (100,100,100), 4 : (204,0,204)}
    gamemode = 0
    font = pygame.font.SysFont("Trebuchet MS", 25)
    bigfont = pygame.font.SysFont("Trebuchet MS", 45)
    smallfont = pygame.font.SysFont("Trebuchet MS", 18)
    gen = 0
    archgen = 0
    currentlyinputting = 0
    inputstring = ""
    mod = 0
    archive = []
    backupcreatures = []
    battlecount = 0
    rulestring = [[3],[2,3],0,0]

    b64 = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
           'S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
           'u','v','w','x','y','z','-','=']

    gridcreatures = ["No Creature","No Creature"]

    stats = ["No Creature","NaN","NaN","NaN","NaN"]
    stats2 = ["No Creature","NaN","NaN","NaN","NaN"]

    shift = 0

def draw(gamemode):
    surface.fill((204, 204, 204))

    squaresize = 800 // 16


    if gamemode == 0:
        title = bigfont.render("Game of Strife and Death",True,(0,0,0))
        text = font.render("It appears you don't have any creatures yet! Press SPACE to generate 50 random creatures!",True,(0,0,0))
        notice = font.render("Make sure you've read the README file so you understand how you do things!",True,(204,0,0))
        surface.blit(title,(350,50))
        surface.blit(text,(75,300))
        surface.blit(notice,(160,500))
    if gamemode == 1:
        for x in range(16):
            for y in range(8):
                rect = (x * squaresize, 65 + y * squaresize, squaresize, squaresize)
                pygame.draw.rect(surface, gridtocol[grid[y][x]], rect)
                pygame.draw.rect(surface, (0, 0, 0), rect, 1)

        for i in [0,10,20,30,40]:
            for j in range(10):
                if i+j >= len(creatures):
                    break

                creaturename = findname(creatures[i + j])


                color1 = 204 if creaturename == gridcreatures[0] else 0
                color3 = 204 if creaturename == gridcreatures[1] else 0

                name = smallfont.render(creaturename, True, (color1, 0, color3))

                surface.blit(name,(170*i/10,(65 + 8 * squaresize) + (30*j)))

        currentlyviewing = font.render(str("Red Creature: " + gridcreatures[0] + " | Blue Creature: " + gridcreatures[1]),True,(0,0,0))
        surface.blit(currentlyviewing,(10,5))
        rulestringt = font.render(str("Rulestring: " + str(rulestring)),True,(0,0,0))
        surface.blit(rulestringt,(10,30))

        if currentlyinputting != 0:
            if currentlyinputting == 1:
                inputtext = font.render(str("Inputting Custom Red Creature " + inputstring),True,(204,0,0))
            if currentlyinputting == 2:
                inputtext = font.render(str("Inputting Custom Blue Creature " + inputstring),True,(0,0,204))
            if currentlyinputting == 3:
                inputtext = font.render(str("Inputting Custom Rulestring " + inputstring),True,(0,204,0))
            if currentlyinputting == 4:
                inputtext = font.render(str("Warping to Generation " + inputstring),True,(204,109,0))
            surface.blit(inputtext,(700,10))

        generationtext = font.render(str("Viewing Generation " + str(archgen) + ", Latest is " + str(gen)),True,(0,0,0))

        surface.blit(generationtext,(820,720))

        if stats[0] != "No Creature":
            lines = ["Creature %s", "Created During Generation %s", "Scored %s Point(s) Last Generation",
                     "Amassed %s Population Last Generation", "Scored %s Point(s) up to this Gen.",
                     "Amassed %s Population up to this Gen."]

            for n, line in enumerate(lines):
                img = font.render(line % stats[n], True, (204, 0, 0))
                surface.blit(img, (820, 65 + 25 * n))

        if stats2[0] != "No Creature":
            lines = ["Creature %s", "Created During Generation %s", "Scored %s Point(s) Last Generation",
                     "Amassed %s Population Last Generation", "Scored %s Point(s) up to this Gen.",
                     "Amassed %s Population up to this Gen."]

            for n, line in enumerate(lines):
                img = font.render(line % stats2[n], True, (0, 0, 204))
                surface.blit(img, (820, 225 + 25 * n))


        lines = ["Left and Right - View other Generations","A - ASAP Generation","F - Fast Generation",
                 "S - Slow Generation","B - Battle the 2 creatures on the grid","I - Do one Iteration",
                 "Left/Right Control - Input Custom Creature Names","Left Alt: Input Custom Rulestring",
                 "Escape - Clear Grid/Exit Custom Input","1-9 - Save in Slot","F1-F9 - Load from Slot",
                 "G - Sort by Generation Created","R - Sort by Rank","P - Sort by Population",
                 "O - Sort by overall Score", "U - Sort by overall Population","W - Warp to Generation"]

        for n,line in enumerate(lines):
            ctrl = smallfont.render(line, True, (0,0,0))
            surface.blit(ctrl, (820, 450 + 15 * n))




def getneighbors(row,col,indx):
    if indx == 0:
        return [[row + 1, col], [row + 1, col + 1], [row + 1, col - 1], [row, col + 1], [row, col - 1], [row - 1, col - 1],
         [row - 1, col], [row - 1, col + 1]]
    elif indx == 1:
        return [[row + 1, col], [row, col + 1], [row, col - 1], [row - 1, col]]
    elif indx == 2:
        return [[row + 1, col], [row, col + 1], [row, col - 1], [row - 1, col], [row + 2, col], [row, col + 2], [row, col - 2],
         [row - 2, col]]
    elif indx == 3:
        return [[row + 1, col + 2], [row + 1, col - 2], [row + 2, col - 1], [row + 2, col + 1], [row - 1, col + 2],
         [row - 1, col - 2], [row - 2, col + 1], [row - 2, col - 1]]

    return neighborhoods[indx]


def breed(mother,father):
    child = [[0 for i in range(8)] for i in range(8)]
    child.append(gen)
    for i in range(4):
        child.append(0)


    for i in range(8):
        for j in range(8):


            if isinstance(child[i],int):
                break


            if random.randint(0,1) == 0:
                child[i][j] = mother[i][j]
            else:
                child[i][j] = father[i][j]

            if random.randint(0,100) < 6:
                child[i][j] = random.randint(0,1)

    return child


def initialize(count):
    global backupcreatures

    creatureslist = []

    for i in range(count):
        creature = [[random.randint(0,1) for i in range(8)] for j in range(8)]
        for j in range(5):
            creature.append(0)

        creatureslist.append(creature)

    backupcreatures = copy.deepcopy(creatureslist)
    return creatureslist


def nametocreature(name):
    binarystring = ""
    for i in name:
        binaryportion = b64.index(i)
        binaryportion = bin(binaryportion)
        binaryportion = binaryportion[2:]


        while len(binaryportion) != 6:
            binaryportion = "0" + binaryportion
        binarystring = binarystring + binaryportion

    while len(binarystring) > 64:
        binarystring = binarystring[1:]
    creature = []
    while len(binarystring) != 64:
        binarystring = "0" + binarystring

    for i in range(8):
        j = i*8
        creaturepart = []
        for k in range(8):
            creaturepart.append(int(binarystring[j+k]))

        creature.append(creaturepart)

    return creature


def findname(creature):
    creaturename = ""
    binarystring = ""

    for i in range(8):
        for j in range(8):
            binarystring = binarystring + str(creature[i][j])
    binarystring = binarystring[::-1]

    number = 0
    digits = 0
    for char in binarystring:
        if digits == 6:
            creaturename = creaturename + str(b64[number])
            number = 0
            digits = 0

        number = number + (int(char) * 2**digits)
        digits += 1
    if number != 0:
        creaturename = creaturename + str(b64[number])

    creaturename = creaturename[::-1]
    return creaturename


def merge(left,right):

    newlist = copy.deepcopy(left)

    for i in range(8):
        newlist[i].extend(right[i])

    return newlist


def flip(creature):
    newcreature = copy.deepcopy(creature)
    for i in newcreature:
        i = i.reverse()
    return newcreature


def getside(side):
    newlist = copy.deepcopy(grid)
    if side == 0:
        for i in newlist:
            for j in range(8):
                del i[8]

    else:
        for i in newlist:
            for j in range(8):
                del i[0]

    return newlist


def blueify(creature):

    bluecreature = copy.deepcopy(creature)

    for i in bluecreature:
        for j in enumerate(i):
            if j[1] == 1:
                i[j[0]] = 2

    return bluecreature


def raw(creature):
    rawcreature = []
    for i in range(8):
        rawcreature.append(creature[i])

    return rawcreature


def iteration(grid):

    newgrid = [[0 for i in range(16)] for j in range(8)]

    for row in range(16):
        for col in range(8):
            cellcount = [0,0,0,0,0]
            neighbors = getneighbors(row,col,rulestring[3])

            for i in neighbors:
                try:
                    cellvalue = grid[i[1]][i[0]]
                    cellcount[cellvalue] = cellcount[cellvalue] + 1
                except:
                    pass

            if grid[col][row] == 0 and sum(cellcount)-cellcount[0] in rulestring[0]:
                max_value = max(cellcount[1:])

                max_index = cellcount[1:].index(max_value)

                if cellcount[1:].count(max_value) == 1:
                    newgrid[col][row] = max_index+1

                else:
                    if rulestring[2] == 0:
                        newgrid[col][row] = 3

                    else:
                        newgrid[col][row] = 4


            if grid[col][row] != 0 and sum(cellcount)-cellcount[0] in rulestring[1]:
                newgrid[col][row] = grid[col][row]

    return newgrid


def findcreatures(grid):

    vitals = [0,0]

    for i in grid:
        for j in i:
            if j == 1 or j == 4:
                vitals[0] += 1
            if j == 2 or j == 4:
                vitals[1] += 1

    return vitals


def battle(creaturea,creatureb,drawf,wait=0.5):
    global grid

    grid = merge(creaturea,blueify(flip(creatureb)))

    if drawf in [1,2]:
        draw(gamemode)
        pygame.display.flip()




    prevgrid4 = copy.deepcopy(grid)
    prevgrid3 = copy.deepcopy(grid)
    prevgrid2 = copy.deepcopy(grid)
    prevgrid = copy.deepcopy(grid)

    for i in range(500):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            exit()

        time.sleep(wait)

        prevgrid4 = copy.deepcopy(prevgrid3)
        prevgrid3 = copy.deepcopy(prevgrid2)
        prevgrid2 = copy.deepcopy(prevgrid)
        prevgrid = copy.deepcopy(grid)
        grid = iteration(grid)

        if grid in [prevgrid,prevgrid2,prevgrid3,prevgrid4]:
            break

        if drawf == 2:
            draw(gamemode)
            pygame.display.flip()

        vitals = findcreatures(grid)


        if vitals[0] == 0 and vitals[1] != 0:
            return [2,vitals]
        elif vitals[0] != 0 and vitals[1] == 0:
            return [1,vitals]
        elif vitals == [0,0]:
            return [0,vitals]

    return [0,vitals]


def generation(drawf):
    global grid,creatures,gen,gridcreatures,backupcreatures,archgen

    creatures = copy.deepcopy(backupcreatures)
    draw(gamemode)
    pygame.display.flip()
    archgen = gen

    for i in range(50):
        creatures[i][9] = 0
        creatures[i][10] = 0

    for i in range(50):
        for j in range(i+1,50):

            print("Battling Creatures", i, "and", j)

            gridcreatures = [findname(creatures[i]),findname(creatures[j])]
            results = battle(raw(creatures[i]),raw(creatures[j]),drawf,0)

            if results[0] == 1:
                creatures[i][9] += 1
                creatures[i][11] += 1

            elif results[0] == 2:
                creatures[j][9] += 1
                creatures[j][11] += 1

            elif results[0] == 0 and results[1] == [0,0]:
                creatures[i][9] += 0.5
                creatures[i][11] += 0.5
                creatures[j][9] += 0.5
                creatures[j][11] += 0.5

            creatures[i][10] += results[1][0]
            creatures[i][12] += results[1][0]
            creatures[j][10] += results[1][1]
            creatures[j][12] += results[1][1]



    creatures = sorted(creatures, key=operator.itemgetter(9,10))


    archive.append(creatures)

    for i in range(50):

        if random.randint(0,100) <= 2*i:
            creatures[i].append(1)
        else:
            creatures[i].append(0)

    creatures = [item for item in creatures if item[13] == 1]

    for i in creatures:
        del i[13]

    gen += 1
    archgen += 1

    length = len(creatures)
    while len(creatures) != 50:
        i,j = random.randint(1,length**2),random.randint(1,length**2)
        i,j = int(math.sqrt(i))-1,int(math.sqrt(j))-1
        print("Breeding Creatures", str(i) + "/" + str(length), "and", str(j) + "/" + str(length))
        creatures.append(breed(creatures[i],creatures[j]))

    print(len(creatures))
    grid = [[0 for i in range(16)]for i in range(8)]
    gridcreatures = ["No Creature","No Creature"]
    backupcreatures = copy.deepcopy(creatures)


def battleall(creature):

    print("Battling", creature)

    for i in range(creature+1, 50):
        fastbattle(creature, i)


    print("Done Battling", creature)


def fastbattle(creaturea, creatureb):
    global creatures

    grid = merge(raw(creatures[creaturea]), blueify(flip(raw(creatures[creatureb]))))

    prevgrid4 = grid[:]
    prevgrid3 = grid[:]
    prevgrid2 = grid[:]
    prevgrid = grid[:]

    for i in range(500):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            exit()

        prevgrid4 = prevgrid3[:]
        prevgrid3 = prevgrid2[:]
        prevgrid2 = prevgrid[:]
        prevgrid = grid[:]

        grid = iteration(grid)


        if grid in [prevgrid, prevgrid2, prevgrid3, prevgrid4]:
            break


        vitals = findcreatures(grid)

        if vitals[0] == 0 and vitals[1] != 0:
            creatures[creatureb][9] += 1
            creatures[creatureb][11] += 1
            break
        elif vitals[0] != 0 and vitals[1] == 0:
            creatures[creaturea][9] += 1
            creatures[creaturea][11] += 1
            break
        elif vitals == [0, 0]:
            creatures[creaturea][9] += 0.5
            creatures[creaturea][11] += 0.5
            creatures[creatureb][9] += 0.5
            creatures[creatureb][11] += 0.5
            break

    creatures[creaturea][10] += vitals[0]
    creatures[creaturea][12] += vitals[0]
    creatures[creatureb][10] += vitals[1]
    creatures[creatureb][12] += vitals[1]
    return


def asapgeneration():
    global grid, creatures, gen, gridcreatures, backupcreatures, archgen

    creatures = copy.deepcopy(backupcreatures)
    draw(gamemode)
    archgen = gen
    pygame.display.flip()


    for i in range(50):
        creatures[i][9] = 0
        creatures[i][10] = 0

    threads = [Thread(target=battleall, args=[i]) for i in range(50)]

    for i in threads:
        i.start()

    for t in threads:
        t.join()


    # here ends modification, all below this line is exactly the same as in the original
    creatures = sorted(creatures, key=operator.itemgetter(9, 10))

    archive.append(creatures)


    creatures = [creatures[i] for i in range(50) if random.randint(0,100) <= 2*i]

    '''
    for i in range(50):
        if random.randint(0, 100) <= 2 * i:
            creatures[i].append(1)
        else:
            creatures[i].append(0)

    creatures = [item for item in creatures if item[13] == 1]

    creatures = [i[:-1] for i in creatures]
    '''

    gen += 1
    archgen += 1

    length = len(creatures)
    while len(creatures) != 50:
        i, j = random.randint(1, length ** 2), random.randint(1, length ** 2)
        i, j = int(math.sqrt(i)) - 1, int(math.sqrt(j)) - 1
        print("Breeding Creatures", str(i) + "/" + str(length), "and", str(j) + "/" + str(length))
        creatures.append(breed(creatures[i], creatures[j]))

    backupcreatures = copy.deepcopy(creatures)


if __name__ == "__main__":
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        if event.type == pygame.KEYUP:
            print("UP", event.key)
            if event.key == 304:
                shift = (shift + 1) % 2

        if event.type == pygame.KEYDOWN:
            key = event.key

            print(key)

            #TODO BETTER SHIFT
            if key == 304:
                shift = (shift+1)%2


            if key == 27:
                grid = [[0 for i in range(16)] for i in range(16)]
                currentlyinputting = 0
                gridcreatures = ["No Creature", "No Creature"]
                inputstring = ""
                rulestring = [[3],[2,3],0,0]

            if currentlyinputting == 0:

                if gamemode == 0 and event.key == pygame.K_SPACE:
                    creatures = initialize(50)
                    gamemode = 1

                if gamemode == 1:
                    if event.key == pygame.K_LCTRL:
                        currentlyinputting = 1

                    if event.key == pygame.K_RCTRL:
                        currentlyinputting = 2

                    if event.key == pygame.K_i:
                        grid = iteration(grid)

                    if event.key == pygame.K_b:
                        battle(nametocreature(gridcreatures[0]),nametocreature(gridcreatures[1]),2)

                    if event.key == pygame.K_a:
                        asapgeneration()

                    if event.key == pygame.K_f:
                        generation(1)

                    if event.key == pygame.K_s:
                        generation(2)

                    if event.key == pygame.K_LEFT:
                        if archgen != 0:
                            archgen = archgen - 1
                            creatures = copy.deepcopy(archive[archgen])

                    if event.key == pygame.K_RIGHT:
                        if archgen != gen:
                            archgen = archgen + 1
                            if archgen == gen:
                                creatures = copy.deepcopy(backupcreatures)
                            else:
                                creatures = copy.deepcopy(archive[archgen])

                    if event.key == pygame.K_LALT:
                        currentlyinputting = 3

                    if event.key == pygame.K_w:
                        currentlyinputting = 4

                    if key in range(48,58):
                        with open(str("Save" + str(key-48) + ".txt"),"w") as savefile:
                            json.dump([gen,archive,backupcreatures,rulestring],savefile)
                    if key in range(282,291):
                        with open(str("Save" + str(key - 281) + ".txt"), "r") as savefile:
                            jsonlist = json.loads(savefile.read())
                            gen = jsonlist[0]
                            archgen = jsonlist[0]
                            archive = jsonlist[1]
                            backupcreatures = jsonlist[2]
                            creatures = copy.deepcopy(backupcreatures)
                            rulestring = jsonlist[3]
                            print(gen,archive,backupcreatures,rulestring)


                    if event.key == pygame.K_g:
                        creatures = sorted(creatures, key=operator.itemgetter(8, 9, 10))

                    if event.key == pygame.K_r:
                        creatures = sorted(creatures, key=operator.itemgetter(9, 10))

                    if event.key == pygame.K_p:
                        creatures = sorted(creatures, key=operator.itemgetter(10, 9))

                    if event.key == pygame.K_o:
                        creatures = sorted(creatures, key=operator.itemgetter(11, 12))

                    if event.key == pygame.K_u:
                        creatures = sorted(creatures, key=operator.itemgetter(12, 11))

            elif currentlyinputting == 1:
                if key == 8:
                    inputstring = inputstring[0:-1]

                elif key == 13 and len(inputstring) < 12:
                    grid = merge(nametocreature(inputstring),getside(1))
                    gridcreatures[0] = findname(nametocreature(inputstring))
                    currentlyinputting = 0
                    inputstring = ""


                elif key <= 127 and len(inputstring) < 11 and chr(key) in b64:
                    if key in [45,61]:
                        inputstring = inputstring + chr(key)
                    else:
                        inputstring = inputstring + chr(key+(-32*shift))

            elif currentlyinputting == 2:

                if key == 8:
                    inputstring = inputstring[0:-1]

                elif key == 13 and len(inputstring) < 12:
                    grid = merge(getside(0),blueify(flip(nametocreature(inputstring))))
                    gridcreatures[1] = findname(nametocreature(inputstring))
                    currentlyinputting = 0
                    inputstring = ""



                elif key <= 127 and len(inputstring) < 11 and chr(key) in b64:

                    if key in [45, 61]:

                        inputstring = inputstring + chr(key)

                    else:

                        inputstring = inputstring + chr(key + (-32 * shift))

            elif currentlyinputting == 3:
                if key in range(48, 58):
                    inputstring = inputstring + str(key-48)
                if key == 47:
                    inputstring = inputstring + "/"
                if key == 8:
                    inputstring = inputstring[0:-1]
                if key == 13:
                    rulestringl = inputstring.split("/")
                    print(rulestringl)
                    newstring = [[],[],0,0]
                    for i in rulestringl[0]:
                        newstring[0].append(int(i))
                    for i in rulestringl[1]:
                        newstring[1].append(int(i))
                    if rulestringl[2] in ['0','1']:
                            newstring[2] = int(rulestringl[2])
                    if rulestringl[3] in ["0","1","2","3"]:
                            newstring[3] = int(rulestringl[3])

                    newstring[0] = sorted(set(newstring[0]))
                    newstring[1] = sorted(set(newstring[1]))
                    print(newstring)
                    now = datetime.datetime.now()
                    now = str(now)
                    now = now.replace(":",";")
                    if archive != []:
                        with open(str("Autosave " + now + ".txt"), "w") as savefile:
                            json.dump([gen, archive, backupcreatures, rulestring], savefile)

                    rulestring = newstring[:]
                    inputstring = ""
                    currentlyinputting = 0

            elif currentlyinputting == 4:
                if key in range(48, 58) and int(inputstring + str(key-48)) <= gen:
                    inputstring = inputstring + str(key - 48)


                if key == 8:
                    inputstring = inputstring[0:-1]

                if key == 13:
                    archgen = int(inputstring)
                    if archgen == gen:
                        creatures = copy.deepcopy(backupcreatures)
                    else:
                        creatures = copy.deepcopy(archive[archgen])
                    currentlyinputting = 0
                    inputstring = ""

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if gamemode == 1:
                if pos[0] <= 800 and pos[1] >= 8*800//16 + 65:
                    #(170*i/10,(65 + 8 * squaresize) + (30*j))
                    if event.button == 1:
                        ones = (pos[1] - (65 + 8 * 800//16))//30
                        tens = pos[0]//170
                        if 10*tens + ones >= 0:
                            creaturetoview = raw(copy.deepcopy(creatures[(10*tens + ones)]))

                            nonraw = copy.deepcopy(creatures[(10*tens + ones)])

                            stats = [findname(nonraw),nonraw[8],nonraw[9],nonraw[10],nonraw[11],nonraw[12]]

                            gridcreatures[0] = findname(creaturetoview)
                            grid = merge(creaturetoview,getside(1))

                    else:
                        ones = (pos[1] - (65 + 8 * 800//16))//30
                        tens = pos[0]//170
                        if 10*tens + ones >= 0:
                            creaturetoview = raw(copy.deepcopy(creatures[(10*tens + ones)]))

                            nonraw = copy.deepcopy(creatures[(10 * tens + ones)])

                            stats2 = [findname(nonraw), nonraw[8], nonraw[9], nonraw[10], nonraw[11], nonraw[12]]


                            gridcreatures[1] = findname(creaturetoview)
                            grid = merge(getside(0),blueify(flip(creaturetoview)))

        draw(gamemode)
        pygame.display.flip()