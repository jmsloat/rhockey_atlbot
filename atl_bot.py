from bs4 import BeautifulSoup
import urllib2
import json

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

    def retreieveGames(self):
	response = urllib2.urlopen(self.url)
	games = json.load(response)
	return games['scores']

    def getScorers(self):
	gameurl = 'http://www.hockey-reference.com/boxscores/201502040EDM.html'
	gamedoc = urllib2.urlopen(gameurl)
	soup = BeautifulSoup(gamedoc)

	scoringTable = soup.find('table', id='scoring')
        import pdb; pdb.Pdb().set_trace()
        print scoringTable
        #dict of period, K is period num, V is list of goal scorers text... right?
        goalList = []
        curPeriod = 1
        trs = scoringTable.find_all('tr')
        for record in trs:
            print record
            if record.th and 'Period' in record.th.text:
                curPeriod = 2
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
    games = bot.retreieveGames()
    bot.getScorers()

if __name__=='__main__':
    main()
