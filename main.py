import random,time,json

# dev tools
dev = {'tosses':True,'prison':True,'buys':True, 'rents':True}
# slow play
slow_play = True
# count of bots
bots = 4

data = {}
running = True
has_buyt = []

# make bot data
for i in range(bots):
    data[str(i+1)] = {'pos':1, 'money':1500, 'properties':[],'streets':[], 'prison':False, 'turns_in_prison':1, 'playing':True}

def turn(runningBot):
    # make turns
    if not runningBot == bots:
        runningBot += 1
    else:
        runningBot = 1
    return runningBot

def get_toss():
    # get a random toss
    toss = [random.randint(1,6),random.randint(1,6)]
    return toss

def prison(runningBot,toss):
    # Looks if bot can leave jail
    if data[str(runningBot)]['turns_in_prison'] == 3:
        data[str(runningBot)]['prison'] = False
        data[str(runningBot)]['turns_in_prison'] = 1
        if dev['prison']:
            print('Bot{} has gone out of prison when he hit 3 turns in prison'.format(runningBot))
    elif toss[0] == toss[1]:
        data[str(runningBot)]['prison'] = False
        data[str(runningBot)]['turns_in_prison'] = 1
        if dev['prison']:
            print('Bot{} has gone out of prison by doubles'.format(runningBot))                                  
    else:
        data[str(runningBot)]['turns_in_prison'] += 1
        return True

def get_pos_data(pos):
    # Get data from data.json
    monopolyData = json.loads(open('./data.json').read())
    for i in monopolyData['properties']:
        gotPosistion = True
        try:
            z = i['posistion']
            z = i['price']
            z = i['group']
            z = i['rent']
        except:
            gotPosistion = False
        if gotPosistion:
            if i['posistion'] == pos and not i['group'] == 'Special':
                return i
        else:
            return False


        

def want_to_buy(pos,money, need,runningBot):
    # looks if bot want to make a purchase(work in progress)
    # All but Railroads and Untilities


    propaty = get_pos_data(pos)
    if not propaty == False:
        price = propaty['price']
        saves = need*10
        val = True
        for i in has_buyt:
            if pos == i:
                val = False
        if money-price > saves:
            if val:
                has_buyt.append(pos)
                data[str(runningBot)]['money'] = data[str(runningBot)]['money'] - price
                data[str(runningBot)]['properties'].append(pos)
                if dev['buys']:
                    print('Bot{} has buyt {}({}). Price is {} money now {}'.format(runningBot,propaty['name'],pos,price,data[str(runningBot)]['money'])) 
                return True
            else:
                # Check if need to pay
                for i in data:
                    for s in data[i]['properties']:
                        if s == pos:
                            data[str(runningBot)]['money'] = data[str(runningBot)]['money'] - propaty['rent']
                            data[i]['money'] += propaty['rent']
                            if dev['rents']:
                                print('Bot{} payed {} to bot{} balances are {} and {}'.format(runningBot,propaty['rent'],i,data[str(runningBot)]['money'],data[i]['money']))


                return False
        else:
            return False
    else:
        return False

def look_need_prison(toss,runningBot,doubleVal,double):
    # looks if bot need to be in prison
    if doubleVal == 3:
        data[str(runningBot)]['prison'] = True
        if dev['prison']:
            print('Put bot{} in prison because he trowd double 3 times in a row.'.format(runningBot))
        doubleVal = 0
        double = False
    if data[str(runningBot)]['pos'] == 30:
        data[str(runningBot)]['prison'] = True
        data[str(runningBot)]['pos'] = 10
        doubleVal = 0
        double = False
    return doubleVal, double


def main():
    # makes main variables
    turns = 0
    runningBot = 1
    double = False
    doubleVal =  0


    while running:
        # look sif bot is still playing 
        if data[str(runningBot)]['playing'] == True:
            turns += 1
            # Get toss
            toss = get_toss() 
            # Run the prison program
            if data[str(runningBot)]['prison'] == True:
                prison(runningBot, toss)
                runningBot = turn(runningBot)
            else:
                data[str(runningBot)]['pos'] += toss[0]+toss[1]
                # look if over start
                if data[str(runningBot)]['pos'] >= 41:
                    data[str(runningBot)]['pos'] = data[str(runningBot)]['pos'] - 41
                    data[str(runningBot)]['money'] += 200
                    # print out the turn and toss
                    if dev['tosses']:
                        print('Bot{0} has tossed {1} his new posistion is {2}'.format(runningBot,toss,data[str(runningBot)]['pos']))
                        print('Bot{} has gone over start and recieved 200 dollars. New balance is {}'.format(runningBot,data[str(runningBot)]['money']))
                else:
                    # print out the turn and toss
                    if dev['tosses']:
                        print('Bot{0} has tossed {1} his new posistion is {2}'.format(runningBot,toss,data[str(runningBot)]['pos']))
                
                # looks if double
                if toss[0] == toss[1]:
                    double = True
                    doubleVal += 1
                else:
                    double = False
                    doubleVal = 0
                # look if need to be in prison
                look_need_prison(toss,runningBot,doubleVal,double)
            # runs the purchase function
            want_to_buy(data[str(runningBot)]['pos'],data[str(runningBot)]['money'],turns//bots,runningBot)
            
            # If not double just go truh                
            if double == False:
                runningBot = turn(runningBot)
        else:
            # calls the turn function
            runningBot = turn(runningBot)
        # slow play
        if slow_play:
            time.sleep(1)
# runs the program
if __name__=='__main__':
    main()


