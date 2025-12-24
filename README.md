# Custom Context-Aware Reflected XSS Scanner

A modular, Python-based security tool designed to detect Reflected Cross-Site Scripting (XSS) vulnerabilities. Unlike basic scanners, this tool intelligently adapts its payloads based on the injection context (HTML Text, Attribute Value, and Attribute Name).

## 🚀 Key Features

* **Context-Aware Payloads:** Automatically generates specific payloads for:
    * **Text Nodes:** (e.g., `<div>INPUT</div>`)
    * **Attribute Values:** (e.g., `<input value="INPUT">`) - Breaks out of quotes.
    * **Attribute Names:** (e.g., `<div INPUT="value">`) - Injects event handlers like `onanimationstart`.
* **Authenticated Scanning:** Supports Session Cookies via CLI to scan pages behind login screens.
* **Canary-Based Detection:** Uses a unique random token (`XSS_TEST_123`) to confirm reflection with high accuracy, minimizing false positives.
* **Reporting:** Generates a clean HTML report (`report.html`) and provides colored terminal output.
* **Modular Architecture:** Logic is separated into Generator, Scanner, and Reporter modules for scalability.

## 📂 Project Structure

```text
xss_scanner_project/
│
├── core/                   # The Core Engine
│   ├── generator.py        # Logic: Decides WHICH payload to use based on context
│   ├── scanner.py          # Logic: Sends requests and detects "Canary" reflection
│   └── reporter.py         # Logic: Generates the HTML report
│
├── main.py                 # CLI Entry Point (The Commander)
├── vulnerable_server.py    # A local Flask server to test the scanner (Proof of Concept)
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## Setup & Installation:
Prerequisites: Python 3.x

1. **Install Dependencies:**
```
    pip install -r requirements.txt
```
3. **Start the Vulnerable Lab Server (Optional for testing): Open a terminal and run:**  
```
    python vulnerable_server.py
```
-The server will run on http://127.0.0.1:5000.

## Usage:   
Run the scanner by providing the Target URL and the Parameter to test. 

**1. Basic Scan:**
python main.py -u [http://127.0.0.1:5000/text_node](http://127.0.0.1:5000/text_node) -p q

**2. POST Request Scan:**
```
python main.py -u [http://127.0.0.1:5000/text_node](http://127.0.0.1:5000/text_node) -p q -m POST
```
**3. Authenticated Scan (with Cookies):**
```
python main.py -u [http://127.0.0.1:5000/profile](http://127.0.0.1:5000/profile) -p name --cookie "session_id=12345; user=admin"
```

**Command Line Arguments**
```
-u, --url: (Required) The target URL.
-p, --param: (Required) The GET parameter to inject payload into.
-c, --cookie: Session cookies for authenticated scanning.
-m, --method: HTTP Method: GET (default) or POST.
```

## Logic & Design Choices:

**1. Payload Generator (core/generator.py):**
I implemented a PayloadGenerator class to handle the requirement of "adapting payloads based on position".

- Logic: It accepts a context argument.

   - If context is attribute_name: It injects style=animation-name:rotation onanimationstart=alert(1) because standard <script> tags won't work inside a tag definition.
    
   - If context is attribute_value: It prioritizes closing the quote (") first.

- Design Choice: Separating this into a class allows easy addition of new contexts (e.g., JSON or JavaScript contexts) in the future without breaking the scanner logic.

**2. Detection Approach:**
Instead of using a heavy headless browser to check for JavaScript execution, I used a Canary (Sentinel Value) approach.

   - The generator embeds a unique string (XSS_TEST_123) in every payload.

   - The scanner checks if canary in response.text.

   - Assumption: If the server reflects the payload characters (like < > " ') and the unique token without encoding/sanitization, the endpoint is vulnerable.

**3. Why Modular?**    
I avoided writing a single-file script. By using a package structure (core/), the code is cleaner, easier to debug, and represents a production-ready software engineering approach.

## Time Spent:
Total Time: ~5 Hours

   - Research (1 Hour): Specifically researching Attribute Name injection vectors and bypass techniques.

   - Core Development (2.5 Hours): Implementing the Generator, Scanner, and Reporter classes.

   - Lab & Testing (1.5 Hours): Building the vulnerable_server.py, debugging edge cases, and finalizing the CLI arguments.
