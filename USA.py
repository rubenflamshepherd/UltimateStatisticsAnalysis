import Player
from operator import itemgetter, attrgetter
from xlrd import *
from xlwt import *

def spacer (string, length):
    ''' get a string and return a string that is length spaces long and 
    added spaces to make up the difference are empty spaces ' '
    '''
    counter = length - len (string)

    while counter > 0:
        string += ' '
        counter -= 1

    return string

def header ():
    '''
    Utility class used for printing column headers in console
    '''
    name = spacer('Name',10)
    num = spacer('Num', 5)
    sex = spacer('Sex', 5)
    pp = spacer('Points', 5)
    t = spacer('Throws', 5)
    tc = spacer('Throws', 5)
    c = spacer('Catches', 5)
    cc = spacer('Catches',5)
    p = spacer('Points',5)
    pa = spacer('Prim.',5)
    sa = spacer('Sec.',5)
    p_m = spacer('+/-',5)
    
    
    line = name + num + sex + pp + t + tc + c + cc + p + pa + sa + p_m
    
    return line

def create_player_objs(roster_file):
    player_list = []
    
    for line in roster_file:
        info = line.split ()
        new_player = Player.Player (name=info [0], num=info [1], sex=info [2])
        player_list.append (new_player)
       
    return player_list

def grab_possession(game_reader):
    '''
    Grab a sequence of players through which a possession has progressed
    '''
    players_on = game_reader.readline ().split ('-')
    # clean the new line tag that pops up
    for x in range (0, len (players_on)):
        players_on[x] = players_on [x].strip ('\n')   
        
    return players_on

def add_point_assist(game_roster, possesion):
    '''
    Assigning points and assists if the current possession ends in a point 
    scored
    '''
    secondary_assist = None

    if possesion[len(possesion) - 1] == 'p':
        primary_assist = possesion[len(possesion) - 3]
        point_getter = possesion[len(possesion) - 2]
        if len(possesion) > 3:
            secondary_assist = possesion[len(possesion) - 4]
        for player in game_roster:
            if player.acr == point_getter:
                player.points += 1
            if player.acr == primary_assist:
                player.primary_assists += 1
            if player.acr == secondary_assist:
                player.secondary_assists += 1
       
def add_shift (game_roster, players_on):
    for player_acr in players_on:
        for roster_player in game_roster:
            if player_acr == roster_player.acr:
                roster_player.points_played += 1

def add_catches (game_roster, players_on):
    '''
    Assigning catches_attempted and catches_completed statistics to player
    objects
    '''
    if players_on[len(players_on) - 1] != 'p':
        for x in range(1, len (players_on)):
            for player in game_roster:
                if players_on[x] == player.acr:
                    player.catches_attempted += 1
                    # Last player in possession drops disc
                    if x != (len (players_on) - 1):
                        player.catches_completed += 1
    else:
        for x in range (1, len (players_on)):
            for player in game_roster:
                # Last player in possession scores point (catches disc)
                if players_on[x] == player.acr:
                    player.catches_attempted += 1
                    player.catches_completed += 1        
                    
def add_throws (game_roster, possesion):
    '''
    Assigning throws_attempted and throws_completed statistics to player
    objects
    '''
    if possesion[len(possesion) - 1] == 'p' or possesion[len(possesion) - 1] == 'g':        
        for x in range (0, len (possesion) - 2):
            for player in game_roster:
                if possesion [x] == player.acr:
                    player.throws_attempted += 1
                    player.throws_completed += 1        
    else:
        for x in range (0, len(possesion)-1):
            for player in game_roster:
                if possesion [x] == player.acr:
                    player.throws_attempted += 1
                    # Last thrower throws away the disc (not completed)
                    if x != (len(possesion) - 2):
                        player.throws_completed += 1
   
                           
