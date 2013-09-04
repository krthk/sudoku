import copy, sys

def row(s, i): return s[i]

def col(s, i): return [s[j][i] for j in range(9)]

def block(s, i): 
    row, col = (i/3)*3, (i%3)*3
    return [s[r][c] for r in range(row, row+3) for c in range(col, col+3)]
  
def isSolved(s):
    for i in range(9):
        if sorted(row(s, i)) != range(1,10): return False
        if sorted(col(s, i)) != range(1,10): return False
        if sorted(block(s, i)) != range(1,10): return False
    return True

def isConsistent(s, choices):
    if isSolved(s): return True
    for i in range(9):
        for j in range(9):
            if choices[i][j] == []: return False
      
    for i in range(9):
        for n in range(1, 10):
            if row(s, i).count(n) > 1: return False
            if col(s, i).count(n) > 1: return False
            if block(s, i).count(n) > 1: return False
    return True
        
def printsudoku(s):
    for i in range(9):
        for j in range(9):
            print s[i][j],
            if j == 2 or j == 5: print '|',
        print 
        if i == 2 or i == 5: print '------+-------+------'
    
#In the given ROI (marked by tl and br), get the cells where n can be put
def getSpotsForN(choices, n, tl, br):
    lst = []
    for i in range(tl[0], br[0]+1):
        for j in range(tl[1], br[1]+1):
            if n in choices[i][j]: lst.append((i,j))
    return lst 

#For every non-zero number, remove it from the choices of the cells which are in its radar
def removeFromRadar(s, choices):
    for i in range(9):
        for j in range(9):
            if s[i][j] == 0: continue
            for scan in range(9):
                if scan == j: continue
                cList = choices[i][scan]
                if s[i][j] in cList: cList.remove(s[i][j])

            for scan in range(9):
                if scan == i: continue
                cList = choices[scan][j]
                if s[i][j] in cList: cList.remove(s[i][j])
        
            for l in range((i/3)*3, (i/3)*3+3):
                for m in range((j/3)*3, (j/3)*3+3):
                    if l == i and m == j: continue
                    cList = choices[l][m]
                    if s[i][j] in cList: cList.remove(s[i][j])
    
    for i in range(9):
        for j in range(9):
            if len(choices[i][j]) == 1: s[i][j] = choices[i][j][0]
    return s, choices

def reducesudoku(s, choices):
    for i in range(9):
        for n in range(1,10):
            lst = getSpotsForN(choices, n, (i,0), (i,8))
            if len(lst) == 1: s[lst[0][0]][lst[0][1]], choices[lst[0][0]][lst[0][1]]= n, [n]
          
    for j in range(9):
        for n in range(1, 10):
            lst = getSpotsForN(choices, n, (0,j), (8,j))
            if len(lst) == 1: s[lst[0][0]][lst[0][1]], choices[lst[0][0]][lst[0][1]]= n, [n]
        
    for l in [0, 3, 6]:
        for m in [0, 3, 6]:
            for n in range(1, 10):
                lst = getSpotsForN(choices, n, (l,m), (l+2, m+2))
                if len(lst) == 1: s[lst[0][0]][lst[0][1]], choices[lst[0][0]][lst[0][1]]= n, [n]
    return s, choices

def solvesudoku(s, choices, VERBOSE = True):
    sstack, gstack, cstack = [], [], []

    while True:
        olds = copy.deepcopy(s)
        while True:
            olds = copy.deepcopy(s)
            s, choices = removeFromRadar(s, choices)
            s, choices = reducesudoku(s, choices)
            if s == olds: break
            if isSolved(s): return s
    
    #Guesses till now make the puzzle inconsistant; take a step back and check for consistancy
        if not isConsistent(s, choices): 
            while True:
                if gstack == []: return None
                row, col, val = gstack.pop()
                s = sstack.pop()
                choices = cstack.pop()
                if VERBOSE: print 'Popping %d from (%d, %d):' %(val, row, col),
                clist = choices[row][col]
                if VERBOSE: print clist
                clist.remove(val)
                if clist != []: 
                    s, choices = removeFromRadar(s, choices)
                    s, choices = reducesudoku(s, choices)
                    if isSolved(s): return s
                    if not isConsistent(s, choices): continue
                    olds = copy.deepcopy(s)
                    break
      
    # Hit a wall. Guesses till now are not proven inconsistant, but we need to make another guess
        if olds == s:
            guess = -1, -1, -1
            while guess == (-1, -1, -1):
                for i in range(9):
                    for j in range(9):
                        if guess != (-1, -1, -1): break
                        if s[i][j] == 0:
                            guess = i, j, choices[i][j][0]
                            break
          
        if VERBOSE: 
            print 'Guessing %d at %s' %(choices[guess[0]][guess[1]][0], guess[:-1])
            print 'Pushing', guess[0], guess[1], choices[guess[0]][guess[1]]
        sstack.append(copy.deepcopy(s))
        cstack.append(copy.deepcopy(choices))
        gstack.append(copy.deepcopy(guess))
        s[guess[0]][guess[1]] = guess[2]
         
def testsudoku(filename, VERBOSE = False):
    f = open(filename, 'r')
    count = 0
  
    for line in f:
        s = []
        count +=1
        for i in range(9):
            line = line.replace('.', '0')
            s.append([int(c) for c in line[i*9:i*9+9]])
        choices = [[[k for k in range(1,10)] for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                if s[i][j] != 0: choices[i][j] = [s[i][j]]
        print '\nSolving puzzle#', count
        printsudoku(s)
        s = solvesudoku(s, choices, VERBOSE)
        if s == None: 
            print 'No possible solution'
        else:
            print '\nSolution'
            printsudoku(s)
  
def main(filename, VERBOSE):
    testsudoku(filename, VERBOSE)
    return

if __name__ == '__main__':
    if len(sys.argv) > 3 or (len(sys.argv) == 3 and sys.argv[1] != '-v') or len(sys.argv) == 1: 
        print "Usage: sudoku [-v] [FILE]"
        print "\nEach line in the FILE is interpreted to be an input puzzle."
        print "Each of the 9 rows are appended to each to form a 81-character input puzzle"
        print "Unknown entries in the puzzle are denoted by a period(.)"
        print "\nExample: 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
        print "\nUse the -v flag to print the debug statements."
        sys.exit()
    
    if len(sys.argv) == 2: main(sys.argv[1], False)
    else: main(sys.argv[2], True)
    