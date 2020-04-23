from collections import defaultdict


def center_print(name, width):
    diff = width - len(name)

    if diff < 0:
        return name[:width]

    left = diff // 2 + diff % 2
    right = diff // 2

    return ' ' * left + name + ' ' * right

class Player:
    def __init__(self, name, nationality, clubs, position, games_played):
        self.name = name
        self.nationality = nationality
        self.clubs = clubs
        self.position = position
        self.games_played = games_played

    def __repr__(self):
        return self.name


class Xi:
    position_width = 18

    def __init__(self, positions, players):
        self.positions = positions
        self.players = players

    def find_position_index(self, position_name, count=1):
        matches = 0

        for i, position in enumerate(self.positions):
            if position == position_name:
                matches += 1
                if matches == count:
                    return i

        return -1

    def print_attack(self):
        lw_pos = self.find_position_index('lw')

        if lw_pos >= 0:
            rw_pos = self.find_position_index('rw')
            st_pos = self.find_position_index('st')

            return ''.join((
                center_print(self.players[lw_pos].name, self.position_width),
                ' ' * self.position_width,
                center_print(self.players[st_pos].name, self.position_width),
                ' ' * self.position_width,
                center_print(self.players[rw_pos].name, self.position_width)
            ))

        striker_a_pos = self.find_position_index('st', 1)
        striker_b_pos = self.find_position_index('st', 2)

        if striker_b_pos >= 0:
            return ''.join((
                ' ' * self.position_width,
                center_print(self.players[striker_a_pos].name, self.position_width),
                ' ' * self.position_width,
                center_print(self.players[striker_b_pos].name, self.position_width),
                ' ' * self.position_width
            ))

        return ''.join((
            ' ' * self.position_width,
            ' ' * self.position_width,
            center_print(self.players[striker_a_pos].name, self.position_width),
            ' ' * self.position_width,
            ' ' * self.position_width
        ))


    def print_midfield(self):
        lm_pos = self.find_position_index('lm')
        rm_pos = self.find_position_index('rm')
        cm_a_pos = self.find_position_index('cm', 1)
        cm_b_pos = self.find_position_index('cm', 2)
        cm_c_pos = self.find_position_index('cm', 3)

        if lm_pos >= 0:
            if cm_c_pos >= 0:
                return ''.join((
                    center_print(self.players[lm_pos].name, self.position_width),
                    center_print(self.players[cm_a_pos].name, self.position_width),
                    center_print(self.players[cm_b_pos].name, self.position_width),
                    center_print(self.players[cm_c_pos].name, self.position_width),
                    center_print(self.players[rm_pos].name, self.position_width)
                ))

            return ''.join((
                center_print(self.players[lm_pos].name, self.position_width),
                center_print(self.players[cm_a_pos].name, self.position_width),
                ' ' * self.position_width,
                center_print(self.players[cm_b_pos].name, self.position_width),
                center_print(self.players[rm_pos].name, self.position_width)
            ))

        return ''.join((
            ' ' * self.position_width,
            center_print(self.players[cm_a_pos].name, self.position_width),
            center_print(self.players[cm_b_pos].name, self.position_width),
            center_print(self.players[cm_c_pos].name, self.position_width),
            ' ' * self.position_width
        ))


    def print_defense(self):
        lb_pos = self.find_position_index('lb')
        rb_pos = self.find_position_index('rb')
        cb_a_pos = self.find_position_index('cb', 1)
        cb_b_pos = self.find_position_index('cb', 2)
        cb_c_pos = self.find_position_index('cb', 3)

        if lb_pos >= 0:
            if cb_c_pos >= 0:
                return ''.join((
                    center_print(self.players[lb_pos].name, self.position_width),
                    center_print(self.players[cb_a_pos].name, self.position_width),
                    center_print(self.players[cb_b_pos].name, self.position_width),
                    center_print(self.players[cb_c_pos].name, self.position_width),
                    center_print(self.players[rb_pos].name, self.position_width)
                ))

            return ''.join((
                center_print(self.players[lb_pos].name, self.position_width),
                center_print(self.players[cb_a_pos].name, self.position_width),
                ' ' * self.position_width,
                center_print(self.players[cb_b_pos].name, self.position_width),
                center_print(self.players[rb_pos].name, self.position_width)
            ))

        return ''.join((
            ' ' * self.position_width,
            center_print(self.players[cb_a_pos].name, self.position_width),
            center_print(self.players[cb_b_pos].name, self.position_width),
            center_print(self.players[cb_c_pos].name, self.position_width),
            ' ' * self.position_width
        ))

    def print_gk(self):
        gk_pos = self.find_position_index('gk')

        return ''.join((
            ' ' * self.position_width,
            ' ' * self.position_width,
            center_print(self.players[gk_pos].name, self.position_width),
            ' ' * self.position_width,
            ' ' * self.position_width
        ))

    def __repr__(self):
        return '\n'.join((
            self.print_attack(),
            self.print_midfield(),
            self.print_defense(),
            self.print_gk()
        ))

class Team:
    def __init__(self, players):
        self.players = players
        self.lineups = []
        self.lineup_name_sets = set()
        self.longest = 0

    def generate_lineups(self):
        players_per_nation = defaultdict(list)

        for player in self.players:
            players_per_nation[player.nationality].append(player)

        nation_groups = sorted(players_per_nation.values(), key=lambda group : len(group))

        def search(pos, nations, clubs, lineup, positions):
            if len(lineup) > self.longest:
                self.longest = len(lineup)
                print(self.longest)
                
            if all(v == 0 for v in positions.values()):
                print(lineup)
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

            if remaining_nations > sum(v for v in positions.values()):
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