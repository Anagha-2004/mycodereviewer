# demo_app2.py
def calculate_sum_up_to_n(n):
    # Bug: The range(n) goes from 0 to n-1, missing 'n' itself.
    total = 0
    for i in range(n):  # Should be range(n + 1)
        total += i
    return tot

# Example: calculate_sum_up_to_5 should be 15, but this code calculates 10.