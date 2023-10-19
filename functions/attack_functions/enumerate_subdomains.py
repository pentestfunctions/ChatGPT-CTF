import random

# Section 1: Mock Penetration Testing Functions
def enumerate_subdomains(domain):
    print(f"\033[91mEnumerate Subdomains called by ChatGPT\033[0m")
    subs = ["blog", "dev", "shop", "admin", "api"]
    return {
        "subdomains": [f"{sub}.{domain}" for sub in random.sample(subs, random.randint(2, 5))]  # Randomize the number and type of subdomains
    }