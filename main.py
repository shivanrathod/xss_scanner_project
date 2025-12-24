import argparse
from colorama import init, Fore
from core.scanner import XSSScanner
from core.reporter import HTMLReporter

# Initialize colorama for cross-platform colored output
init()

def parse_cookies(cookie_string):
    """
    Parses a raw cookie string (e.g., "id=123; session=abc") into a dictionary.
    Required for the requests library to handle authenticated sessions.
    """
    cookies = {}
    if cookie_string:
        for item in cookie_string.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies[key] = value
    return cookies

def main():
    """
    Main entry point for the XSS Scanner CLI tool.
    Handles argument parsing, scanner initialization, and reporting.
    """
    # 1. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="Custom Reflected XSS Scanner Tool")
    
    parser.add_argument("-u", "--url", help="Target URL (e.g., http://example.com/search)", required=True)
    parser.add_argument("-p", "--param", help="Parameter to test (e.g., q, search, query)", required=True)
    parser.add_argument("-c", "--cookie", help="Custom cookies for authenticated scans (e.g., 'session_id=xyz')", required=False)
    # Requirement: Support for both GET and POST methods
    parser.add_argument("-m", "--method", help="HTTP Method to use: GET or POST", default="GET", choices=["GET", "POST"])
    
    args = parser.parse_args()

    # 2. Process Inputs
    cookies = parse_cookies(args.cookie)

    print(f"{Fore.YELLOW}=== Starting XSS Scanner ==={Fore.RESET}")
    print(f"[*] Target: {args.url}")
    print(f"[*] Method: {args.method}")
    
    if cookies:
        print(f"[*] Loaded Cookies: {cookies}")

    # 3. Initialize Scanner Engine
    # Injecting cookies to handle authentication requirements
    scanner = XSSScanner(cookies=cookies)
    
    # 4. Start the Scan
    # The scanner will iterate through multiple contexts (Text, Attribute, etc.)
    vulnerabilities = scanner.scan(args.url, args.param, method=args.method)

    # 5. Generate Report
    reporter = HTMLReporter()
    reporter.generate_report(vulnerabilities)

    print(f"{Fore.YELLOW}=== Scan Finished ==={Fore.RESET}")

if __name__ == "__main__":
    main()
