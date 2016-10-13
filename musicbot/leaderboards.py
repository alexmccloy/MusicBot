import json
import os

"""
Leaderboard json format:
trivia_name <string> : players (player_name, score)[]
"""


class LeaderboardManager:
    def __init__(self, max_score):
        self.leaderboardFile = "trivia/leaderboards.json"
        self.learderboard = None
        self.max_score = max_score

    def load_leaderboard(self):
        #loads leaderboard into memory from file - must be called before leaderboards can be used
        with open(self.leaderboardFile) as json_data:
            self.leaderboard = json.load(json_data)
            json_data.close()

    def save_leaderboard(self):
        if self.leaderboard == None:
            return
        #moves exising leaderboard to leaderboard2.json and then writes leaderboard in current memory to file
        #this will backup the previous leaderboard but keep only 1 backup at a time
        os.rename(self.leaderboardFile, self.leaderboardFile + "_backup")
        newFile = open(self.leaderboardFile, "w")
        newFile.write(json.dumps(self.leaderboard))
        newFile.close()

    def add_game_results(self, triviaName, results):
        #adds game results to leaderboards for a single triviaName(dictionary key). If game exists will update the
        #values, else will create a new entry

        #divide results so that score is independent of max_score
        for i in range(len(results)):
            results[i] = (results[i][0], results[i][1]/self.max_score)
        try:
            oldEntry = self.leaderboard[triviaName]
        except KeyError:
            #value was not already in dicitonary - insert new entry
            self.leaderboard[triviaName] = results
            return

        #value was already in dictionary
        self.leaderboard[triviaName] = self.average_lists(self.leaderboard[triviaName], results)


    def load_game_results(self, triviaName):
        #returns a formatted string with leaderboard results for the given triviaName. If given argument is None then
        #return all trivia games
        #first sort all lists
        for key in self.leaderboard:
            self.leaderboard[key].sort(reverse=True, key=lambda tup: tup[1])
        output = ""
        if triviaName == None or triviaName not in self.leaderboard:
            for key in self.leaderboard:
                output += self.load_game_results(key) + "\n\n"
            return output

        output += triviaName + ":\n"
        for player in self.leaderboard[triviaName]:
            output += player[0] + ": " + str(100*player[1]) + "\n"
        return output



    def average_lists(self, old, new):
        # average the scores in 2 lists
        newnew = []
        for p in new:
            newnew.append(p[0], p[1]/self.max_score)
        megalist = old + newnew
        result = []
        names = []
        for i in range(len(megalist)):
            name = megalist[i][0]
            score = 0
            num = 0
            if name in names:
                continue
            for j in range(len(megalist)):
                if megalist[j][0] == name:
                    score += megalist[j][1]
                    num += 1
            names.append(name)
            print("Name " + str(name) + ", score " + str(score) + ", num " + str(num) + ", maxscore " + str(self.max_score))
            result.append((name, (score/num)))
        return result
