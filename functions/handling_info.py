import re
import openai
import ast
import datetime

SEPARATOR = "=" * 50

def display_final_logs(state):
    print("\033[93m" + "=" * 50 + "\033[0m")
    for key, value in state.items():
        print(f"\033[94m{key}:\033[0m {value}")
    print("\033[93m" + "=" * 50 + "\033[0m")
    
def load_api_key_from_file(filename="apikey.txt"):
    """Loads the API key from the specified file."""
    with open(filename, "r") as f:
        return f.read().strip()
    
def extract_function_details_from_response(response):
    """Extracts function details from the given ChatGPT response."""
    response_message = response["choices"][0]["message"]["content"]
    match = re.search(r'(?P<function_name>\w+)\((?P<args>.+?)\)', response_message)
    if match:
        function_name = match.group('function_name')
        args_str = match.group('args')
        # Ensure domain names are quoted
        args_str = re.sub(r'(?<!")([a-zA-Z0-9.-]+\.com)(?!")', r'"\1"', args_str)
        return function_name, args_str
    return None, None

def parse_args(args_str):
    """
    Parses the arguments string and converts it to a dictionary.
    Args:
    - args_str: A string of the format "key1=value1, key2=value2, ..."
    
    Returns:
    - Dictionary of parsed arguments.
    """
    args = {}
    
    # This will split the string at commas, but not those enclosed within brackets
    # For example, for input:
    # 'subdomains=["api.example.com", "dev.example.com"], port=80'
    # It will split into:
    # ['subdomains=["api.example.com", "dev.example.com"]', ' port=80']
    splitted_args = [part for part in re.split(r',(?![^\[]*\])', args_str)]
    
    for arg in splitted_args:
        parts = arg.split("=")
        if len(parts) == 2:
            key, value = parts
            key = key.strip()

            # Check if the value is a list
            if value.startswith('[') and value.endswith(']'):
                try:
                    value = ast.literal_eval(value)
                except ValueError:
                    print(f"Warning: Skipping malformed argument '{arg}'")
                    continue
            else:
                # Remove quotes around the value if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

            args[key] = value
        else:
            print(f"Warning: Skipping malformed argument '{arg}'")
            
    return args


def request_openai_response(message, functions):
    log_message(message)  # Log the message

    formatted_message = [{"role": "user", "content": message}]  # Formatting the message in the expected format

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=formatted_message,   # Using the correctly formatted message
        functions=functions
    )

def log_message(message):
    """
    Log the message into a log file with a timestamp.
    """
    with open("chat_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"Iteration: {timestamp}\n")
        log_file.write(message + "\n")
        log_file.write(SEPARATOR + "\n")
    
def display_response(content):
    print("\033[93m" + "=" * 50 + "\033[0m")
    print(content)
    print("\033[93m" + "=" * 50 + "\033[0m")
    
    
#! Future ideas
def decide_next_function(state):
    # If no subdomains are discovered, try discovering them
    if state["Subdomains_detected"] == "Not yet discovered":
        return "enumerate_subdomains", {"domain": "professor100110.com"}
    
    # If subdomains are discovered but services are not identified, identify them
    if state["Services_detected"] == "Not yet discovered":
        subdomains = state["Subdomains_detected"].split(", ")
        # Return the first subdomain to scan as an example (you can loop through them later)
        return "identify_tech", {"domain": subdomains[0]}
    
    # Add more such heuristics...

    # If none of the conditions match or you want to exit the loop
    return None, {}
