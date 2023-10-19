# ChatGPT-powered CTF Penetration Tester

This script is a proof of concept that uses OpenAI's ChatGPT to perform penetration testing tasks in an attempt to identify potential vulnerabilities in a domain. The purpose is to use ChatGPT to automate certain CTF (Capture The Flag) challenges by leveraging the AI's ability to make decisions based on the results of executed functions. It uses fully mock data to not attack real world targets allowing for weighted output for infinite possibilities.

- I would like in the future to automate the subdomain identification into the port scan and service scan (using mock HTTPx or whatweb style data for each subdomain/webservice port) before the ChatGPT function begins as those should be standard practice and give ChatGPT a starting point without wasting requests or potentially falling into a loop. (So subdomain scan into port scan on each subdomain into whatweb/httpx on each subdomain and webserver port identified to find alternative webservers) 

## Features
- Utilizes various functions to perform common penetration testing tasks.
- Keeps track of the state to ensure that functions aren't repeatedly executed on the same domain or subdomain.
- Aims to identify just 1 vulnerable path or service.
- If a vulnerability is found, the automated testing is stopped.

## Important Notes
- **Ethical Use**: This script should only be used for ethical purposes. Ensure that you have proper permission to perform any tests.
- **Limitation**: The current implementation only allows ChatGPT to suggest and run one function at a time.

## Functionality Overview
- Enumerate IPs
- Check SSL Vulnerability (weighted to 95, 2.5, 2.5 FOR none, heartbleed, poodle)
- Directory Scan (weighted to find at most ONE potentially exposing directory/file across all subdomains)
- Enumerate Subdomains
- Identify Tech
- Port Scan (weighted to fit a more realistic range of vulnerable versions being less likely and follow the port structure already identified by other domains)
- SQL Injection Simulation
- ... and more!

## Usage

1. Ensure that you have the required libraries installed. This script utilizes the `openai` library among others.
2. Update your OpenAI API key in the `functions.handling_info.load_api_key_from_file` method.
3. Run the main script to start the automated penetration testing process guided by ChatGPT.

## Contribution

Contributions are welcome! If you have additional functions or improvements you'd like to add, feel free to submit a pull request.

## Disclaimer

This is a proof of concept. Always ensure you have the proper permissions to perform penetration testing. Misuse can lead to legal repercussions.


