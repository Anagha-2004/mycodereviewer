# demo_app2.py
def safe_divide(numerator, denominator):
    """
    Divides two numbers.
    BUG: Fails when the denominator is 0.
    """
    # Critical Bug: No check for division by zero.
    result = numerator / denominator 
    return result