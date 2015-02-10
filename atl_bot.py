from bs4 import BeautifulSoup
import urllib2
import json
import time

class Goal(object):
    """Data Structures for goals parsed from hockey-reference.com"""
    def __init__(self, period, goaltime, team, scorers):
        self.time = goaltime
        self.period = period
        self.team = team
        self.scorers = scorers.strip()

    def __repr__(self):
        team = '{} Goal\n'.format(self.team)
        timeofgoal = '{} of Period {}\n'.format(self.time, self.period)
        return '{}{}{}\n'.format(team, timeofgoal, self.scorers)

class ATLBot(object):

    def __init__(self):
	self.apikey = open('api.key', 'r').read().strip()
        self.url = 'https://api.hockeystreams.com/Scores?key={}&event=nhl'.format(self.apikey)

    def start(self):
        prevScores = {} # Dict of previous scores - don't want to ask site for scorers unless
                        # the score has changed
        while True:
            import pdb; pdb.Pdb().set_trace()
            games = self.getGames()
            
            #only get score if started
            for game in games:
                print game
                
                started = True if not str(game['isPlaying']) == '0' else False
                homeAbbrev = str(game['shortHomeTeam'])
                homeScore = int(game['homeScore'])
                awayScore = int(game['awayScore']) 

                if started and not (homeScore, awayScore) == prevScores.get(homeAbbrev,(0,0)):
                    self.getScorers(homeAbbrev)
                else:
                    pass

                prevScores[homeAbbrev] = (homeScore, awayScore)


            time.sleep(60)


    def getGames(self):
	response = urllib2.urlopen(self.url)
	games = json.load(response)
	return games['scores']

    def getScorers(self, homeTeam):
        
        # build URL + request html from it
        today = time.strftime('%Y%m%d')
	gameurl = 'http://www.hockey-reference.com/boxscores/{}0{}.html'.format(today, homeTeam)
	gamedoc = urllib2.urlopen(gameurl)
	soup = BeautifulSoup(gamedoc)

        # Parse html
	scoringTable = soup.find('table', id='scoring')
        goalList = []
        curPeriod = 1

        # get all table records and goal data from inside them
        trs = scoringTable.find_all('tr')
        for record in trs:

            #determine what period in quite possibly the ugliest possible manner
            if record.th and 'Period' in record.th.text:
                if '1st' in record.th.text:
                    curPeriod = 1
                elif '2nd' in record.th.text:
                    curPeriod = 2
                elif '3rd' in record.th.text:
                    curPeriod = 3
                else:
                    curPeriod = 'OT'
            else:
                fields = record.find_all('td') # will get all table data
                # will always have three values in this list:
                #  1: Time of Goal
                #  2: Team Abbreviation of who scored the goal
                #  3: The Goal-Scorer and his assistants
                time = fields[0].text
                team = fields[1].text
                scorers = fields[2].text
                g = Goal(curPeriod, time, team, scorers)
                goalList.append(g)
        
        for goal in goalList:
            print goal

def main():
    bot = ATLBot()
    bot.start()

if __name__=='__main__':
    main()
