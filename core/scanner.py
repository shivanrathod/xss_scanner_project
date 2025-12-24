import requests
from colorama import Fore, Style
from core.generator import PayloadGenerator

class XSSScanner:
    def __init__(self, cookies=None):
        self.generator = PayloadGenerator()
        self.session = requests.Session()
        
        # Set authentication cookies if provided
        if cookies:
            self.session.cookies.update(cookies)
        
        # Set a standard User-Agent to bypass basic bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scan(self, url, param_name):
        """
        Injects payloads into the specified parameter and checks for reflection.
        """
        print(f"{Fore.CYAN}[*] Scanning URL: {url} | Parameter: {param_name}{Style.RESET_ALL}")
        
        contexts = ['text_node', 'attribute_value', 'attribute_name']
        vulnerabilities = []

        for context in contexts:
            payloads = self.generator.generate_payloads(context)
            
            for payload in payloads:
                try:
                    # Construct request with payload
                    params = {param_name: payload}
                    
                    # Execute GET request
                    response = self.session.get(url, params=params)
                    
                    # Detection: Check if the sentinel (canary) is reflected in the response
                    if self.generator.get_canary() in response.text:
                        print(f"{Fore.GREEN}[+] VULNERABILITY FOUND!{Style.RESET_ALL}")
                        print(f"    Context: {context}")
                        print(f"    Payload: {payload}")
                        
                        vulnerabilities.append({
                            'url': url,
                            'context': context,
                            'payload': payload
                        })
                        
                except requests.RequestException as e:
                    print(f"{Fore.RED}[!] Network error: {e}{Style.RESET_ALL}")

        return vulnerabilities