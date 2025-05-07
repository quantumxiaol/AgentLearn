import math
import mcp
from langchain.tools import tool
def getPrimeinNumN(num):
    """
    This function returns a list of prime numbers up to the given number.
    """
    num = int(num)  
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    return [n for n in range(2, num + 1) if is_prime(n)]

@tool()
def getPrimeinNumN_tool(num) -> str:
    """
    This function returns a list of prime numbers up to the given number.
    """
    primes = getPrimeinNumN(num)
    return f"小于等于 {num} 的质数有: {primes}"




# @mcp.tool()
# def add_numbers(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b