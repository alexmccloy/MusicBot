import json


"""
Leaderboard json format:
trivia_name <string> : players (player_name, score)[]
"""


class LeaderboardManager:
    self.leaderboardFile = "trivia/leaderboards.json"
    self.learderboard = None

    def load_leaderboard():
        #loads leaderboard into memory
        with open(leaderboardFile) as json_data:
            self.leaderboard = json.load(json_data)
            json_data.close()


    def add_game_results(triviaName, results):
        #first read
