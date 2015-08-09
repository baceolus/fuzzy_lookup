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
    
        output.write(sequence)
    
    output.write('cccccccccccccccccccccccccccccccccaaccccccccccccccttccccccccccccccccccccccccccccccccccccccccccccccccc\n')
    output.write('cccccccccccccccccccccccccccccccccaaccccccccccccccttccccccccccccccccccccgcccccccccccccccccccccccccccc\n')

    output.close()

sequences_generator('yay', 100, 100)