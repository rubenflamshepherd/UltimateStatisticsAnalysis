def spacer (string, length):
    ''' get a string and return a string that is length spaces long and 
    added spaces to make up the difference are empty spaces ' '
    '''
    counter = length - len(string)

    assert counter > 0, 'ERROR: spacer() cannot pad string'

    while counter > 0:
        string += ' '
        counter -= 1

    return string

class Player:
    
    def __init__ (self, name, num, sex):
        self.name = name
        self.num = num
        self.sex = sex
        self.acr = name[0:3]
        self.catches_attempted = 0
        self.catches_completed = 0 # _c suffic stands for 'completed'
        self.catching_per = 0
        self.throws_attempted = 0
        self.throws_completed = 0
        self.throwing_per = 0
        self.points_played = 0
        self.points = 0
        self.primary_assists = 0
        self.secondary_assists = 0
        self.plus_minus = 0
        self.flow = 0
        
    def __str__ (self):
        name = spacer (self.name, 10)
        num = spacer (self.num, 5)
        sex = spacer (self.sex, 5)    
        acr = spacer (self.acr, 5)
        points_played = spacer (str(self.points_played), 5)
        throws = spacer(str(self.throws_attempted), 5)
        throws_c = spacer(str(self.throws_completed), 5)
        catches = spacer(str(self.catches_attempted), 5)
        catches_c = spacer(str(self.catches_completed), 5)
        flow = spacer(str(self.flow), 5)
        points = spacer(str(self.points), 5)
        p_assists = spacer(str(self.primary_assists), 5)
        s_assists = spacer(str(self.secondary_assists), 5)
        plus_minus = spacer(str(self.plus_minus), 5)
        
        line = name + num + sex + acr + points_played + throws + throws_c + \
            catches + catches_c + flow + points + p_assists + \
            s_assists + plus_minus
        
        return line
        