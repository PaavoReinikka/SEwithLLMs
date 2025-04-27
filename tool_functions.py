import time
import requests
from langchain_core.tools import tool

@tool
def get_current_date() -> str:
    '''
    Returns the current date in Finland in format YYYY-MM-DD.
    
    Args:
        None
    Returns:
        str: The current date in Finland in format YYYY-MM-DD.
    '''
    return time.strftime("%Y-%m-%d", time.localtime())

@tool
def get_current_time() -> str:
    '''
    Returns the current time in Finland in format HH:MM.
    
    Args:
        None
    Returns:
        str: The current time in Finland in format HH:MM.
    '''
    return time.strftime("%H:%M", time.localtime())

@tool
def fetch_electricity_price(date: str, time: str) -> str:
    '''
    Fetches the electricity price in Finland from the API using the given date and hour.
    
    Args:
        date (str): The date in format YYYY-MM-DD.
        time (str): The time in format HH:MM.
    
        Returns:
        str: The date and time and the electricity price in EUR/MWh.
             Or an error message if the API call fails.
    '''
    api_address = 'https://api.porssisahko.net/v1/price.json'
    params = f"date={date}&hour={hour}"
    url = f"{api_address}?{params}"
    print(f"Fetching data from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = dict(response.json())
        return f"Electricity price on {date} at {hour}:00 is {data['price']} EUR/MWh"        
    else:
        return f"Failed to fetch data: {response.status_code}"
        

@tool
def fetch_current_electricity_price() -> str:
    '''
    Fetches the current electricity price in Finland from the API
    using the current date and time from system.
    
    Args:
        None
    Returns:
        str: The current date and time and the electricity price in EUR/MWh.
             Or an error message if the API call fails.
    '''
    api_address = 'https://api.porssisahko.net/v1/price.json'
    date = time.strftime("%Y-%m-%d", time.localtime())
    #hour = time.strftime("%H", time.localtime())
    #params = f"date={date}&hour={hour}"
    hour = time.strftime("%H", time.localtime())
    minute = time.strftime("%M", time.localtime())
    params = f"date={date}&hour={hour}&,minute={minute}"
    url = f"{api_address}?{params}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = dict(response.json())
        return f"Current electricity price: {data['price']} EUR/MWh"        
    else:
        return f"Failed to fetch data: {response.status_code}"


@tool
def add(a: int, b: int) -> int:
    '''
    Adds two integers together.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The sum of the two integers.
    '''
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    '''
    Subtracts the second integer from the first.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The result of subtracting b from a.
    '''
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    '''
    Multiplies two integers together.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The product of the two integers.
    '''
    return a * b

@tool
def divide(a: int, b: int) -> float:
    '''
    Divides the first integer by the second.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        float: The result of dividing a by b.
    
    Raises:
        ValueError: If b is zero.
    '''
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

tool_map = {
    "get_current_date": get_current_date,
    "get_current_time": get_current_time,
    "fetch_electricity_price": fetch_electricity_price,
    "fetch_current_electricity_price": fetch_current_electricity_price,
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
}

def get_tools() -> list:
    '''
    Returns the list of tool functions.
    
    Args:
        None
    Returns:
        list: A list of tool functions.
    '''
    return list(tool_map.values())

def get_tool(name: str):
    '''
    Returns the tool function based on the name.
    
    Args:
        name (str): The name of the tool.
    
    Returns:
        function: The tool function.
    '''
    return tool_map.get(name, None)

def get_tool_names() -> list:
    '''
    Returns the list of tool names.
    '''
    return list(tool_map.keys())