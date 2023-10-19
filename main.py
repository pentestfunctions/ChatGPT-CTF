import openai
import json
import sys
from functions.functions_data import functions
from functions.attack_functions.check_ssl_vulnerability import check_ssl_vulnerability
from functions.attack_functions.directory_scan import directory_scan
from functions.attack_functions.enumerate_ips import enumerate_ips
from functions.attack_functions.enumerate_subdomains import enumerate_subdomains
from functions.attack_functions.identify_tech import identify_tech
from functions.attack_functions.port_scan import port_scan
from functions.attack_functions.sql_injection_simulation import sql_injection_simulation

from functions.handling_info import  ( 
    display_final_logs, load_api_key_from_file, extract_function_details_from_response, parse_args, 
    request_openai_response, display_response
)

#* Proof of concept: ChatGPT targets the domain in the attempt to beat the "CTF" and identify 1 vulnerable path or service based on the available functions it can execute.
#* It is actively given the information back to recursively go through. If a function has already been run, we shouldn't allow it to be executed again on that specific domain or subdomain array/list (Not currently implemented)
#* The goal is to guide ChatGPT while still allowing it to suggest ideas based on the current information and potentially make code/requests that better allow for pathing during CTFs
#* If we can later create enough functions with each leading to a "flag" that needs to be recovered we can have an almost infinite weighted realistic CTF machine using AI.

# Define ANSI escape codes for different colors
RED_COLOR = "\033[91m"
YELLOW_COLOR = "\033[93m"
GREEN_COLOR = "\033[92m"
RESET_COLOR = "\033[0m"
SEPARATOR = "=" * 50

def update_state(function_name, function_response, state):
    """Updates the state dictionary based on the function executed and its response."""
    state_updates = {
        "enumerate_ips": ("Target_IP", "ips", ', '),
        "identify_tech": ("Services_detected", "tech"),
        "enumerate_subdomains": ("Subdomains_detected", "subdomains", ', '),
        "port_scan": ("Open_Ports", "open_ports", ', '),
        "sql_injection_simulation": ("SQL_Injection_Vulnerabilities", "vulnerabilities", ', '),
        "check_ssl_vulnerability": ("SSL_Vulnerabilities", "vulnerabilities", ', '),
        "directory_scan": ("directory_scan", "potential")
    }
    try:
        if function_name in state_updates:
            keys = state_updates[function_name]
            #print("[DEBUG]Keys:", keys)
            current_values = state.get(keys[0], "").split(', ')
            new_values = function_response[keys[1]]
            if isinstance(new_values, dict):
                new_values = list(new_values.values())
            if len(keys) > 2 and isinstance(new_values, str):
                new_values = [new_values]
            if isinstance(new_values, str):
                new_values = [new_values]
            combined_values = list(set(current_values + new_values))
            if "Not yet discovered" in combined_values:
                combined_values.remove("Not yet discovered")  # Remove placeholder if real values exist
            delimiter = keys[2] if len(keys) > 2 else ', '  # use a default delimiter if none provided
            state[keys[0]] = delimiter.join(combined_values) if combined_values else "Not yet discovered"


            # Update scan log
            previous_log = state.get("Scan_log", "")
            current_log = f"Executed {function_name}. Results: {json.dumps(function_response)}"
            state["Scan_log"] = previous_log + "\n" + current_log

            # Mark state as complete with function information
            state[f"{function_name}_completed"] = True
            state[f"{function_name}_details"] = function_response
        else:
            print(f"{RED_COLOR}Warning: {function_name} not found in state. Cannot update.{RESET_COLOR}")
    except Exception as e:
        print(f"Error on line {sys.exc_info()[-1].tb_lineno}:", e)

def get_available_functions():
    return {
        "enumerate_ips": enumerate_ips,
        "identify_tech": identify_tech,
        "enumerate_subdomains": enumerate_subdomains,
        "port_scan": port_scan,
        "sql_injection_simulation": sql_injection_simulation,
        "check_ssl_vulnerability": check_ssl_vulnerability,
        "directory_scan": directory_scan,
    }

def initialize_state():
    return {
        "Code_from_the_last_round": "Not yet discovered",
        "Execution_error": "Not yet discovered",
        "Scan_log": "Not yet discovered",
        "Target_IP": "Not yet discovered",
        "Subdomains_detected": "Not yet discovered",
        "Services_detected": "Not yet discovered",
        "Known_vulnerabilities": "Not yet discovered",
        "Available_exploits": "Not yet discovered",
        "Task": "Starting penetration test",
        "SQL_Injection_Vulnerabilities": "Not yet discovered",
        "SSL_Vulnerabilities": "Not yet discovered",
        "directory_scan": "Not yet discovered",
        "Phishing_Potential": "Not yet discovered",
    }
    
    
