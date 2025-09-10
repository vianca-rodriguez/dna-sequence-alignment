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

        #Create Matrices
        rows, cols = len(s1) + 1, len(s2) + 1
        scoring_matrix = [[0] * cols for _ in range(rows)]
        match_checker_matrix = [[0] * len(s2) for _ in range(len(s1))]

        #Match or mismatch
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    match_checker_matrix[i][j] = match
                else:
                    match_checker_matrix[i][j] = mismatch

        #Initialization
        for i in range(rows):
            scoring_matrix[i][0] = i * gap_penalty
        for j in range(cols):
            scoring_matrix[0][j] = j * gap_penalty

        #Fill matrix
        for i in range(1, rows):
            for j in range(1, cols):
                scoring_matrix[i][j] = max(
                    scoring_matrix[i-1][j-1] + match_checker_matrix[i-1][j-1],
                    scoring_matrix[i-1][j] + gap_penalty,
                    scoring_matrix[i][j-1] + gap_penalty 
                )

        #Backtracking
        aligned_s1 = ""
        aligned_s2 = ""

        i, j = len(s1), len(s2)

        while i > 0 or j > 0:
            if i > 0 and j > 0 and scoring_matrix[i][j] == scoring_matrix[i-1][j-1] + match_checker_matrix[i-1][j-1]:
                aligned_s1 = s1[i-1] + aligned_s1
                aligned_s2 = s2[j-1] + aligned_s2
                i -= 1
                j -= 1
            elif i > 0 and scoring_matrix[i][j] == scoring_matrix[i-1][j] + gap_penalty:
                aligned_s1 = s1[i-1] + aligned_s1
                aligned_s2 = "-" + aligned_s2
                i -= 1
            else:
                aligned_s1 = "-" + aligned_s1
                aligned_s2 = s2[j-1] + aligned_s2
                j -= 1

        # Output results 
        result = []
        result.append((aligned_s1, aligned_s2, scoring_matrix[-1][-1]))
        print(aligned_s1 + " " + aligned_s2 + " " + str(scoring_matrix[-1][-1]))
