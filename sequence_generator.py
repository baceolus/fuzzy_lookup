import random

def sequences_generator(filename):
    output = open(filename, 'w')
    nucleotides = ['a', 't', 'g', 'c']
    sequence = ''

    for i in xrange(100):
        sequence += random.choice(nucleotides)
    
    sequence += '\n'
    print sequence
    print len(sequence)
    
    output.write(sequence)

    output.close()

sequences_generator('yay')