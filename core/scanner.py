import requests
from colorama import Fore, Style
from core.generator import PayloadGenerator

class XSSScanner:
    """
    Core Scanner Class.
    Responsible for sending payloads to the target and detecting reflections.
    """
    def __init__(self, cookies=None):
        self.generator = PayloadGenerator()
        self.session = requests.Session()
        
        # If cookies are provided, add them to the session for authenticated scanning
        if cookies:
            self.session.cookies.update(cookies)
        
        # Set a standard User-Agent to bypass basic bot detection logic
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scan(self, url, param_name, method="GET"):
        """
        Scans a specific parameter on the target URL for XSS vulnerabilities.
        
        Args:
            url (str): The target URL.
            param_name (str): The parameter to inject payloads into.
            method (str): HTTP Method (GET or POST).
            
        Returns:
            list: A list of dictionaries containing details of found vulnerabilities.
        """
        print(f"{Fore.CYAN}[*] Scanning URL: {url} | Parameter: {param_name} | Method: {method}{Style.RESET_ALL}")
        
        # Requirement: Handle at least 3 injection contexts
        contexts = ['text_node', 'attribute_value', 'attribute_name']
        vulnerabilities = []

        for context in contexts:
            # Generate context-specific payloads (e.g., closing quotes for attributes)
            payloads = self.generator.generate_payloads(context)
            
            for payload in payloads:
                try:
                    target_url = url
                    payload_data = {param_name: payload}
                    
                    # Requirement: Support GET and POST
                    if method.upper() == "POST":
                        # For POST, data goes in the body
                        response = self.session.post(target_url, data=payload_data)
                    else:
                        # For GET, data goes in URL parameters
                        response = self.session.get(target_url, params=payload_data)
                    
                    # Detection Logic: Check if the unique 'Canary' token is present in the response
                    canary = self.generator.get_canary()
                    
                    if canary in response.text:
                        print(f"{Fore.GREEN}[+] VULNERABILITY FOUND!{Style.RESET_ALL}")
                        print(f"    Context: {context}")
                        print(f"    Payload: {payload}")
                        
                        vulnerabilities.append({
                            'url': url,
                            'context': context,
                            'payload': payload,
                            'method': method
                        })
                        
                except Exception as e:
                    print(f"{Fore.RED}[!] Error connecting to {url}: {e}{Style.RESET_ALL}")

        return vulnerabilities
