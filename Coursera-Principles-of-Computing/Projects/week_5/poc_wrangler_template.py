"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    prev_elem = None
    for elem in list1:
        if elem != prev_elem:
            prev_elem = elem
            new_list.append(elem)

    return new_list 

def binary_search(str_list, target_str):
    """
    use binary search to search target_str from sorted str_list
    """
    while len(str_list) > 0:
        middle = len(str_list)/2
        if str_list[middle] == target_str:
            return True
        if str_list[middle] < target_str:
            str_list = str_list[ middle + 1:]
        else:
            str_list = str_list[:middle]

    return False

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    for elem1 in list1:
        if binary_search(list2, elem1):
            new_list.append(elem1)

    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    sorted_list = []
    idx1, idx2 = 0, 0
    while idx1 < len(list1)  and idx2 < len(list2):
        if list1[idx1] <= list2[idx2]:
            sorted_list.append(list1[idx1])
            idx1 = idx1 + 1
        else:
            sorted_list.append(list2[idx2])
            idx2 = idx2 + 1

    if idx1 < len(list1):
        sorted_list = sorted_list + list1[idx1:]
    else:
        sorted_list = sorted_list + list2[idx2:]

    return sorted_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1

    length = len(list1)
    first_list = merge_sort( list1[:length/2] )
    second_list = merge_sort( list1[length/2:] )
    list1 = merge(first_list, second_list) 
    return list1

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) < 1:
        return [""]
    fir_char = word[0]
    rest_strings = gen_all_strings( word[1:] )
    generated_string = []
    for string in rest_strings:
        for idx in range( len(string) + 1 ):
            temp_str = string[0:idx] + fir_char + string[idx:]
            generated_string.append( temp_str )

    generated_string = generated_string + rest_strings
    return  generated_string

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    response = urllib2.urlopen('http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt')
    # strip() remove whitespace
    return [line.strip() for line in response.readlines() ] 

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

#Uncomment when you are ready to try the game
run()


    
    
