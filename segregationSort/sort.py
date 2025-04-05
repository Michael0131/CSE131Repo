def segregate(array, iBegin, iEnd):
    '''
    Partition function for quicksort.
    Rearranges elements in the array such that elements less than or equal to the pivot 
    are on the left, and elements greater than the pivot are on the right.
    
    Parameters:
        array (list): The list of elements to sort.
        iBegin (int): Starting index of the segment to partition.
        iEnd (int): Ending index of the segment to partition.
    
    Returns:
        int: The index where the pivot element is placed after partitioning.
    '''
    if iBegin == iEnd:
        return iBegin  # Base case: only one element, no need to partition

    iPivot = (iBegin + iEnd) // 2  # Choose the middle element as pivot
    iUp = iBegin  # Start scanning from the beginning
    iDown = iEnd  # Start scanning from the end

    # Partitioning loop: move pointers towards each other
    while iUp < iDown:
        # Move iUp right while elements are <= pivot
        while iUp < iDown and array[iUp] <= array[iPivot]:
            iUp += 1

        # Move iDown left while elements are >= pivot
        while iUp < iDown and array[iDown] >= array[iPivot]:
            iDown -= 1

        # Swap elements that are out of place
        if iUp < iDown:
            array[iUp], array[iDown] = array[iDown], array[iUp]

    iPivotSwap = iUp  # Index where pivot will be swapped

    # Adjust pivot swap index if it's larger than pivot but still out of place
    if iPivotSwap > iPivot and array[iPivotSwap] > array[iPivot]:
        iPivotSwap -= 1

    # Swap pivot with element at its final sorted position
    array[iPivotSwap], array[iPivot] = array[iPivot], array[iPivotSwap]

    return iPivotSwap  # Return the new pivot position


def sort_recursive(array, iBegin, iEnd):
    '''
    Recursive quicksort function.
    Sorts the array by partitioning it and recursively sorting the subarrays.
    
    Parameters:
        array (list): The list of elements to sort.
        iBegin (int): Starting index of the current segment.
        iEnd (int): Ending index of the current segment.
    '''
    # Base case: if subarray is empty or has one element
    if iEnd < 0 or iEnd - iBegin < 1:
        return

    # Partition the array and get pivot index
    iPivot = segregate(array, iBegin, iEnd)

    # Recursively sort the subarrays around the pivot
    sort_recursive(array, iBegin, iPivot - 1)
    sort_recursive(array, iPivot + 1, iEnd)


def sort(array):
    '''
    Public function to sort a list using quicksort.
    
    Parameters:
        array (list): The list of elements to be sorted.
    
    Returns:
        list: The sorted list.
    '''
    # Start the recursive sort with full array bounds
    sort_recursive(array, 0, len(array) - 1)
    return array


def run_tests():


    # Test case 1: Already sorted
    assert sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
     
    # Test case 2: Reverse sorted
    assert sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
     
    # Test case 3: Random order
    assert sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]
     
    # Test case 4: Duplicates
    assert sort([4, 4, 4, 4, 4]) == [4, 4, 4, 4, 4]
     
    # Test case 5: Single element
    assert sort([42]) == [42]
     
    # Test case 6: Empty array
    assert sort([]) == []
     
    # Test case 7: All negative numbers
    assert sort([-3, -2, -1, -5, -4]) == [-5, -4, -3, -2, -1]
     
    # Test case 8: Mixed positive and negative numbers
    assert sort([10, -5, 2, 3, -1, 7, 0]) == [-5, -1, 0, 2, 3, 7, 10]
     
    # Test case 9: Large numbers
    assert sort([1000, 500, 100, 10, 1]) == [1, 10, 100, 500, 1000]
     
    # Test case 10: All elements the same
    assert sort([7, 7, 7, 7, 7]) == [7, 7, 7, 7, 7]
     
    # Test case 11: Smallest possible size (empty array)
    assert sort([100]) == [100]
 
    # Test Case 12: 20 positive numbers
    assert sort([10, 23, 5, 17, 42, 90, 32, 50, 67, 8, 12, 4, 99, 65, 1, 34, 11, 44, 26, 9]) == [1, 4, 5, 8, 9, 10, 11, 12, 17, 23, 26, 32, 34, 42, 44, 50, 65, 67, 90, 99]
 
    # Test Case 13: 20 negative numbers
    assert sort([-10, -23, -5, -17, -42, -90, -32, -50, -67, -8, -12, -4, -99, -65, -1, -34, -11, -44, -26, -9]) == [-99, -90, -67, -65, -50, -44, -42, -34, -32, -26, -23, -17, -12, -11, -10, -9, -8, -5, -4, -1]
 
    # Test Case 14: floating-point numbers 
    assert sort([10.5, 2.3, 5.7, 4.8, 1.9, 0.2, 6.3, 3.4, 2.1, 8.0, 9.5, 3.6, 7.4]) == [0.2, 1.9, 2.1, 2.3, 3.4, 3.6, 4.8, 5.7, 6.3, 7.4, 8.0, 9.5, 10.5]
 
    print("All test cases passed!")

run_tests()