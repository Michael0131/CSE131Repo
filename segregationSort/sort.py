def segregate(array, iBegin, iEnd):
    if iBegin == iEnd:
        return iBegin  # Single element case
    
    iPivot = (iBegin + iEnd) // 2  # Pivot selection
    iUp = iBegin
    iDown = iEnd

    # Partition loop
    while iUp < iDown:
        while iUp < iDown and array[iUp] <= array[iPivot]:
            iUp += 1  # Move up the index
        
        while iUp < iDown and array[iDown] >= array[iPivot]:
            iDown -= 1  # Move down the index
        
        if iUp < iDown:
            array[iUp], array[iDown] = array[iDown], array[iUp]  # Swap elements
    
    iPivotSwap = iUp

    # Ensure the pivot is in the right place
    if iPivotSwap > iPivot and array[iPivotSwap] > array[iPivot]:
        iPivotSwap -= 1
    
    array[iPivotSwap], array[iPivot] = array[iPivot], array[iPivotSwap]  # Swap pivot
    
    return iPivotSwap

def sort_recursive(array, iBegin, iEnd):
    # Base case: single element or invalid range
    if iEnd < 0 or iEnd - iBegin < 1:
        return
    
    # Partition the array
    iPivot = segregate(array, iBegin, iEnd)
    
    # Recursively sort the two partitions
    sort_recursive(array, iBegin, iPivot - 1)
    sort_recursive(array, iPivot + 1, iEnd)

def sort(array):
        # Wrapper for the provided sort_recursive() function
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