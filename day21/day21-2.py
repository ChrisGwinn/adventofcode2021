from collections import Counter, namedtuple

GameState = namedtuple('GameState', 'p1_pos p2_pos p1_score p2_score, turn')

track_length = 10
track = [10] + list(range(1, track_length))
roll_to_weight = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

starting_state = GameState(7, 9, 0, 0, 1)
unfinished_games = Counter()
unfinished_games[starting_state] = 1
p1_wins, p2_wins = 0, 0

while len(unfinished_games) > 0:
    for ug, count in frozenset(unfinished_games.items()):
        del unfinished_games[ug]
        for r, w in roll_to_weight.items():
            if ug.turn == 1:
                # player 1
                new_pos = (ug.p1_pos + r) % 10
                new_score = ug.p1_score + track[new_pos]
                if new_score >= 21:
                    p1_wins += count * w
                else:
                    unfinished_games[GameState(new_pos, ug.p2_pos, new_score, ug.p2_score, 2)] += count * w
            else:
                # player 2
                new_pos = (ug.p2_pos + r) % 10
                new_score = ug.p2_score + track[new_pos]
                if new_score >= 21:
                    p2_wins += count * w
                else:
                    unfinished_games[GameState(ug.p1_pos, new_pos, ug.p1_score, new_score, 1)] += count * w

print(f'Player 1 wins: {p1_wins} Player 2 wins: {p2_wins}')