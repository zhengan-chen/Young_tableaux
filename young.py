import numpy as np
from math import factorial
import itertools

def insert_into_row(row,value):
    """
    Inserts a value into a row of the tableau using the bumping rule.
    Returns the bumped value if any, otherwise None.
    """
    for i, x in enumerate(row):
        if value < x:
            row[i] = value
            return x
    row.append(value)
    return None

def robinson_schensted(permutation):
    """
    Implements the Robinson–Schensted algorithm to generate the P and Q tableaux.
    """
    P = []  # The insertion tableau
    Q = []  # The recording tableau
    
    for step, value in enumerate(permutation, 1):
        row_num = 0
        to_insert = value
        
        while row_num < len(P):
            # print(len(P))
            bumped = insert_into_row(P[row_num], to_insert)
            if bumped is None:
                break
            to_insert = bumped
            row_num += 1
        
        if row_num == len(P):
            # Create a new row if we couldn't insert into any existing row
            P.append([to_insert])
        
        # Update the recording tableau
        if row_num == len(Q):
            Q.append([step])
        else:
            Q[row_num].append(step)
    
    return P, Q

def print_tableau(tableau):
    """
    Prints a tableau in a nicely formatted way.
    """
    for row in tableau:
        print(" ".join(map(str, row)))

def get_shape(P):
    """
    Returns the shape of a Young tableau.
    """
    return tuple(len(row) for row in P)


def hook_lengths(shape):
    """
    Compute the hook lengths for each box in a Young diagram of given shape.
    Args:
        shape (list of int): A list where each element represents the number of boxes in a row.
    Returns:
        list of list: A matrix of the same shape where each entry is the hook length of the corresponding box.
    """
    rows = len(shape)
    hooks = []
    
    for i, row_length in enumerate(shape):
        hooks.append([])
        for j in range(row_length):
            # Calculate the hook length for the box at (i, j)
            down = sum(1 for k in range(i + 1, rows) if j < shape[k])  # Boxes below
            right = shape[i] - j - 1  # Boxes to the right
            hooks[-1].append(1 + down + right)  # Include the box itself
    
    return hooks

def hook_formula(shape):
    """
    Compute the number of standard Young tableaux for a given shape using the hook formula.
    Args:
        shape (list of int): A list where each element represents the number of boxes in a row.
    Returns:
        int: The number of standard Young tableaux for the given shape.
    """
    n = sum(shape)  # Total number of boxes
    hooks = hook_lengths(shape)
    
    # Compute the product of all hook lengths
    hook_product = 1
    for row in hooks:
        for h in row:
            hook_product *= h
    
    # Apply the hook formula
    return factorial(n) // hook_product


def print_hook_lengths(hooks):
    """
    Pretty-print the hook lengths matrix.
    """
    for row in hooks:
        print(" ".join(map(str, row)))

def extract_subpermutations(perm, length=4):
    """
    Extract all subsequences of length 4 where the indices satisfy i < j < k < l.
    """
    subperms = []
    for indices in itertools.combinations(range(len(perm)), length):
        subperm = [perm[i] for i in indices]
        subperms.append(subperm)
    return subperms

def ifsmooth(perm):
    """
    Check if a permutation is smooth.
    """
    subpermutations = extract_subpermutations(perm)
    for subperm in subpermutations:
        assert len(subperm) == 4, "Sub-permutations must have length 4"
        if subperm[1]>subperm[0] and subperm[0]>subperm[3] and subperm[3]>subperm[2]:
            return False
        if subperm[0]>subperm[2] and subperm[2]>subperm[1] and subperm[1]>subperm[3]:
            return False
    return True

def knuth_step(S, N):
    '''knuth iteration'''
    perm_list = set()
    for perm in N:
        perm = list(perm)  # Convert tuple to list
        for i in range(len(perm) - 2):
            # First kind of transformation
            if perm[i] > perm[i + 1] and perm[i] < perm[i + 2]:
                new_perm = perm.copy()
                new_perm[i+1], new_perm[i+2] = new_perm[i+2], new_perm[i+1]
                perm_list.add(tuple(new_perm))  # Store as tuple
            if perm[i] < perm[i + 1] and perm[i] > perm[i + 2]:
                new_perm = perm.copy()
                new_perm[i+1], new_perm[i+2] = new_perm[i+2], new_perm[i+1]
                perm_list.add(tuple(new_perm))

            # Second kind of transformation
            if perm[i+2] > perm[i] and perm[i+2] < perm[i+1]:
                new_perm = perm.copy()
                new_perm[i], new_perm[i+1] = new_perm[i+1], new_perm[i]
                perm_list.add(tuple(new_perm))
            if perm[i+2] < perm[i] and perm[i+2] > perm[i+1]:
                new_perm = perm.copy()
                new_perm[i], new_perm[i+1] = new_perm[i+1], new_perm[i]
                perm_list.add(tuple(new_perm))
    
    for perm in S:
        perm = list(perm)  # Convert tuple to list
        for i in range(len(perm) - 2):
            # First kind of transformation
            if perm[i] > perm[i + 1] and perm[i] < perm[i + 2]:
                new_perm = perm.copy()
                new_perm[i+1], new_perm[i+2] = new_perm[i+2], new_perm[i+1]
                perm_list.add(tuple(new_perm))  # Store as tuple
            if perm[i] < perm[i + 1] and perm[i] > perm[i + 2]:
                new_perm = perm.copy()
                new_perm[i+1], new_perm[i+2] = new_perm[i+2], new_perm[i+1]
                perm_list.add(tuple(new_perm))

            # Second kind of transformation
            if perm[i+2] > perm[i] and perm[i+2] < perm[i+1]:
                new_perm = perm.copy()
                new_perm[i], new_perm[i+1] = new_perm[i+1], new_perm[i]
                perm_list.add(tuple(new_perm))
            if perm[i+2] < perm[i] and perm[i+2] > perm[i+1]:
                new_perm = perm.copy()
                new_perm[i], new_perm[i+1] = new_perm[i+1], new_perm[i]
                perm_list.add(tuple(new_perm))
    
    return perm_list
