
num_to_board = {i: set() for i in range(100)}
boards = [[[0 for i in range(5)] for j in range(5)] for k in range(100)]
BOARD_SIZE = 5

# Not true that numbers are restricted to colums
def read_boards(f):
    working_board, row, col = 0, 0, 0

    for line in f:
        if line == '\n':
            working_board += 1
            col, row  = 0, 0
        else:
            for n in line.rstrip().split(' '):
                # TODO: yuck, this dooesn't work for single digit numbers. There are probably non-hack solutions
                if (n != ''):
                    num_to_board[int(n)].add((working_board, col, row))
                    boards[working_board][col][row] = int(n)
                    col += 1
            col = 0
            row += 1
    return working_board + 1

def mark_board(board_num, col, row):
    boards[board_num][col][row] = None

def check_board_for_bingo(board_num, col, row):
    if len(list(filter(lambda x: x != None, [boards[board_num][col][i] for i in range(BOARD_SIZE)]))) == 0:
        return True
    if len(list(filter(lambda x: x != None, [boards[board_num][i][row] for i in range(BOARD_SIZE)]))) == 0:
        return True
    return False

def score_board(board_num, called_num):
    return (sum([sum(filter(lambda x: x != None, boards[board_num][i])) for i in range(BOARD_SIZE)]) * called_num)

with open('day4-input.txt') as f:
#with open('day4-input-sample.txt') as f:
    bingo_calls = f.readline().rstrip().split(',')
    f.readline()
    board_count = read_boards(f)
    print (f"Read {board_count} boards")

# Part 1
    # for c in map(int, bingo_calls):
    #     for board_num, col, line in num_to_board[c]:
    #         mark_board(board_num, col, line)
    #         if check_board_for_bingo(board_num, col, line):
    #             print ('board num: ')
    #             print (board_num)
    #             print('score part 1')
    #             print (score_board(board_num, c))
    #             exit()

# Part 2
    bingo_set = set()
    for c in map(int, bingo_calls):
        print(f"calling {c}")
        for board_num, col, line in sorted(num_to_board[c]):
            if board_num not in bingo_set:
                mark_board(board_num, col, line)
                if check_board_for_bingo(board_num, col, line):
                    if len(bingo_set) == board_count -1:
                        print(f"Board {board_num} is the last bingo")
                        print(score_board(board_num, c))
                        exit()
                    else:
                        print(f"Bingo {board_num}")
                        bingo_set.add(board_num)

    # Bingo when all 5 in a row or column is covered
    # These don't need to happen in order
    # You do need to know the other things on the board to score them
    # Numbers are from 0 to 99
    # would like a map from 0-99 to all boards that contain that number

