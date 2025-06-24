import random
import time

# Constants
N_VALUES = [500, 10000, 100000]

comparison_count = 0

def reset_comparison_count():
    global comparison_count
    comparison_count = 0

def increment_comparison():
    global comparison_count
    comparison_count += 1

# Standard Quick Sort
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        increment_comparison()
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Modified Quick Sort with Median-of-Three and Hybrid Insertion Sort
def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low:
            increment_comparison()
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key

def median_of_three(arr, low, mid, high):
    a, b, c = arr[low], arr[mid], arr[high]
    if (a - b) * (c - a) >= 0:
        return low
    elif (b - a) * (c - b) >= 0:
        return mid
    else:
        return high

def modified_quick_sort(arr, low, high):
    INSERTION_SORT_THRESHOLD = 10
    if high - low + 1 <= INSERTION_SORT_THRESHOLD:
        insertion_sort(arr, low, high)
    else:
        mid = (low + high) // 2
        median_index = median_of_three(arr, low, mid, high)
        arr[median_index], arr[high] = arr[high], arr[median_index]
        pi = partition(arr, low, high)
        modified_quick_sort(arr, low, pi - 1)
        modified_quick_sort(arr, pi + 1, high)

def merge(arr, aux, left, mid, right):
    i, j, k = left, mid + 1, left
    while i <= mid and j <= right:
        increment_comparison()
        if arr[i] <= arr[j]:
            aux[k] = arr[i]
            i += 1
        else:
            aux[k] = arr[j]
            j += 1
        k += 1
    while i <= mid:
        aux[k] = arr[i]
        i, k = i + 1, k + 1
    while j <= right:
        aux[k] = arr[j]
        j, k = j + 1, k + 1
    for t in range(left, right + 1):
        arr[t] = aux[t]

def top_down_merge_sort(arr, aux, left, right):
    INSERTION_SORT_THRESHOLD = 32
    if right - left + 1 <= INSERTION_SORT_THRESHOLD:
        insertion_sort(arr, left, right)
    elif left < right:
        mid = (left + right) // 2
        top_down_merge_sort(arr, aux, left, mid)
        top_down_merge_sort(arr, aux, mid + 1, right)
        merge(arr, aux, left, mid, right)

def bottom_up_merge_sort(arr, aux):
    INSERTION_SORT_THRESHOLD = 32
    n = len(arr)
    size = 1
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if right - left + 1 <= INSERTION_SORT_THRESHOLD:
                insertion_sort(arr, left, right)
            else:
                merge(arr, aux, left, mid, right)
        size *= 2

def measure_sort(func, arr):
    data = arr.copy()
    aux = [0] * len(data)
    start = time.perf_counter()
    if func is bottom_up_merge_sort:
        func(data, aux)
    else:
        func(data, aux, 0, len(data) - 1)
    end = time.perf_counter()
    return end - start

def test_sorting_algorithm(data, algorithm, name):
    global comparison_count
    data_copy = data.copy()
    reset_comparison_count()
    try:
        start_time = time.perf_counter()
        if algorithm is bottom_up_merge_sort:
            aux = [0] * len(data_copy)
            algorithm(data_copy, aux)
        elif algorithm is top_down_merge_sort:
            aux = [0] * len(data_copy)
            algorithm(data_copy, aux, 0, len(data_copy) - 1)
        else:
            algorithm(data_copy, 0, len(data_copy) - 1)
        end_time = time.perf_counter()
        return (end_time - start_time) * 1000, comparison_count
    except RecursionError:
        return None, None

def main():
  random.seed(42)
  
  # Store results for all test cases
  results = {
      'Random Data': {},
      'Ascending Sorted Data': {},
      'Descending Sorted Data': {},
      'Partially Sorted Data': {}
  }
  
  algorithms = [
      (quick_sort, "Quick Sort"),
      (modified_quick_sort, "Quick Sort Hybrid"),
      (top_down_merge_sort, "Merge Sort Top-Down"),
      (bottom_up_merge_sort, "Merge Sort Bottom-Up")
  ]
      
  for N in N_VALUES:
      # Test 1: Random data
      def run_test(test_name, data_generator, algorithms, results, N):
          """Run a test for a specific data type and store results"""
          data = data_generator(N)
          for algo_func, algo_name in algorithms:
              # Skip Quick Sort for large N on sorted data to avoid stack overflow
              if (algo_name == "Quick Sort" and N > 500 and 
                  test_name in ['Ascending Sorted Data', 'Descending Sorted Data']):
                  if algo_name not in results[test_name]:
                      results[test_name][algo_name] = {}
                  results[test_name][algo_name][N] = (None, None)
              else:
                  time_ms, comparisons = test_sorting_algorithm(data, algo_func, algo_name)
                  if algo_name not in results[test_name]:
                      results[test_name][algo_name] = {}
                  results[test_name][algo_name][N] = (time_ms, comparisons)

      # Data generators
      def generate_random_data(N):
          return [random.randint(0, 100000) for _ in range(N)]

      def generate_ascending_data(N):
          data = [random.randint(0, 100000) for _ in range(N)]
          data.sort()
          return data

      def generate_descending_data(N):
          data = [random.randint(0, 100000) for _ in range(N)]
          data.sort(reverse=True)
          return data

      def generate_partially_sorted_data(N):
          data = [random.randint(0, 100000) for _ in range(N)]
          for i in range(0, int(N * 0.95)):
              data[i] = i
          return data

      # Test cases configuration
      test_cases = [
          ('Random Data', generate_random_data),
          ('Ascending Sorted Data', generate_ascending_data),
          ('Descending Sorted Data', generate_descending_data),
          ('Partially Sorted Data', generate_partially_sorted_data)
      ]

      # Run all tests
      for test_name, data_generator in test_cases:
          run_test(test_name, data_generator, algorithms, results, N)
  
  # Print formatted tables
  def print_table(title, data):
      print(f"\n{title}") 
      print("+" + "-"*24 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+")
      print(f"| {'Algorithm':<22} | {'Time@.5k':<8} | {'Comparison':<10} | {'Time':<8} | {'Comparison':<10} | {'Time':<8} | {'Comparison':<10} |")
      print(f"| {'':<22} | {'(ms)':<8} | {'@.5k':<10} | {'@10k':<8} | {'@10k':<10} | {'@100k':<8} | {'@100k':<10} |")
      print("+" + "-"*24 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+")

      for algo_name in ["Quick Sort", "Quick Sort Hybrid", "Merge Sort Top-Down", "Merge Sort Bottom-Up"]:
          if algo_name in data:
              row = f"| {algo_name:<22} |"
              for N in [500, 10000, 100000]:
                  if N in data[algo_name] and data[algo_name][N][0] is not None:
                      time_val, comp_val = data[algo_name][N]
                      row += f" {time_val:>8.1f} |"
                      row += f" {comp_val:>10,.0f} |"
                  else:
                      row += f" {'N/A':>8} | {'N/A':>10} |"
              print(row)
      print("+" + "-"*24 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+")
          
  # Print all tables
  for test_name, test_data in results.items():
      print_table(f"Table. Results on {test_name}", test_data)

if __name__ == "__main__":
  main()
