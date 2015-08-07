class sequence(object):

    def __init__(self, seq, n, id = -1):
        self.seq = seq
        self.id = id
        self.n = n
        self.len = len(seq)

    def cut_sequence(self):
        '''
        cut sequence into list of N-grams of length n
        '''
        output = []
        for i in xrange(self.len- self.n + 1):
            output.append(self.seq[i:i + self.n])

        return output

    def get_id(self):
        return self.id

    def get_sequence(self):
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
        self.graph = graph()
        self.add_sequences(sequences, self.graph)

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
        for seq in sequences:
            self.add_sequence(seq, graph)

def read_sequences(filename, n):
    sequences = []
    index = 0
    inp_file = open(filename)

    for line in inp_file:
        sequences.append(sequence(line[:-1], n, index))
        index += 1

    inp_file.close()
    return sequences

sequences = read_sequences('sequences.txt', 15)
my_map = ngram_map(sequences)

print my_map.word_map
