class HuntersTrieNode():

    def __init__(self, char, partent_node):
        self.char = char
        self.children = {}
        self.partent_node = partent_node
        self.is_terminal = False

    def add_string(self, string_to_add):
        # print('add_string', '-'*10)
        # print('self.char:', self.char)
        # print('self.children:', self.children)
        # print('string_to_add:', string_to_add)

        if len(string_to_add) > 0:
            char_to_add = string_to_add[0]
            if char_to_add not in self.children:
                self.children[char_to_add] = HuntersTrieNode(char_to_add, self)
            self.children[char_to_add].add_string(string_to_add[1:])
        else:
            self.is_terminal = True

    def search(self, string_to_search_for):
        # print('search', '-'*10)
        # print('self.char:', self.char)
        # print('self.children:', self.children)
        # print('string_to_search_for:', string_to_search_for)

        if len(string_to_search_for) == 0:
            if self.is_terminal:
                return True
            else:
                return False
        else:
            active_char = string_to_search_for[0]
            if active_char not in self.children:
                return False
            else:
                return self.children[active_char].search(string_to_search_for[1:])
       

class HuntersTrie():
    def __init__(self):
        self.root_node = HuntersTrieNode('<', None)
    def add_word(self, word):
        self.root_node.add_string(word)
    # def add_words(self, iter):
    #    """Maybe this'll be faster than using a loop.""
    #     next(iter)
    def prefix_search(self, prefix):
        return self.root_node.search(prefix)
    def get_structure(self):
        """
        1. Make a list of all leaf nodes.
        2. Go backwards up family tree of leaf nodes, capturing string.
        3. Reverse string to get word.
        """
        children = [self.root_node]
        leaves = []
        while len(children) > 0:
            remaining_children = []
            for child in children:
                if child.is_terminal:
                    leaves.append(child)
                remaining_children.extend(child.children.values())
            children = remaining_children
        words = []
        for leaf in leaves:
            word = []
            active_node = leaf
            while active_node.partent_node:
                word.append(active_node.char)
                active_node = active_node.partent_node
            words.append(''.join(word[::-1]))
        return words


if __name__ == '__main__':
    # Tests:
    t = HuntersTrie()
    t.add_word('abc')
    t.add_word('abcd')
    t.add_word('xyz')
    assert t.prefix_search('abc') == True
    assert t.prefix_search('abcd') == True
    assert t.prefix_search('xyz') == True
    # print(t.get_structure())
    