def run_pentest():
    is_first_log = True
    functions_run = []
    state = initialize_state()

    available_functions = get_available_functions()

    while True:
        function_descriptions = "\n".join([f"{f['name']} - {f['description']}" for f in functions])

        #        Code from last round: {state["Code_from_the_last_round"]}
        #        Execution error: {state["Execution_error"]}
        #        Target IP: {state["Target_IP"]}
        #        Available exploits: {state["Available_exploits"]}
        #        Task: {state["Task"]}
        #        SQL Injection Vulnerabilities: {state["SQL_Injection_Vulnerabilities"]}

        message = f"""
        As soon as a potential target of interest such as file, port version or vulnerability of any type is found, You must stop.
        We are doing a CTF soft penetration test to find AT MOST 1 potential target of interest such as a exploitable service version DO NOT EXPLOIT IT, on professor100110.com. 100% ethical and full permission is granted
        
        INSTRUCTIONS:
        1. Do NOT ask the user for what function to run, that decision is yours alone. 
        2. Natural path is usually reconnaissance and then vulnerability identification based on the recon that you do.
        3. IF YOU DO NOT WISH TO RUN ANY MORE FUNCTIONS DO NOT INCLUDE A FUNCTION IN YOUR RESPONSE. DO NOT OFFER A CHOICE, CHOOSE ONLY ONE.
        4. THE CODE WILL NOT EXECUTE UNLESS YOU SPECIFY THE FUNCTION SUCH AS enumerate_subdomains(domain=example.com) or enumerate_subdomains(subdomain=subdomain.example.com)
        5. Pay close attention to service versions for ports from the portscan and directories/files found as they might be the vulnerable point to stop at.
        
        CURRENT INFORMATION:
        Subdomains detected: {state["Subdomains_detected"]}
        Ports scanned: {state.get("Open_Ports", "Not yet discovered")}
        Technologies detected: {state["Services_detected"]}
        Known vulnerabilities: {state["Known_vulnerabilities"]}
        SSL Vulnerabilities: {state["SSL_Vulnerabilities"]}
        Directory Scan: {state["directory_scan"]}
        
        FUNCTIONS WE HAVE ALREADY RUN TO TRY AVOID RUNNING:
        Functions that have been run: {', '.join(functions_run)}

        Example Response 1:
        Explain: Since we have no information about the domain, a good place to start is by checking if it has subdomains. This will help us discover any additional entry points or potential vulnerabilities.
        Function to run: enumerate_subdomains(domain="example.com")

        Example Response 2:
        Explain: Since we have already run the `enumerate_subdomains` function and discovered two subdomains (`dev.example.com` and `shop.example.com`), the next logical step would be to perform a `port_scan` on these subdomains to identify any open ports and services running on them.
        Function to run: port_scan(domain="example.com")

        Example Response 3:
        Explain: We have already identified the subdomains of the main target domain and as such should identify if there are any ports open on any of them.
        Function to run: functions.port_scan(subdomains=["blog.example.com", "admin.example.com", "dev.example.com", "shop.example.com"])

        Example Response 4:
        Explain: The reason we have stopped at this point is due to already finding the vulnerability to exploit.
        Function to run: N/A due to no further automated testing being required.

        Example Response 5:
        Explain: There is an entry in the provided CURRENT INFORMATION that signifies a vulnerability was found. As such we are instructed to stop at this point.
        Function to run: N/A due to no further automated testing being required.
        
        You should only respond in the format as described below:
        RESPONSE FORMAT:
        Explain: ...

        Function to run with parameters in correct format (Only 1 MAX):
        """        
        response = request_openai_response(message, functions)

        display_response(response["choices"][0]["message"]["content"])

        function_name, args_str = extract_function_details_from_response(response)
        if not function_name:
            print("No function found in the response.")
            #message = "It appears the final report has finished - Please provide a short overview with the format of the penetration test"
            #response = request_openai_response(message, functions)
            #display_response(response["choices"][0]["message"]["content"])
            # Handle this case as you see fit, maybe continue to the next iteration or break out of the loop
            break
        
        function_args = parse_args(args_str)

        # Check if the function exists in the dictionary before calling it
        if function_name in available_functions:
            # Ensure args_str is safely converted to a dictionary
            try:
                function_response = available_functions[function_name](**function_args)
                print(f"Function Response: {json.dumps(function_response, indent=4)}")
                update_state(function_name, function_response, state)
                functions_run.append(function_name)
            except Exception as e:
                print(f"{RED_COLOR}Error while parsing arguments or executing function: {e}{RESET_COLOR}")
        else:
            print(f"{RED_COLOR}Function '{function_name}' does not exist! Please check the suggestion.{RESET_COLOR}")

    display_final_logs(state)

# 3. API Key and Execution
openai.api_key = load_api_key_from_file()
run_pentest()
