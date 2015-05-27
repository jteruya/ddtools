# Not a perfect even split

import random

def partition(l, pred):
    yes, no = [], []
    for e in l:
        if pred(e):
            yes.append(e)
        else:
            no.append(e)
    return yes, no

# Open the file and randomly read in the lines
with open('newusers.csv','r') as source:

    # Pick up the header
    header = source.readline()

    # Pick up lines at random
    lines = [ (line) for line in source ] 

lines.sort()

lines1, lines2 = partition(lines, lambda x: random.random() < 0.5)

# Write to the file
with open('newusers_random_A.csv','w') as target1:

    # Write the header
    target1.write (header)

    # Write the rest of the lines
    for line in lines1:
        target1.write( line )

# Write to the file
with open('newusers_random_B.csv','w') as target2:

    # Write the header
    target2.write (header)

    # Write the rest of the lines
    for line in lines2:
        target2.write( line )        