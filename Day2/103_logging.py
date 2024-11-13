import logging

# Basic setup
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s',
   filename='app.log'
)

def divide(a, b):
   logging.info(f"Dividing {a} by {b}")
   try:
       result = a / b
       logging.info(f"Result is {result}")
       return result
   except ZeroDivisionError:
       logging.critical("Division by zero!")
       return None

# Example usage
divide(10, 2)    # Logs: "INFO - Dividing 10 by 2" then "INFO - Result is 5.0"
divide(10, 0)    # Logs: "INFO - Dividing 10 by 0" then "ERROR - Division by zero!"
