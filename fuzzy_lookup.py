import time

class sequence(object):

    def __init__(self, seq, n = 15, id = -1):
        self.seq = seq
        self.id = id
        self.n = n
        self.len = len(seq)

    def cut_sequence(self):
        output = []
        for i in xrange(self.len- self.n + 1):
            output.append(self.seq[i:i + self.n])

        return output

    def get_id(self):
        return self.id

    def get_sequence(self):
        return self.seq

    def get_length(self):
        return self.len

    def __str__(self):
        return self.seq


class node(object):

    def __init__(self, name, value = -1):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name)

    def get_value(self):
        return self.value
    

class graph(object):

    def __init__(self):
        root = node('r', 0)
        self.nodes = [root]
        self.edges = {root:[]}
        self.node_index = 1
        
    def add_child(self, parent, child):
        self.edges[parent].append(child)

    def children(self, node):
        return self.edges[node] 

    def children_names(self, node):
        names = ''
        
        for nodes in self.edges[node]:
            names += str(nodes)

        return names

    def choose_node(self, nodes_list, name):
        for node in nodes_list:
            if str(node) == name:
                return node
        raise NameError('no such nodes')

    def add_node(self, name):
        new_node = node(name, self.node_index)
        self.node_index += 1
        self.nodes.append(new_node)
        self.edges[new_node] = []
        
        return new_node

    def add_ngram(self, ngram):
        node = self.nodes[0]
        i = 0
        n = len(ngram)

        while i < n:
            if ngram[i] in self.children_names(node):
                node = self.choose_node(self.children(node), ngram[i])
                i += 1
            else:
                break

        while i < n:
            new_node = self.add_node(ngram[i])
            self.add_child(node, new_node)
            node = new_node
            i += 1

        return node.get_value()

    def add_sequence(self, seq):
        ngrams = seq.cut_sequence()
        ngram_ids = []

        for each in ngrams:
            ngram_ids.append(self.add_ngram(each))

        return seq.get_id(), ngram_ids


class ngram_map(object):
    '''
    this class contains a dictionary which maps IDs of all sequences, containing each N-gram
    '''
    def __init__(self, sequences):
        self.word_map = {}
        print 'graph creation begins'
        t1 = time.time()
        self.graph = graph()
        self.sequences_quantity = str(len(sequences))
        self.add_sequences(sequences, self.graph)
        print 'graph creation ends. Total time = ' + str(time.time() - t1)

    def add_ngram(self, ngram_id, seq_id):
        try:
            self.word_map[ngram_id].append(seq_id)
        
        except:
            self.word_map[ngram_id] = [seq_id]

    def add_sequence(self, seq, graph):
        seq_id, ngram_ids = graph.add_sequence(seq)

        for ngram_id in ngram_ids:
            self.add_ngram(ngram_id, seq_id)

    def add_sequences(self, sequences, graph):
        index = 1
        for seq in sequences:
            t1 = time.time()
            self.add_sequence(seq, graph)
            tim = time.time() - t1
            print str(index) + ' of ' + self.sequences_quantity + ' sequences added \
             \n time = '+ str(tim)
            index += 1
        
    def examine_sequence(self, seq, hits = 5):
        '''
        takes all sequences and return only the ones
        wich have at least 5(variable hits) common N-grams with query sequence
        '''
        ngrams = self.graph.add_sequence(seq)[1]
        candidates = {}
        chosen_ids = []

        for ngram in ngrams:
            
            try:
                for seq in self.word_map[ngram]:
                    if seq in candidates:
                        candidates[seq] += 1
                    else:
                        candidates[seq] = 0

            except KeyError:
                pass

        for seq in candidates:
            if candidates[seq] >= hits:
                chosen_ids.append(seq)

        return chosen_ids


class manipulations(object):

    def __init__(self, filename, n, treshold):
        self.n = n #length of N-grams
        self.index = 0
        self.sequences = []
        self.treshold = treshold
        self.read_sequences(filename)

        self.map = ngram_map(self.sequences)
    
    def similar_sequences(self, seq, string_output = True):
        candidate_ids = self.map.examine_sequence(seq)
        candidate_sequences = self.retrieve_sequences(candidate_ids)
        chosen_sequences = []

        for each in candidate_sequences:

            mismatches = needle(seq, each).score()
            if mismatches <= self.treshold:
                if string_output:
                    chosen_sequences.append([str(each), mismatches])
                else:
                    chosen_sequences.append([each, mismatches])

        return chosen_sequences

    def retrieve_sequences(self, seq_ids):
        sequences = []
        if type(seq_ids) == int:
            seq_ids = [seq_ids]

        for each in seq_ids:
            seq = self.sequences[each]
            sequences.append(seq)

        return sequences 

    def read_sequences(self, filename):
        inp_file = open(filename)
    
        for line in inp_file:
            self.sequences.append(sequence(line[:-1], self.n, self.index))
            self.index += 1

        inp_file.close()

class needle(object):

    def __init__(self, seq1, seq2):
        self.seq1 = seq1.get_sequence()
        self.seq1_len = seq1.get_length()
        self.seq2 = seq2.get_sequence()
        self.seq2_len = seq2.get_length()
        self.matrix = self.score_matrix()

    def score_matrix(self):
        matrix = [[]]
        penalty1, penalty2 = 0, -1

        for i in xrange(self.seq1_len + 1):
            matrix[0].append(penalty1)
            penalty1 -= 1

        for i in self.seq2:
            matrix.append([])
            matrix[-1].append(penalty2)
            penalty2 -= 1
            
            for j in self.seq1:
                if i == j:
                    matrix[-1].append(0)
                else:
                    matrix[-1].append(-1)
        
        return matrix

    def score(self):
        
        for i in xrange(1, self.seq2_len + 1):
        
            for j in xrange(1, self.seq1_len + 1):
                seq1_gap = self.matrix[i - 1][j] - 1
                seq2_gap = self.matrix[i][j - 1] - 1
                no_gap = self.matrix[i - 1][j - 1] + self.matrix[i][j]
                self.matrix[i][j] = max(seq1_gap, seq2_gap, no_gap)

        return abs(self.matrix[-1][-1])






test = manipulations('yay', 15, 5)
s = sequence('cccccccccccccccccccccccccccccccccaaccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
for seq in test.similar_sequences(s):
    print seq


