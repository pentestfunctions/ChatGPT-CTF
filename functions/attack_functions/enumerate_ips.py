import random

def enumerate_ips(domain=None, subdomain=None):
    print("\033[91mEnumerate IPs called by ChatGPT\033[0m")
    
    target = subdomain if subdomain else domain
    ips = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    return {
        "target": target,
        "ips": [ips]
    }