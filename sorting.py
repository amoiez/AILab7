import heapq

# -------------------------------------------------
# Sorting Algorithms
# -------------------------------------------------

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def heap_sort(arr):
    heap = arr.copy()
    heapq.heapify(heap)
    sorted_list = []
    while heap:
        sorted_list.append(heapq.heappop(heap))
    return sorted_list


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# -------------------------------------------------
# Data Analysis Functions
# -------------------------------------------------

def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def is_reverse_sorted(arr):
    return all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1))


def count_adjacent_disorder(arr):
    count = 0
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            count += 1
    return count


def duplicate_ratio(arr):
    if len(arr) == 0:
        return 0
    unique_count = len(set(arr))
    return 1 - (unique_count / len(arr))


# -------------------------------------------------
# Smart Sorting Framework
# -------------------------------------------------

def smart_sort(arr):
    n = len(arr)

    if n == 0:
        return [], "No algorithm needed", "The list is empty."

    if n == 1:
        return arr.copy(), "No algorithm needed", "The list has only one element."

    if is_sorted(arr):
        return arr.copy(), "No sorting needed", "The list is already sorted."

    disorder = count_adjacent_disorder(arr)
    disorder_ratio = disorder / (n - 1)
    dup_ratio = duplicate_ratio(arr)

    # Decision rules
    if n <= 10:
        chosen = "Insertion Sort"
        reason = "Small list detected, so Insertion Sort is efficient and simple."
        result = insertion_sort(arr)

    elif disorder_ratio < 0.2:
        chosen = "Insertion Sort"
        reason = "List is nearly sorted, so Insertion Sort performs very well."
        result = insertion_sort(arr)

    elif dup_ratio > 0.5:
        chosen = "Merge Sort"
        reason = "Many duplicate values found, so Merge Sort gives stable and reliable performance."
        result = merge_sort(arr)

    elif is_reverse_sorted(arr):
        chosen = "Heap Sort"
        reason = "List is in reverse order, so Heap Sort avoids Quick Sort worst-case style behavior."
        result = heap_sort(arr)

    elif n > 1000:
        chosen = "Python Built-in Sort"
        reason = "Large list detected, so Python's optimized built-in sort is the most practical choice."
        result = sorted(arr)

    else:
        chosen = "Quick Sort"
        reason = "General unsorted input detected, so Quick Sort is a strong average-case choice."
        result = quick_sort(arr)

    return result, chosen, reason


# -------------------------------------------------
# Testing the Framework
# -------------------------------------------------

test_cases = {
    "Small List": [5, 2, 9, 1, 5, 6],
    "Nearly Sorted": [1, 2, 3, 5, 4, 6, 7, 8],
    "Reverse Sorted": [9, 8, 7, 6, 5, 4, 3, 2, 1],
    "Many Duplicates": [4, 2, 2, 8, 3, 3, 3, 1, 4, 4, 4],
    "Large Random Style": [23, 5, 17, 8, 99, 45, 12, 67, 34, 2, 88, 54, 31]
}

for name, data in test_cases.items():
    sorted_list, algorithm, reason = smart_sort(data)
    print(f"\nTest Case: {name}")
    print("Original List :", data)
    print("Chosen Method :", algorithm)
    print("Reason        :", reason)
    print("Sorted List   :", sorted_list)