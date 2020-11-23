

def nextGen(currGen: list):
    ng = [[0 for ee in e] for e in currGen]
    for i in range(len(ng)):
        for j in range(len(ng[i])):
            nb = 0
            if i > 0:
                nb += currGen[i-1][j]
                if j > 0:
                    nb += currGen[i-1][j-1]
                if j < len(currGen[i])-1:
                    nb += currGen[i-1][j+1]
            if i < len(currGen)-1:
                nb += currGen[i+1][j]
                if j > 0:
                    nb += currGen[i+1][j-1]
                if j < len(currGen[i])-1:
                    nb += currGen[i+1][j+1]
            if j > 0:
                nb += currGen[i][j-1]
            if j < len(currGen[i])-1:
                nb += currGen[i][j+1]

            if currGen[i][j] == 1:
                if nb == 2 or nb == 3:
                    ng[i][j] = 1
                else:
                    ng[i][j] = 0
            else:
                if nb == 3:
                    ng[i][j] = 1
    return ng
