# demo_app2.py
def calculate_sum_up_to_n(n):
    """
    Calculates the sum of all integers from 0 up to and including n.
    Example: calculate_sum_up_to_5 should return 15 (0+1+2+3+4+5).
    """
    total = 0
    # BUG: The range(n) stops at n-1, skipping 'n' itself.
    for i in range(n):  
        total += i
    return total