from flask import Flask, request

app = Flask(__name__)

# Vulnerable Lab Server for XSS Scanner Testing
# WARNING: This code is intentionally vulnerable. Do not run in production.

@app.route('/')
def home():
    return """
    <h1>Vulnerable XSS Lab</h1>
    <p>Target Endpoints:</p>
    <ul>
        <li><a href='/text_node?q=test'>Text Node Injection</a></li>
        <li><a href='/attribute_value?q=test'>Attribute Value Injection</a></li>
        <li><a href='/attribute_name?q=test'>Attribute Name Injection</a></li>
    </ul>
    """

# Context 1: HTML Text Node Injection
# Vulnerability: User input is reflected directly between tags
@app.route('/text_node')
def text_node():
    q = request.args.get('q', '')
    return f"<html><body><h1>Search Results</h1><div>You searched for: {q}</div></body></html>"

# Context 2: Attribute Value Injection
# Vulnerability: User input is reflected inside an attribute's quoted value
@app.route('/attribute_value')
def attr_value():
    q = request.args.get('q', '')
    return f"<html><body><h1>Login</h1><input type='text' value='{q}'></body></html>"

# Context 3: Attribute Name Injection
# Vulnerability: User input is reflected as an attribute name
@app.route('/attribute_name')
def attr_name():
    q = request.args.get('q', 'class')
    return f"<html><body><h1>Custom Div</h1><div {q}='highlight'>This is a div</div></body></html>"

if __name__ == '__main__':
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