def add_plus_minus (game_roster, players_on, possesion):
    '''
    Assigning plus_minus statistics to player objects
    '''
    if possesion[len(possesion) -1] == 'p':
        for x in range (0, len (players_on)):
            for player in game_roster:
                if players_on[x] == player.acr:
                    player.plus_minus += 1
    elif possesion[0] == 'd':
        for x in range (0, len (players_on)):
            for player in game_roster:
                if players_on [x] == player.acr:
                    player.plus_minus -= 1
                    
def write_data (game_roster, output):
    '''
    Write statics from each player object in game_roster to Excel
    output is the file name (string)
    '''
    stats_headers = \
        ['Name', 'Num', 'Throws Att.', 'Throws Comp.', 'Throwing %',\
        'Catches Att.', 'Catches Comp.', 'Catching %', 'Flow', 'Points',\
        'Prim. Ass.', 'Sec. Ass.', '+/-']
    
    for player in game_roster:
        if player.catches_attempted > 0:
            player.catching_per = \
                (float(player.catches_completed)/ \
                float(player.catches_attempted)) * 100
        if player.throws_attempted > 0:
            player.throwing_per = \
                (float (player.throws_completed)/ \
                float(player.throws_attempted)) * 100
        player.flow = player.throwing_per * player.catching_per/100
        
    game_roster_sorted = sorted(
        game_roster, key=attrgetter('flow', 'catching_per'), reverse=True)    
    output_file = Workbook ()    
    analysis_sheet = output_file.add_sheet(
        'Created Statistics - PYTHON', cell_overwrite_ok=True)
    
    for col in range (len (stats_headers)):
        analysis_sheet.write (0, col, stats_headers[col])    
    for x in range (0, len(game_roster)):
            analysis_sheet.write(x + 1, 0, game_roster_sorted[x].name)
            analysis_sheet.write(x + 1, 1, game_roster_sorted[x].num)
            analysis_sheet.write(x + 1, 2, game_roster_sorted[x].throws_attempted)
            analysis_sheet.write(x + 1, 3, game_roster_sorted[x].throws_completed)
            analysis_sheet.write(x + 1, 4, game_roster_sorted[x].throwing_per)
            analysis_sheet.write(x + 1, 5, game_roster_sorted[x].catches_attempted)
            analysis_sheet.write(x + 1, 6, game_roster_sorted[x].catches_completed)
            analysis_sheet.write(x + 1, 7, game_roster_sorted[x].catching_per)
            analysis_sheet.write(x + 1, 8, game_roster_sorted[x].flow)
            analysis_sheet.write(x + 1, 9, game_roster_sorted[x].points)
            analysis_sheet.write(x + 1, 10, game_roster_sorted[x].primary_assists)
            analysis_sheet.write(x + 1, 11, game_roster_sorted[x].secondary_assists)
            analysis_sheet.write(x + 1, 12, game_roster_sorted[x].plus_minus)
            
    output_file.save(output)
    
def grab_data(roster, game):
    '''
    roster and game are open rewritable text files. Grab files and create player
    objects while adding up the statistics they collect over the game
    '''
    game_roster = create_player_objs(roster)   
    players_on = grab_possession(game) # 1st line of possession is players on
        
    while players_on[0] != 'g': # Signifies end of game   
        
        add_shift(game_roster, players_on)        
        # Add up catching and throwing
        possesion = ['start','start'] # Initialize variable, don't think I need this
                
        while possesion [0] != '#': # Signifies end of possession
            possesion = grab_possession(game)
            add_throws(game_roster, possesion)
            add_catches(game_roster, possesion)
            add_point_assist(game_roster, possesion)
            add_plus_minus(game_roster, players_on, possesion)
            print possesion
            
        players_on = grab_possession (game)

    for item in game_roster:
        print item
    return game_roster

if __name__ == '__main__':
    game = open ('Example-BGame3.txt', 'r')
    roster = open ('Example-BRoster.txt', 'r')

    header = header()
    print header

    game_roster = grab_data(roster, game)
    write_data(game_roster, output='ExampleOuput-BGame3.xls')   