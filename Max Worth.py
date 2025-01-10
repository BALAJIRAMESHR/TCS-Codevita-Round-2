def calculate_word_worth(word):
    """Calculate the worth of a word based on character positions (a=1, b=2, etc)"""
    return sum(ord(c.lower()) - ord("a") + 1 for c in word)


def find_max_worth(N, strings, costs, contradictions, budget):
    # Calculate worth for each string
    worth_values = []
    for s in strings:
        worth = calculate_word_worth(s)
        worth_values.append(worth)

    # Create adjacency matrix for contradictions
    contra_matrix = [[False] * N for _ in range(N)]
    for s1, s2 in contradictions:
        i = strings.index(s1)
        j = strings.index(s2)
        contra_matrix[i][j] = True
        contra_matrix[j][i] = True

    # Create items list with (cost, worth, index)
    items = [(costs[i], worth_values[i], i) for i in range(N)]

    max_worth = 0

    def backtrack(pos, remaining_budget, selected):
        nonlocal max_worth
        if pos == N:
            current_worth = sum(worth_values[i] for i in selected)
            max_worth = max(max_worth, current_worth)
            return

        # Skip current item
        backtrack(pos + 1, remaining_budget, selected)

        # Try including current item
        if costs[pos] <= remaining_budget:
            can_include = True
            for idx in selected:
                if contra_matrix[idx][pos]:
                    can_include = False
                    break

            if can_include:
                selected.add(pos)
                backtrack(pos + 1, remaining_budget - costs[pos], selected)
                selected.remove(pos)

    backtrack(0, budget, set())
    return max_worth


def solve():
    try:
        # Read input
        N, M = map(int, input().strip().split())
        strings = input().strip().split()
        costs = list(map(int, input().strip().split()))

        # Read contradictions
        contradictions = []
        for _ in range(M):
            s1, s2 = input().strip().split()
            contradictions.append((s1, s2))

        # Read budget
        budget = int(input().strip())

        # Calculate result
        result = find_max_worth(N, strings, costs, contradictions, budget)
        print(result, end="")

    except Exception as e:
        print(0, end="")


if __name__ == "__main__":
    solve()
