# Generators

# Q1

from itertools import permutations

def permutations(lst):
    """Generates all permutations of sequence LST.  Each permutation is a
    list of the elements in LST in a different order.

    >>> sorted(permutations([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> type(permutations([1, 2, 3]))
    <class 'generator'>
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    if not lst:
        yield []
        return

    if not isinstance(lst, list):
        lst = list(lst)

    yield lst # First combination

    for n in lst:
        new_list = lst[:]
        pos = new_list.index(n)
        new_list.pop(pos)
        new_list.insert(0, n)
        for rest in permutations(new_list[1:]):
            if new_list[:1] + rest != lst:
                yield new_list[:1] + rest

# Review

# Q2

def nearest_two(x):
    """Return the power of two that is nearest to x.

    >>> nearest_two(8)    # 2 * 2 * 2 is 8
    8.0
    >>> nearest_two(11.5) # 11.5 is closer to 8 than 16
    8.0
    >>> nearest_two(14)   # 14 is closer to 16 than 8
    16.0
    >>> nearest_two(2015)
    2048.0
    >>> nearest_two(.1)
    0.125
    >>> nearest_two(0.75) # Tie between 1/2 and 1
    1.0
    >>> nearest_two(1.5)  # Tie between 1 and 2
    2.0

    """
    power_of_two = 1.0
    if x < 1:
        factor = 0.5
    else:
        factor = 2
    while abs(power_of_two * factor - x) < abs(power_of_two - x):
        power_of_two = power_of_two * factor
    if abs(power_of_two * 2 - x) == abs(power_of_two - x):
        power_of_two = power_of_two * 2
    return power_of_two

# Q3

def repeated(f, n):
    """Returns a single-argument function that takes a value, x, and applies
    the single-argument function F to x N times.
    >>> repeated(lambda x: x*x, 3)(2)
    256
    """
    def h(x):
        for k in range(n):
            x = f(x)
        return x
    return h

def smooth(f, dx):
    """Returns the smoothed version of f, g where

    g(x) = (f(x - dx) + f(x) + f(x + dx)) / 3

    >>> square = lambda x: x ** 2
    >>> round(smooth(square, 1)(0), 3)
    0.667
    """
    "*** YOUR CODE HERE ***"

    return lambda x: (f(x - dx) + f(x) + f(x + dx)) / 3

def n_fold_smooth(f, dx, n):
    """Returns the n-fold smoothed version of f

    >>> square = lambda x: x ** 2
    >>> round(n_fold_smooth(square, 1, 3)(0), 3)
    2.0
    """
    "*** YOUR CODE HERE ***"
    return repeated(lambda g: smooth(g, dx), n)(f)

# Q4

def make_advanced_counter_maker():
    """Makes a function that makes counters that understands the
    messages "count", "global-count", "reset", and "global-reset".
    See the examples below:

    >>> make_counter = make_advanced_counter_maker()
    >>> tom_counter = make_counter()
    >>> tom_counter('count')
    1
    >>> tom_counter('count')
    2
    >>> tom_counter('global-count')
    1
    >>> jon_counter = make_counter()
    >>> jon_counter('global-count')
    2
    >>> jon_counter('count')
    1
    >>> jon_counter('reset')
    >>> jon_counter('count')
    1
    >>> tom_counter('count')
    3
    >>> jon_counter('global-count')
    3
    >>> jon_counter('global-reset')
    >>> tom_counter('global-count')
    1
    """
    "*** YOUR CODE HERE ***"
    counter = 0

    def inner():

        count = 0

        def helper(msg=""):
            if msg == "count":
                nonlocal count
                count += 1
                return count
            elif msg == "global-count":
                nonlocal counter
                counter += 1
                return counter
            elif msg == "global-reset":
                nonlocal counter
                counter = 0
            elif msg == "reset":
                #nonlocal count
                count = 0

        return helper

    return inner


# Q5

def deck(suits, ranks):
    """Creates a deck of cards (a list of 2-element lists) with the given
    suits and ranks. Each element in the returned list should be of the form
    [suit, rank].

    >>> deck(['S', 'C'], [1, 2, 3])
    [['S', 1], ['S', 2], ['S', 3], ['C', 1], ['C', 2], ['C', 3]]
    >>> deck(['S', 'C'], [3, 2, 1])
    [['S', 3], ['S', 2], ['S', 1], ['C', 3], ['C', 2], ['C', 1]]
    >>> deck([], [3, 2, 1])
    []
    >>> deck(['S', 'C'], [])
    []
    """
    "*** YOUR CODE HERE ***"
    return [[elem, rank] for elem in suits for rank in ranks]

# Q6

def riffle(deck):
    """Produces a single, perfect riffle shuffle of DECK, consisting of
    DECK[0], DECK[M], DECK[1], DECK[M+1], ... where M is position of the
    second half of the deck.  Assume that len(DECK) is even.
    >>> riffle([3, 4, 5, 6])
    [3, 5, 4, 6]
    >>> riffle(range(20))
    [0, 10, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
    """
    "*** YOUR CODE HERE ***"
    return [deck[i//2] if i % 2 == 0 else deck[(len(deck)//2)+(i//2)] for i in range(len(deck))]

# Q7

def is_circular(G):
    """Return true iff G represents a circular directed graph."""
    for v in G:
        if reaches_circularity(G, v):
            return True
    return False

def reaches_circularity(G, v0):
    """Returns true if there is a circularity in G in some path
    starting from vertex V0.
    >>> G = { 'A': ['B', 'D'], 'B': ['C'], 'C': ['F'], 'D': ['E'], 
    ...       'E': ['F'], 'F': ['G'], 'G': ['A'] }
    >>> is_circular(G)
    True
    >>> G['F'] = []
    >>> is_circular(G)
    False
    """
    "*** YOUR CODE HERE ***"

    def is_path_to_cycle(v1):
        for w in G[v1]:
            if v0 == w:
                return True
            if is_path_to_cycle(w):
                return True
            return is_path_to_cycle(w) #make tree recursive

        #return False

    return is_path_to_cycle(v0)

# Q8

class Link:
    empty = ()

    def __init__(self, first, rest=empty):
        if not (rest is Link.empty or isinstance(rest, Link)):
            raise ValueError('rest must be Link or empty')
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is Link.empty:
            return 'Link({})'.format(
                self.first)
        else:
            return 'Link({}, {})'.format(
                self.first, repr(self.rest))

    def __len__(self):
        return 1 + len(self.rest)  # Where's the base case??

def intersection(xs, ys):
    """
    >>> a = Link(1)
    >>> intersection(a, Link.empty) is Link.empty
    True

    >>> b = a
    >>> intersection(a, b).first # intersection begins at a
    1

    >>> looks_like_a = Link(1)
    >>> intersection(a, looks_like_a) is Link.empty # no intersection! (identity vs value)
    True

    >>> b = Link(1, Link(2, Link(3, a)))
    >>> a.first = 5
    >>> intersection(a, b).first # intersection begins at a
    5

    >>> c = Link(3, b)
    >>> intersection(b, c).first # intersection begins at b
    1
    >>> intersection(c, b).first # intersection begins at b
    1

    >>> intersection(a, c).first # intersection begins at a
    5
    """
    "*** YOUR CODE HERE ***"

    #start = Link.empty

    #def helper(x2s, y2s):
        #nonlocal start
    if xs is Link.empty or ys is Link.empty:
        return Link.empty

    if len(xs) > len(ys):
        return intersection(xs.rest, ys)
    elif len(xs) < len(ys):
        return intersection(xs, ys.rest)

    while xs is not ys:
        xs, ys = xs.rest, ys.rest
    return xs

    #helper(xs, ys)
