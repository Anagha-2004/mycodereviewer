# demo_app2.py
def safe_divide(numerator, denominator):
    """
    Divides two numbers, ensuring the denominator is not zero.
    """
    if denominator == 0:
        # Correct fix: return a clear error indicator or raise a ValueError
        return "Error: Cannot divide by zero." 
    
    result = numerator / denominator 
    return result