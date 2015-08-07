import random

def sequences_generator(filename, sequence_len, sequences_number):
    output = open(filename, 'w')
    nucleotides = ['a', 't', 'g', 'c']
    sequence = ''

    for j in xrange(sequences_number):
        sequence = ''
        for i in xrange(sequence_len):
            sequence += random.choice(nucleotides)
        sequence += '\n'
        print sequence
        print len(sequence)
    
        output.write(sequence)

    output.close()

sequences_generator('yay', 100, 10000)