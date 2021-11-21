# you can only pack a bag with 'max_weight' units worth of stuff
# pack the most of the 'love' unit possible while staying under or at 'max_weight' weight units

from random import randint
import os


### NOTICE: Put path of 'iteam_tags variable 'path' ###
path = (os.path.dirname( os.path.realpath(__file__)) +'\iteam_tags.txt')

max_weight = 200

## get/create iteams and tags
def get_iteams():
    iteams = []
    with open(path, 'r') as fin:
        file = fin.readlines()

    for line in file:
        for letter in range(len(line)):
            if line[letter] == ' ':
                iteams.append(line[:letter])
                break

    return iteams

def get_tags(iteams):
    tag = []
    with open(path, 'r') as fin:
        file = fin.readlines()

    for line in file:
        for letter in range(len(line)):

            if line[letter] == '[':
                 chunk = line[letter:-1]

                 for letter in range(len(chunk)):
                    if chunk[letter] == ' ':
                        love = int(chunk[1:letter-1])
                        weight = int(chunk[letter : -1])   

                        tag.append([love,weight])
                        break 

    tags = dict(zip(iteams, tag))
    return tags

def generate_iteams():
    tag = []
    iteams = get_iteams()
    
    with open(path, 'w') as fin:
        for iteam in iteams:

            love = randint(0,100)
            weight = randint(0,100)

            fin.write(f'{iteam} [{love}, {weight}]\n')
            tag.append([love, weight])
    

    tags = dict(zip(iteams, tag))
    return iteams, tags

## brute and neccesities 
def get_all(num):
    run = True
    x = -1

    while run:
        x += 1
        poss = f'{x:0{num}b}'
        list=[]
        for digit in poss:
            list.append(int(digit))
        yield list
        if poss == '1'* num:
            run = False

def backpack_values(iteams,tags,pack):
    love_f = 0
    weight_f = 0
    
    for present in range (len(pack)):
        if pack[present] == 1:
            
            love = tags[iteams[present]][0]
            weight = tags[iteams[present]][1]

            love_f += love
            weight_f += weight
            if weight_f > max_weight:
                return 0, 0
    return love_f, weight_f

### brute forces the correct answer by finding all possabilities and keeping the best one ###

def brute(iteams, tags, alt=False, poss=False):

    love_best = 0
    weight_best = 0
    best_pack = []
    
    if poss == False:
        poss_iteams = int(input('how many iteams would you like to check with >> '))
        poss = get_all(poss_iteams)

    x = 0
    for pack in poss:
        love_f, weight_f = backpack_values(iteams,tags,pack)    
        
        if love_f >= love_best:

            love_best = love_f
            weight_best = weight_f

            #######
            if alt:
                best_pack.append(pack)

                if len(best_pack) > 4:
                    best_pack.pop(0)    
            ######

            else:
                best_pack = pack

        if x == 10 and alt and poss_iteams > 10:
            break

        x += 1

    return love_best, weight_best, best_pack

# evole and neccesities
def cross_over(pos):  

    #create vetiations of existing pos using top 3 beginings and end
    for x in range(3):
        begining = pos[x][0:int(len(pos[0])/2)]     

        if x < 3:
            x = 0 

        end = pos[x][int(len(pos[0])/2):len(pos[0])]
        for poject in end:
            begining.append(poject)
        pos.insert(0,begining)

        random_list=[]
        for iteam in range(len(pos[-1])):
            if randint(0,3) == 1:
                random_list.append(randint(0,1))
            else:
                random_list.append(pos[-1][iteam])
        
        pos.insert(0, random_list)

    return pos

###Use Genetic algorithum to find best possability ###

def evole(iteams, tags):
    # use previous def to cross-over iteam true/false to get new versions
    #get amoount of possabiliys and run throught cross_over to get different versions
    _, _, pos = brute(iteams, tags, alt=True)
    backpack = cross_over(pos)  
    previous = [backpack[0],0]

    # get value of crossed over versions
    run = True    
    while run:
        _, _, pos = brute(iteams, tags, alt=True, poss=backpack)
        backpack = cross_over(pos)
        
        best = 0
        new_pack=[]
        for pack in backpack:
            value, _ = backpack_values(iteams, tags, pack)
            if value > best:
                value = best
                new_pack.append(pack)
            else:
                new_pack.insert(0,pack)
        
        if new_pack[-1] == previous[0]:
            previous[-1] +=1

            amount = 10 **((len(backpack[0])-2)/10)
            if amount < 10000:
                amount = 10000
            if previous[-1] == amount:
                run = False
        else:
            previous[0] = new_pack[-1]
            previous[-1] = 0

    #send back best with addr
    love, weight, pos = brute(iteams, tags, poss=new_pack)
    return love, weight, pos
     

# print the results
def results(love, weight, pos):
    print('')
    print(f'Most love was {love} at {weight} units weight')
    print(pos)

        
def main():
    create = input('(g)enerate new tags or (u)se current>> ').lower()
    if create == 'u':
        iteams = get_iteams()
        tags = get_tags(iteams)
    else:
        iteams, tags = generate_iteams()


    method = input('use (b)rute or (e)volution>> ').lower()
    if method == 'b':
        love, weight, pos = brute(iteams, tags)
        results(love, weight, pos)

    else:
        love, weight, pos = evole(iteams, tags)
        results(love, weight, pos)

if __name__ == '__main__':
    main()       
