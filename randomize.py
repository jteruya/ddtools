import random

# Open the file and randomly read in the lines
with open('newusers.csv','r') as source:

    # Pick up the header
    header = source.readline()

    # Pick up lines at random
    data = [ (random.random(), line) for line in source ]

data.sort()

# Write to the file
with open('newusers_random.csv','w') as target:

    # Write the header
    target.write (header)

    # Write the rest of the lines
    for _, line in data:
        target.write( line )