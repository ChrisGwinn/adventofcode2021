#file_to_use = 'day10/day10-sample.txt'
file_to_use = 'day10/day10-input.txt'

score_10_1 = 0
scores_10_2 = []
corrupted_char_scores = {')':3, ']':57, '}':1197, '>':25137}
missing_char_scores = {'(':1, '[':2, '{':3, '<':4}
close_to_open = {')':'(', ']':'[', '}':'{', '>':'<'}
stack = []

def score_stack(stack_to_score):
    score = 0
    while len(stack_to_score) > 0:
        score = (score * 5) + missing_char_scores[stack_to_score.pop()]
    return score


with open(file_to_use) as f:
    for line in [l.strip() for l in f]:
        for c in line:
            if c in close_to_open.keys():
                prev = stack.pop()
                if prev != close_to_open[c]:
                    score_10_1 += corrupted_char_scores[c]
                    stack = []
                    break
            elif c in close_to_open.values():
                stack.append(c)
            else:
                print (f'whoops! should not have a {c} here')
        
        if len(stack) != 0:
            scores_10_2.append(score_stack(stack))

print(f'score for 10-1: {score_10_1}')
print(f'score for 10-2: {sorted(scores_10_2)[len(scores_10_2) // 2]}')

