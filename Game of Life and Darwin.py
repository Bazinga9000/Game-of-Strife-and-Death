import pygame,random,copy,time,operator,math,json
pygame.init()
surface = pygame.display.set_mode((1300,760))

grid = [[0 for i in range(16)] for j in range(8)]
gridtocol = {0 : (255,255,255), 1 : (204,0,0), 2 : (0,0,204)}
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

b64 = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
       'S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
       'u','v','w','x','y','z','-','=']

gridcreatures = ["No Creature","No Creature"]

stats = ["No Creature","NaN","NaN","NaN","NaN"]
stats2 = ["No Creature","NaN","NaN","NaN","NaN"]


def draw(gamemode):
    surface.fill((204, 204, 204))

    squaresize = 800 // 16


    if gamemode == 0:
        title = bigfont.render("Game of Strife and Death",True,(0,0,0))
        text = font.render("It appears you don't have any creatures yet! Press SPACE to generate 50 random creatures!",True,(0,0,0))
        surface.blit(title,(350,50))
        surface.blit(text,(75,300))

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
        surface.blit(currentlyviewing,(10,10))

        if currentlyinputting != 0:
            if currentlyinputting == 1:
                inputtext = font.render(str("Inputting Custom Red Creature " + inputstring),True,(204,0,0))
            if currentlyinputting == 2:
                inputtext = font.render(str("Inputting Custom Blue Creature " + inputstring),True,(0,0,204))
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
                surface.blit(img, (820, 250 + 25 * n))


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


def iteration():
    global grid

    newgrid = copy.deepcopy(grid)

    for row in range(16):
        for col in range(8):
            cellcount = [0,0,0]
            neighbors = [[row+1,col],
                         [row+1,col+1],
                         [row+1,col-1],
                         [row,col+1],
                         [row,col-1],
                         [row-1,col-1],
                         [row-1,col],
                         [row-1,col+1]]



            for i in neighbors:
                if i[1] not in [-1,8] and i[0] not in [-1,16]:
                    cellvalue = grid[i[1]][i[0]]
                    cellcount[cellvalue] = cellcount[cellvalue] + 1

            if newgrid[col][row] == 0 and cellcount[1] + cellcount[2] == 3:
                if cellcount[1] > cellcount[2]:
                    newgrid[col][row] = 1
                else:
                    newgrid[col][row] = 2
            if newgrid[col][row] != 0 and cellcount[1] + cellcount[2] not in [2,3]:
                newgrid[col][row] = 0

    return newgrid


def findcreatures():

    vitals = [0,0]

    for i in grid:
        for j in i:
            if j == 1:
                vitals[0] += 1
            if j == 2:
                vitals[1] += 1

    return vitals


def battle(creaturea,creatureb,drawf,wait=0.5):
    global grid

    grid = merge(creaturea,blueify(flip(creatureb)))

    if drawf in [1,2]:
        draw(gamemode)
        pygame.display.flip()
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            exit()

    prevgrid4 = copy.deepcopy(grid)
    prevgrid3 = copy.deepcopy(grid)
    prevgrid2 = copy.deepcopy(grid)
    prevgrid = copy.deepcopy(grid)

    for i in range(500):
        time.sleep(wait)

        prevgrid4 = copy.deepcopy(prevgrid3)
        prevgrid3 = copy.deepcopy(prevgrid2)
        prevgrid2 = copy.deepcopy(prevgrid)
        prevgrid = copy.deepcopy(grid)
        grid = iteration()

        if grid in [prevgrid,prevgrid2,prevgrid3,prevgrid4]:
            break

        if drawf == 2:
            draw(gamemode)
            pygame.display.flip()

        pygame.event.get()
        vitals = findcreatures()


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
        print("Breeding Creatures", i, "and", j)
        creatures.append(breed(creatures[i],creatures[j]))

    grid = [[0 for i in range(8)]for i in range(8)]
    gridcreatures = ["No Creature","No Creature"]
    backupcreatures = copy.deepcopy(creatures)



while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    if event.type == pygame.KEYDOWN:
        key = event.key

        print(key)

        #TODO BETTER SHIFT
        if key == 304:
            mod = -((mod + 32)%64)


        if key == 27:
            grid = [[0 for i in range(16)] for i in range(16)]
            currentlyinputting = 0
            gridcreatures = ["No Creature", "No Creature"]
            inputstring = ""

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
                    grid = iteration()

                if event.key == pygame.K_b:
                    battle(nametocreature(gridcreatures[0]),nametocreature(gridcreatures[1]),2)

                if event.key == pygame.K_a:
                    generation(0)

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

                if key in range(48,57):
                    with open(str("Save" + str(key-48) + ".txt"),"w") as savefile:
                        json.dump([gen,archive,backupcreatures],savefile)
                if key in range(282,290):
                    with open(str("Save" + str(key - 281) + ".txt"), "r") as savefile:
                        jsonlist = json.loads(savefile.read())
                        gen = jsonlist[0]
                        archgen = jsonlist[0]
                        archive = jsonlist[1]
                        backupcreatures = jsonlist[2]
                        creatures = copy.deepcopy(backupcreatures)
                        print(gen,archive,backupcreatures)

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
                    mod = 0

                inputstring = inputstring + chr(key+mod)

        elif currentlyinputting == 2:

            if key == 8:
                inputstring = inputstring[0:-1]

            elif key == 13 and len(inputstring) < 12:
                grid = merge(getside(0),blueify(flip(nametocreature(inputstring))))
                gridcreatures[1] = findname(nametocreature(inputstring))
                currentlyinputting = 0
                inputstring = ""


            elif key <= 127 and len(inputstring) < 11 and chr(key) in b64:
                if key in [45,61]:
                    mod = 0

                inputstring = inputstring + chr(key+mod)



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