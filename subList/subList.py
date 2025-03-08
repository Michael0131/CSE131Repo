# 1. Name:
#      Michael Johnson
# 2. Assignment Name:
#      Lab 09 : Sub-List Sort Program
# 3. Assignment Description:
#      I created a sub-list sort program based on a design description.
# 4. What was the hardest part? Be as specific as possible.
#      the design for this program was strong so the hardest part was chosing test cases that would 
#      really make sure this program worked and was reliable. 
# 5. How long did it take for you to complete the assignment?
#      Between programming, debugging, creating test cases and recording 2 hours

def combine(source, destination, iBegin1, iBegin2, iEnd2):
    ''' 
    Merges two sorted sublists from 'source' into the 'destination' array.
    
    Arguments:
    source -- the array containing the sublists to be merged
    destination -- the array where the merged result is stored
    iBegin1 -- the starting index of the first sorted sublist
    iBegin2 -- the starting index of the second sorted sublist
    iEnd2 -- the ending index of the second sorted sublist (exclusive)
    
    Returns:
    destination -- the array with the two merged sorted sublists
    '''
    
    iEnd1 = iBegin2  # Set iEnd1 as the beginning of the second sublist (which is the first to merge)
    
    # Iterate through the destination array, comparing elements from both sublists
    for iDestination in range(iBegin1, iEnd2):
        # If there are elements left in the first sublist, and (either the second sublist is exhausted 
        # or the current element in the first sublist is smaller), we take the element from the first sublist
        if (iBegin1 < iEnd1) and (iBegin2 == iEnd2 or source[iBegin1] < source[iBegin2]):
            destination[iDestination] = source[iBegin1]
            iBegin1 += 1  # Move the pointer for the first sublist
        else:
            destination[iDestination] = source[iBegin2]
            iBegin2 += 1  # Move the pointer for the second sublist
    
    return destination  # Return the destination array with merged sublists

def sublist_sort(array):
    '''
    Sorts an array using the sublist sort method, which repeatedly merges sorted sublists.
    
    Arguments:
    array -- the list to be sorted
    
    Returns:
    src -- the sorted array
    '''
    
    size = len(array)  # Get the length of the input array
    src = array  # Assign the source array (the one to be sorted)
    des = [None] * size  # Create a destination array to hold merged sublists
    num = 2  # Initialize the variable to count the number of sublists (we start with two sublists)
    
    # Continue sorting while there are more than one sublist
    while num > 1:
        num = 0  # Reset the number of sublists for each round of merging
        iBegin1 = 0  # Start from the beginning of the array
        
        # Iterate over the array and find sorted sublists
        while iBegin1 < size:
            iEnd1 = iBegin1 + 1  # Start by assuming a sublist of size 1 (one element)
            
            # Expand the sublist while it's sorted (previous element <= current element)
            while iEnd1 < size and src[iEnd1 - 1] <= src[iEnd1]:
                iEnd1 += 1
            
            iBegin2 = iEnd1  # Now, iBegin2 is where the second sublist starts
            
            if iBegin2 < size:
                iEnd2 = iBegin2 + 1  # Assume a sublist of size 1 (one element)
            else:
                iEnd2 = iBegin2  # If the second sublist is exhausted, set iEnd2 to iBegin2
            
            # Expand the second sublist while it's sorted
            while iEnd2 < size and src[iEnd2 - 1] <= src[iEnd2]:
                iEnd2 += 1
            
            num += 1  # Increase the number of sublists
            
            # Call the combine function to merge the two sublists into 'des'
            combine(src, des, iBegin1, iBegin2, iEnd2)
            
            iBegin1 = iEnd2  # Move the starting index to the end of the second sublist
        
        # After each round, swap the source and destination arrays
        src, des = des, src
    
    return src  # Return the sorted array


def run_tests():
    # Test case 1: Already sorted
    assert sublist_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    # Test case 2: Reverse sorted
    assert sublist_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    # Test case 3: Random order
    assert sublist_sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]
    
    # Test case 4: Duplicates
    assert sublist_sort([4, 4, 4, 4, 4]) == [4, 4, 4, 4, 4]
    
    # Test case 5: Single element
    assert sublist_sort([42]) == [42]
    
    # Test case 6: Empty array
    assert sublist_sort([]) == []
    
    # Test case 7: All negative numbers
    assert sublist_sort([-3, -2, -1, -5, -4]) == [-5, -4, -3, -2, -1]
    
    # Test case 8: Mixed positive and negative numbers
    assert sublist_sort([10, -5, 2, 3, -1, 7, 0]) == [-5, -1, 0, 2, 3, 7, 10]
    
    # Test case 9: Large numbers
    assert sublist_sort([1000, 500, 100, 10, 1]) == [1, 10, 100, 500, 1000]
    
    # Test case 10: All elements the same
    assert sublist_sort([7, 7, 7, 7, 7]) == [7, 7, 7, 7, 7]
    
    # Test case 11: Smallest possible size (empty array)
    assert sublist_sort([100]) == [100]

    # Test Case 12: 20 positive numbers
    assert sublist_sort([10, 23, 5, 17, 42, 90, 32, 50, 67, 8, 12, 4, 99, 65, 1, 34, 11, 44, 26, 9]) == [1, 4, 5, 8, 9, 10, 11, 12, 17, 23, 26, 32, 34, 42, 44, 50, 65, 67, 90, 99]

    # Test Case 13: 20 negative numbers
    assert sublist_sort([-10, -23, -5, -17, -42, -90, -32, -50, -67, -8, -12, -4, -99, -65, -1, -34, -11, -44, -26, -9]) == [-99, -90, -67, -65, -50, -44, -42, -34, -32, -26, -23, -17, -12, -11, -10, -9, -8, -5, -4, -1]

    # Test Case 14: 20 mixed positive and negative numbers
    assert sublist_sort([10, -23, 5, -17, 42, -90, -32, 50, -67, 8, -12, 4, 99, -65, 1, 34, -11, 44, -26, 9]) == [-90, -67, -65, -32, -26, -23, -17, -12, -11, 1, 4, 5, 8, 9, 10, 34, 42, 44, 50, 99]

    # Test Case 15: Floating-point numbers
    assert sublist_sort([10.5, 2.3, 5.7, 4.8, 1.9, 0.2, 6.3, 3.4, 2.1, 8.0, 9.5, 3.6, 7.4]) == [0.2, 1.9, 2.1, 2.3, 3.4, 3.6, 4.8, 5.7, 6.3, 7.4, 8.0, 9.5, 10.5]

    print("All test cases passed!")

# Run the tests
run_tests()




