HW_SOURCE_FILE = 'hw03.py'

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"

    if n <= 3:
        return n
    return g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    "*** YOUR CODE HERE ***"

    if n <= 3:
        return n
    x, y, z = 1, 2, 3
    while n > 3:
        x, y, z = y, z, z + 2*y + 3*x
        n = n -1
    return z


def increment(f):
    return f + 15

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    "*** YOUR CODE HERE ***"

    def nextVal(val, index, switch):
        if index == n:
            return val
        if switch:
            return switchDirection(val+1, index+1, switch)
        return switchDirection(val-1, index+1, switch)

    def switchDirection(val, index, switch):
        if has_seven(index) or index % 7 == 0:
            return nextVal(val, index, not switch)
        return nextVal(val, index, switch)

    return nextVal(1, 1, True)


    '''#Iteration
    i = 1
    iVal = 1
    countSwitch = 0
    while i < n:
        if (has_seven(i) or (i % 7 == 0)) and i == n:
            return n
        elif has_seven(i) or (i % 7 == 0):
            countSwitch += 1
        if countSwitch % 2 == 0:
            iVal = iVal + 1
        elif countSwitch % 2 != 0:
            iVal = iVal - 1
        i += 1
    return iVal'''

def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """

    if k % 10 == 7:
        return True
    elif k < 10:
        return False
    else:
        return has_seven(k // 10)

def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    "*** YOUR CODE HERE ***"

    exponent, i, maxDenomination = 0, 1, 1
    while i < amount:
        maxDenomination = 2 ** exponent
        exponent += 1
        i = i * 2
    y = maxDenomination

    return count_change_using_maxDenom(amount, y)

def count_change_using_maxDenom(amount, n):
    if amount == 0:
        return 1
    elif amount < 0:
        return 0
    elif n == 0:
        return 0
    else:
        return count_change_using_maxDenom(amount-n, n) + count_change_using_maxDenom(amount, n//2)

def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"

    if n == 1:
        print_move(start, end)
    else:
        other = abs(6 - start - end)
        move_stack(n-1, start, other)
        move_stack(1, start, end)
        move_stack(n-1, other, end)


def flatten(lst):
    """Returns a flattened version of lst.

    >>> flatten([1, 2, 3])     # normal list
    [1, 2, 3]
    >>> x = [1, [2, 3], 4]      # deep list
    >>> flatten(x)
    [1, 2, 3, 4]
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> flatten(x)
    [1, 1, 1, 1, 1, 1]
    """
    "*** YOUR CODE HERE ***"
    if len(lst) == 0:
        return lst
    if type(lst[0]) == int:
        return lst[0:1] + flatten(lst[1:])
    if type(lst[0]) == list:
        return flatten(lst[0][0:] + lst[1:])


def merge(lst1, lst2):
    """Merges two sorted lists.

    >>> merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([], [2, 4, 6])
    [2, 4, 6]
    >>> merge([1, 2, 3], [])
    [1, 2, 3]
    >>> merge([5, 7], [2, 4, 6])
    [2, 4, 5, 6, 7]
    """
    "*** YOUR CODE HERE ***"

    if len(lst1) == 0:
        return lst2 
    if len(lst2) == 0:
        return lst1
    if lst1[0] < lst2[0]:
        return [lst1[0]] + merge(lst1[1:], lst2)
    if lst2[0] <= lst1[0]:
        return [lst2[0]] + merge(lst1, lst2[1:])

def mergesort(seq):
    """Mergesort algorithm.

    >>> mergesort([4, 2, 5, 2, 1])
    [1, 2, 2, 4, 5]
    >>> mergesort([])     # sorting an empty list
    []
    >>> mergesort([1])   # sorting a one-element list
    [1]
    """
    "*** YOUR CODE HERE ***"
    
    if len(seq) < 2:
        return seq

    mid = len(seq)//2
    leftSide = mergesort(seq[:mid])
    rightSide = mergesort(seq[mid:])

    return merge(leftSide, rightSide)


###################
# Extra Questions #
###################

from operator import sub, mul

def Y(f):
    """The Y ("paradoxical") combinator."""
    return f(lambda: Y(f))


def Y_tester():
    """
    >>> tmp = Y_tester()
    >>> tmp(1)
    1
    >>> tmp(5)
    120
    >>> tmp(2)
    2
    """
    "*** YOUR CODE HERE ***"
    return Y(________)  # Replace 
