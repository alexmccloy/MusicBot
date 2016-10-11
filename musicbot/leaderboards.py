import json
import os

"""
Leaderboard json format:
trivia_name <string> : players (player_name, score)[]
"""


class LeaderboardManager:
    def __init__(self):
        self.leaderboardFile = "trivia/leaderboards.json"
        self.learderboard = None

    def load_leaderboard():
        #loads leaderboard into memory from file - must be called before leaderboards can be used
        with open(leaderboardFile) as json_data:
            self.leaderboard = json.load(json_data)
            json_data.close()

    def save_leaderboard():
        if self.leaderboard == None:
            return
        #moves exising leaderboard to leaderboard2.json and then writes leaderboard in current memory to file
        #this will backup the previous leaderboard but keep only 1 backup at a time
        os.rename(self.leaderboardFile, self.leaderboardFile + "_backup")
        newFile = open(self.leaderboardFile, "w")
        newfile.write(json.dumps(self.leaderboard))
        newfile.close()

    def add_game_results(triviaName, results):
        #adds game results to leaderboards for a single triviaName(dictionary key). If game exists will update the
        #values, else will create a new entry
        try:
            oldEntry = self.leaderboard[triviaName]
        except KeyError:
            #value was not already in dicitonary - insert new entry
            self.leaderboard[triviaName] = results
            return

        #value was already in dictionary
        self.leaderboard[triviaName] = average_lists(self.leaderboard[triviaName], results)


    def load_game_results(triviaName):
        #returns a formatted string with leaderboard results for the given triviaName. If given argument is None then
        #return all trivia games
        output = ""
        if triviaName == None or triviaName not in self.leaderboard:
            for key in self.leaderboard:
                output += load_game_results(key) + "\n\n"
            return output

        output += triviaName + ":\n"
        for player in self.leaderboard[triviaName]:
            output += player[0] + ": " + player[1] + "\n"
        return output



    def average_lists(old, new):
        # average the scores in 2 lists
        megalist = old + new
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
            result.append((name, int(score/num)))
        return result
