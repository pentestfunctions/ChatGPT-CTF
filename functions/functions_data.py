functions = [
    {
        "name": "enumerate_ips",
        "description": "Mocks the retrieval of IPs for a domain",
        "parameters": {
            "type": "object",
            "properties": {
                "subdomain": {"type": "string"}
            },
            "required": ["domain"]
        }
    },
    {
        "name": "identify_tech",
        "description": "Mocks the identification of the technology stack of a domain or subdomain",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of domains to identify tech. Can be a single domain or multiple domains."
                },
                "subdomains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of subdomains to identify tech. Can be a single subdomain or multiple subdomains."
                }
            },
            "minProperties": 1,
            "additionalProperties": False,
            "description": "At least one of 'domains' or 'subdomains' should be provided."
        }
    },
    {
        "name": "enumerate_subdomains",
        "description": "Mocks the discovery of subdomains of a domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {"type": "string"}
            },
            "required": ["domain"]
        }
    },
    {
        "name": "port_scan",
        "description": "Mocks a port scan on one or more domains or subdomains",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of domains to scan. Can be a single domain or multiple domains."
                },
                "subdomains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of subdomains to scan. Can be a single subdomain or multiple subdomains."
                }
            },
            "minProperties": 1,
            "additionalProperties": False,
            "description": "At least one of 'domains' or 'subdomains' should be provided."
        }
    },
    {
        "name": "sql_injection_simulation",
        "description": "Mocks an SQL injection attack simulation on one or more domains or subdomains",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of domains to simulate the attack on. Can be a single domain or multiple domains."
                },
                "subdomains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of subdomains to simulate the attack on. Can be a single subdomain or multiple subdomains."
                }
            },
            "minProperties": 1,
            "additionalProperties": False,
            "description": "At least one of 'domains' or 'subdomains' should be provided."
        }
    },
    {
        "name": "check_ssl_vulnerability",
        "description": "Mocks an SSL vulnerability check on one or more domains or subdomains",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of domains to check. Can be a single domain or multiple domains."
                },
                "subdomains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of subdomains to check. Can be a single subdomain or multiple subdomains."
                }
            },
            "minProperties": 1,
            "additionalProperties": False,
            "description": "At least one of 'domains' or 'subdomains' should be provided."
        }
    },
    {
        "name": "directory_scan",
        "description": "Mocks a directory traversal vulnerability check on one or more URLs or subdomains",
        "parameters": {
            "type": "object",
            "properties": {
                "urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of URLs to check. Can be a single URL or multiple URLs."
                },
                "subdomains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of subdomains to check. Can be a single subdomain or multiple subdomains."
                }
            },
            "minProperties": 1,
            "additionalProperties": False,
            "description": "At least one of 'urls' or 'subdomains' should be provided."
        }
    }
]

