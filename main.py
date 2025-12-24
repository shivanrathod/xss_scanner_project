import argparse
from colorama import init, Fore
from core.scanner import XSSScanner
from core.reporter import HTMLReporter

# Initialize colorama for Windows terminal support
init()

def parse_cookies(cookie_string):
    """Parses a cookie string (key=value; key2=val2) into a dictionary."""
    cookies = {}
    if cookie_string:
        for item in cookie_string.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies[key] = value
    return cookies

def main():
    # Setup CLI arguments
    parser = argparse.ArgumentParser(description="Custom Context-Aware Reflected XSS Scanner")
    
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    parser.add_argument("-p", "--param", help="Vulnerable parameter name", required=True)
    parser.add_argument("-c", "--cookie", help="Session cookies (e.g., 'session=123')", required=False)
    
    args = parser.parse_args()

    # Parse optional cookies
    cookies = parse_cookies(args.cookie)

    print(f"{Fore.YELLOW}=== Starting XSS Scanner ==={Fore.RESET}")
    if cookies:
        print(f"{Fore.CYAN}[*] Authenticated Scan Enabled.{Fore.RESET}")

    # Initialize and run scanner
    scanner = XSSScanner(cookies=cookies)
    vulnerabilities = scanner.scan(args.url, args.param)

    # Generate Report
    reporter = HTMLReporter()
    reporter.generate_report(vulnerabilities)

    print(f"{Fore.YELLOW}=== Scan Finished ==={Fore.RESET}")

if __name__ == "__main__":
    main()