import math
import queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data

    def __lt__(self, other):
        return self.data < other.data

    def children(self):
        return (self.left, self.right)


def get_frequencies(fname):
    with open(fname, 'r') as file:
        counts = Counter()
        for line in file:
            counts.update(line)
    return dict(counts.most_common())


def make_huffman_tree(f):
    """Build a Huffman prefix-code tree from character frequencies."""
    p = queue.PriorityQueue()
    for char, frequency in f.items():
        p.put(TreeNode(data=(frequency, char)))

    if p.empty():
        return None

    while p.qsize() > 1:
        x = p.get()
        y = p.get()
        combined_frequency = x.data[0] + y.data[0]
        p.put(TreeNode(left=x, right=y, data=(combined_frequency, "")))

    return p.get()


def get_code(node, prefix="", code=None):
    """Return a dictionary mapping each character to its Huffman code."""
    if code is None:
        code = {}
    if node is None:
        return code

    if node.left is None and node.right is None:
        # A one-character alphabet still receives a one-bit code.
        code[node.data[1]] = prefix or "0"
    else:
        get_code(node.left, prefix + "0", code)
        get_code(node.right, prefix + "1", code)
    return code


def fixed_length_cost(f):
    """Number of bits to encode the text with equal-length codes."""
    if not f:
        return 0
    bits_per_character = max(1, math.ceil(math.log2(len(f))))
    return sum(f.values()) * bits_per_character


def huffman_cost(C, f):
    """Weighted sum of code lengths, measured in bits."""
    return sum(f[char] * len(C[char]) for char in f)


if __name__ == "__main__":
    files = ["f1.txt", "alice29.txt", "asyoulik.txt", "grammar.lsp", "fields.c"]
    print("| File | Fixed-Length Coding (bits) | Huffman Coding (bits) | Ratio |")
    print("|---|---:|---:|---:|")
    for fname in files:
        frequencies = get_frequencies(fname)
        fixed = fixed_length_cost(frequencies)
        tree = make_huffman_tree(frequencies)
        codes = get_code(tree)
        huffman = huffman_cost(codes, frequencies)
        ratio = huffman / fixed if fixed else 0.0
        print(f"| {fname} | {fixed:,} | {huffman:,} | {ratio:.3f} |")