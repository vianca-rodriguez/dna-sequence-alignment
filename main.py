import sys
import csv

if len(sys.argv) > 1:  
    file = sys.argv[1] 
    sequence_pairs = [] 
    match = 1
    mismatch = -1
    gap_penalty = -2

    with open(file, "r") as sequences:
        csvreader = csv.reader(sequences)
        next(csvreader)
        for row in csvreader:
            if len(row) < 2:  
                continue
            s1 = row[0]
            s2 = row[1]
            sequence_pairs.append((s1, s2))

    for i in range(len(sequence_pairs)):
        s1, s2 = sequence_pairs[i]

        # Initialization
        n = len(s1) + 1
        m = len(s2) + 1
        scoring_matrix = [[0] * m for _ in range(n)]

        for i in range(n):
            scoring_matrix[i][0] = gap_penalty * i
        for j in range(m):
            scoring_matrix[0][j] = gap_penalty * j

        # Fill the scoring matrix
        for i in range(1, n):  
            for j in range(1, m):  
                if s1[i - 1] == s2[j - 1]:
                    score = match
                else: 
                    score = mismatch

                scoring_matrix[i][j] = max(
                    scoring_matrix[i - 1][j - 1] + score,  
                    scoring_matrix[i][j - 1] + gap_penalty,  
                    scoring_matrix[i - 1][j] + gap_penalty  
                )

        # Backtracking
        aligned_s1 = []
        aligned_s2 = []
        i, j = n - 1, m - 1

        while i > 0 or j > 0:
            current_score = scoring_matrix[i][j]
            if i > 0 and j > 0 and (current_score == scoring_matrix[i-1][j-1] + (match if s1[i-1] == s2[j-1] else mismatch)):
                aligned_s1.append(s1[i-1])
                aligned_s2.append(s2[j-1])
                i -= 1
                j -= 1
            elif i > 0 and (current_score == scoring_matrix[i-1][j] + gap_penalty):
                aligned_s1.append(s1[i-1])
                aligned_s2.append('-')
                i -= 1
            elif j > 0 and (current_score == scoring_matrix[i][j-1] + gap_penalty):
                aligned_s1.append('-')
                aligned_s2.append(s2[j-1])
                j -= 1


        # Reverse aligned sequences
        aligned_s1.reverse()
        aligned_s2.reverse()

        # Result
        print(''.join(aligned_s1) + " " + ''.join(aligned_s2) + " " + str(scoring_matrix[-1][-1]))

