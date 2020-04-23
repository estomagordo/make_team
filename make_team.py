from collections import defaultdict

class Player:
    def __init__(self, name, nationality, clubs, position, games_played):
        self.name = name
        self.nationality = nationality
        self.clubs = clubs
        self.position = position
        self.games_played = games_played

    def __repr__(self):
        return self.name

class Team:
    position_width = 18

    def __init__(self, players):
        self.players = players
        self.lineups = []
        self.lineup_name_sets = set()
        self.best = 0
    
    def center_print(self, name):
        diff = self.position_width - len(name)

        if diff < 0:
            return name[:self.position_width]

        left = diff // 2 + diff % 2
        right = diff // 2

        return ' ' * left + name + ' ' * right

    def pretty_print(self, lineup):
        lineup.sort(key=lambda player : -player.games_played)

        goalies = [player for player in lineup if player.position == 'G']
        defenders = [player for player in lineup if player.position == 'D']
        attackers = [player for player in lineup if player.position == 'F']

        print(' '.join(attacker.name for attacker in attackers))
        print(' '.join(defender.name for defender in defenders))
        print(' '.join(goalie.name for goalie in goalies))

    def generate_lineups(self):
        players_per_nation = defaultdict(list)

        for player in self.players:
            players_per_nation[player.nationality].append(player)

        nation_groups = sorted(players_per_nation.values(), key=lambda group : len(group))

        def search(pos, nations, clubs, lineup, positions):
            if all(v == 0 for v in positions.values()):
                score = sum(player.games_played for player in lineup)
                if score > self.best:
                    self.best = score
                    print(score)
                    print(sorted(clubs))
                    print(sorted(nations))
                    self.pretty_print(lineup)
                return

            for player in nation_groups[pos]:
                if player.nationality in nations:
                    continue

                if player.clubs & clubs:
                    continue

                if positions[player.position] == 0:
                    continue

                new_positions = dict(positions)
                new_positions[player.position] -= 1

                search(pos + 1, nations | { player.nationality }, clubs | player.clubs, lineup + [player], new_positions)

            remaining_nations = len(nation_groups) - pos - 1

            if remaining_nations >= sum(v for v in positions.values()):
                search(pos + 1, set(nations), set(clubs), list(lineup), dict(positions))

        search(0, set(), set(), [], { 'G': 2, 'D': 4, 'F': 6 })


def parse_clubs(clubstring):
    clubs = set()

    for club in clubstring[1:-1].split(','):
        clubs.add(club.replace('_', ' '))

    return clubs


def get_players():
    players = []

    with open('players.txt', encoding='utf-8') as players_file:
        for line in players_file.readlines():
            name, nation, clubs, position, games_played = line.split()
            clubset = parse_clubs(clubs)
            players.append(Player(
                name.replace('_', ' '),
                nation.replace('_', ' '),
                clubset,
                position,
                int(games_played)
            ))

    return players

if __name__ == '__main__':
    PLAYERS = get_players()

    team = Team(PLAYERS)
    team.generate_lineups()