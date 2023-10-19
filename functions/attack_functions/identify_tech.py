import random

def identify_tech(domains=None, subdomains=None):
    print(f"\033[91mIdentify Tech called by ChatGPT\033[0m")
    
    # Handle multiple targets similarly to the port_scan function
    targets = []
    
    if domains:
        if isinstance(domains, str):
            targets.append(domains)
        elif isinstance(domains, list):
            targets.extend(domains)
    
    if subdomains:
        if isinstance(subdomains, str):
            targets.append(subdomains)
        elif isinstance(subdomains, list):
            targets.extend(subdomains)
    
    # Ensure that targets are unique
    targets = list(set(targets))
    
    all_tech_results = {}
    for target in targets:
        tech_info = random.choice(["[200] Server: Apache", "[200] Server: Nginx", "[200] Tech: WordPress", "[200] Tech: Joomla", "[200] Tech: React", "[200] Tech: Vue"])
        
        # Use existing logic to format the tech info for the target
        if ' - ' in tech_info:
            tech_info = f"[200] https://{target} - {tech_info.split(' - ')[1]}"
        else:
            tech_info = f"[200] https://{target} - {tech_info.split(': ')[1]}"
        
        all_tech_results[target] = tech_info
    
    return {
        "tech": all_tech_results
    }