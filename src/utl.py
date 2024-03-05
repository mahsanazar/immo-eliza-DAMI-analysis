import requests
from bs4 import BeautifulSoup
import json
from functools import wraps, partial
import csv
import time
import os


def list_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def list_to_file(data_list, file_path):
    with open(file_path, "w") as file:
        for item in data_list:
            file.write(f"{item}\n")


def dict_to_json_file(data_dict, file_path):
    """
    Saves a dictionary to a JSON file with UTF-8 encoding.

    Args:
        data_dict (dict): The dictionary to save.
        file_path (str): The path to the file where the dictionary should be saved.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


def extract_value_from_nested(searchKey, data):
    """
    Retrieves a value from a nested structure using a sequence of keys/indexes.
    """
    try:
        # Base case for recursion: if searchKey is empty, return the current data
        if not searchKey:
            return data

        # Recursive step: process the first key/index from searchKey
        current_key = searchKey[0]
        next_data = (
            data[current_key] if isinstance(data, list) else data.get(current_key, None)
        )

        # Recursive call with the remaining keys
        return extract_value_from_nested(searchKey[1:], next_data)
    except (TypeError, KeyError, IndexError, AttributeError):
        # In case of an error accessing the data, return None
        return None


def filtered_dict_by_value_path_map(nestedDict, value_paths_map):
    """
    Filters a nested dictionary based on a predefined map of value paths, extracting specified values.

    Example:
        nestedDict = {'person': {'name': 'John', 'age': 30, 'city': 'New York'}}
        VALUE_PATHS_MAP = {'person_name': ['person', 'name'], 'person_age': ['person', 'age']}
        result = filtered_dict_by_attributes_map(nestedDict, VALUE_PATHS_MAP)
        print(result)  # Output: {'person_name': 'John', 'person_age': 30}

    Args:
        nestedDict (dict): The nested dictionary to filter.
        value_paths_map (dict): A mapping of desired keys to their paths in the nestedDict for extracting values.

    Returns:
        dict: A filtered dictionary containing only the keys and values specified in value_paths_map.
    """
    filtered_dict = {}
    for key, value in value_paths_map.items():
        filtered_dict[key] = extract_value_from_nested(value, nestedDict)
    return filtered_dict


def list_of_dicts_to_csv(list_of_dicts, csv_file_name):
    """
    Appends a list of dictionaries to a CSV file. If the file doesn't exist, it creates a new one.

    Parameters:
    - list_of_dicts (list of dict): The list of dictionaries to be written to the CSV file.
    - csv_file_name (str): The name of the CSV file to write to.
    """
    # Check if the file exists to decide on writing headers
    try:
        with open(csv_file_name, "r") as csvfile:
            write_header = False
    except FileNotFoundError:
        write_header = True

    with open(csv_file_name, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = list_of_dicts[0].keys() if list_of_dicts else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()  # Write the column headers only if the file is new

        for dictionary in list_of_dicts:
            writer.writerow(dictionary)


def use_session(func=None, *, headers=None):
    # decorator to use requests.Session
    # partial from the functools module to allow the decorator to be used with or without parameters.
    if func is None:
        return partial(use_session, headers=headers)

    @wraps(func)
    def wrapper(*args, **kwargs):
        with requests.Session() as session:
            if headers:
                session.headers.update(headers)

            return func(session, *args, **kwargs)

    return wrapper


def retry_decorator(max_retries=3, delay=1):
    """A decorator to retry a function call with a delay in case of UnboundLocalError, continuing with execution if all retries fail."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except UnboundLocalError as e:
                    print(
                        f"Retry {retries+1}/{max_retries} for function {func.__name__} due to error: {e}"
                    )
                    time.sleep(delay)  # Pause for delay seconds before retrying
                    retries += 1
            print(
                f"All {max_retries} retries failed for function {func.__name__}. Continuing with execution."
            )
            return None  # Return None or an appropriate value indicating failure

        return wrapper

    return decorator
