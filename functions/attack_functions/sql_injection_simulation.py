import random

def sql_injection_simulation(urls=None, subdomains=None):
    print(f"\033[91mSQL Injection Simulation called by ChatGPT\033[0m")

    targets = []

    if urls:
        if isinstance(urls, str):  # If only one URL is given as a string
            targets.append(urls)
        elif isinstance(urls, list):  # If multiple URLs are given as a list
            targets.extend(urls)

    if subdomains:
        if isinstance(subdomains, str):  # If only one subdomain is given as a string
            targets.append(subdomains)
        elif isinstance(subdomains, list):  # If multiple subdomains are given as a list
            targets.extend(subdomains)

    # Ensure that targets are unique
    targets = list(set(targets))

    # Predefined list of potential vulnerable endpoints
    endpoints = [
        "login.php",
        "search.php",
        "user-profile.php",
        "checkout.php",
        "product-details.php",
        "feedback.php"
    ]

    sqli_types = {
        "Blind SQL Injection detected": "/{} Blind SQL Injection vulnerability detected.",
        "Time-based Blind SQL Injection detected": "/{} Time-based Blind SQL Injection vulnerability detected.",
        "Error-based SQL Injection detected": "/{} Error-based SQL Injection vulnerability detected.",
        "UNION-based SQL Injection detected": "/{} UNION-based SQL Injection vulnerability detected."
    }

    other_outcomes = {
        "No vulnerability detected": "/{} No SQL injection vulnerability detected.",
        "Potential vulnerability, needs manual verification": "/{} Potential SQL injection vulnerability detected. Manual verification required."
    }

    # Combine all potential outcomes
    combined_outcomes = {**sqli_types, **other_outcomes}

    all_simulations = {}

    for target in targets:
        endpoint = random.choice(endpoints)
        outcome_message = combined_outcomes[random.choice(list(combined_outcomes.keys()))].format(endpoint)
        all_simulations[target] = f"[{target}{outcome_message}]"

    return {
        "vulnerabilities": all_simulations
    }
