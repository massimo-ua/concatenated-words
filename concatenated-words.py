import sys


class TreeNode:
    """
    Class that represent leafs of the prefix tree
    """

    def __init__(self, char=False, is_word=False):
        self.children = {}
        self.char = char
        self.is_word = is_word

    def get_child(self, char):
        if char in self.children:
            return self.children[char]
        else:
            return None

    def add_child(self, char):
        new_child = TreeNode(char)
        self.children[char] = new_child
        return new_child

    # mark current node as word
    def set_is_word(self, is_word):
        self.is_word = is_word


class Tree:
    """
    Class that represent the prefix tree
    """

    def __init__(self):
        self.root = TreeNode()
        self.word_length_dictionary = {}

    def add_word(self, word):
        current = self.root
        for char in word:
            # try to get child if exists
            next_child = current.get_child(char)
            # if child not exists we\'ll create it
            if not next_child:
                next_child = current.add_child(char)
            current = next_child
        current.set_is_word(True)
        self._append_word_to_word_length_dictionary(word)

    def _append_word_to_word_length_dictionary(self, word):
        word_length = len(word)
        # check if already exists list of words of that length and use it or create new one
        if word_length in self.word_length_dictionary:
            word_list = self.word_length_dictionary[word_length]
        else:
            word_list = []
        # add word to the list
        word_list.append(word)
        # set or replace list of words with given length
        self.word_length_dictionary[word_length] = word_list

    def is_concatenated(self, word):
        """Recursive function that check if word is compound"""
        is_concatenated = False
        if word:
            for prefix in self.list_prefixes(word):
                prefix_length = len(prefix)
                # cut off prefix from the word
                suffix = word[prefix_length:]
                # if still there is some characters in word
                if suffix:
                    # check if part of the word is in the tree
                    if self.check_word_in_tree(suffix):
                        return True
                    else:
                        # if not continue comparison of the part
                        is_concatenated = self.is_concatenated(suffix)
        return is_concatenated

    def list_prefixes(self, word):
        """
        Get list of prefixes for current word
        :param word:
        :return: list of prefixes
        """
        prefix = ''
        prefix_list = []
        current = self.root
        for char in word:
            current = current.get_child(char)
            if not current:
                return prefix_list
            prefix += char
            if current.is_word:
                prefix_list.append(prefix)
        return prefix_list

    def check_word_in_tree(self, word):
        """
        Check if word exists in the tree, starting from the root
        :param word:
        :return: True|False
        """
        current = self.root
        for char in word:
            current = current.get_child(char)
            if not current:
                return False
        if current.is_word:
            return True
        else:
            return False

    def find_longest_concatenated_word(self, number_of_words=1):
        """
        Finds [number_of_words] longest compound words
        """
        words = []
        # get reversed list of keys (words length)
        reversed_key_list = list(reversed(self.word_length_dictionary.keys()))
        for key in reversed_key_list:
            for word in self.word_length_dictionary[key]:
                if self.is_concatenated(word):
                    if len(words) == number_of_words:
                        return words
                    else:
                        words.append(word)
        return None

    def total_concatenated_words(self):
        count = 0
        reversed_key_list = list(reversed(self.word_length_dictionary.keys()))
        for key in reversed_key_list:
            for word in self.word_length_dictionary[key]:
                if self.is_concatenated(word):
                    count += 1
        return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:  Please specify a filename."
    else:
        filename = sys.argv[1]
        tree = Tree()
        file = open(filename, 'r')
        for word in file:
            if len(word) > 0:
                tree.add_word(word.strip())
        cwl = tree.find_longest_concatenated_word(number_of_words=2)
        print "======== Result ========"
        for index, word in enumerate(cwl):
            print "{} longest concatenated word is: {}".format(index + 1, word)
        print "The total count of all the concatenated words in the file is {}".format(tree.total_concatenated_words())
