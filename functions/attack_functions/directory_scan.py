import random

def directory_scan(urls=None, subdomains=None):
    print(f"\033[91mDirectory Traversal Check called by ChatGPT\033[0m")
    
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
    
    # Realistic potentially vulnerable directories and files
    vulnerable_directories = [
        "/admin/backups/",
        "/uploads/files/",
        "/conf/config.php~",
        "/logs/access.log",
        "/.git/config",
        "/.htaccess",
        "/db/database.sql",
        "/backup.tar.gz",
        "/wp-config.php~",
        "/.env"
    ]

    # Non-vulnerable or realistic directories
    safe_directories = [
        "/assets/img/",
        "/js/lib/",
        "/css/",
        "/contact/",
        "/api/v1/products/",
        "/docs/",
        "/about/",
        "/user/settings/",
        "/img/header/",
        "/downloads/software/"
    ]
    
    all_scan_results = {}
    vulnerable_found = False  # Flag to track if a vulnerable directory has been found
    
    for target in targets:
        # If a vulnerable directory was found in a previous scan, decrease its likelihood for subsequent scans
        if vulnerable_found:
            vulnerable_weight = 0
        else:
            vulnerable_weight = 1

        # Select a random number of directories/files to be exposed
        num_to_expose = random.randint(1, 4)
        random_directories = random.choices(
            vulnerable_directories + safe_directories,
            weights=[vulnerable_weight] * len(vulnerable_directories) + [5] * len(safe_directories),
            k=num_to_expose
        )
        random_directories = list(set(random_directories))  # Remove duplicates

        # Check if any of the selected directories are vulnerable
        for dir in random_directories:
            if dir in vulnerable_directories:
                vulnerable_found = True
                break
        
        # Construct message based on exposed directories
        if len(random_directories) == 1:
            message = f"Potential directory found at {target}{random_directories[0]}"
        else:
            message = f"Directories found on {target}:\n" + "\n".join([f"{target}{dir}" for dir in random_directories])
        
        all_scan_results[target] = message
    
    return {
        "potential": all_scan_results
    }
