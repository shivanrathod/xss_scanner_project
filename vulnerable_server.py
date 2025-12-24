from flask import Flask, request

app = Flask(__name__)

# Ye code jaan-boojh kar vulnerable banaya gaya hai practice ke liye.
# Real world mein hum templates use karte hain, f-strings nahi.

@app.route('/')
def home():
    return """
    <h1>Vulnerable XSS Lab</h1>
    <p>Welcome! Try attacking these pages:</p>
    <ul>
        <li><a href='/text_node?q=hello'>Text Node Injection</a></li>
        <li><a href='/attribute_value?q=hello'>Attribute Value Injection</a></li>
        <li><a href='/attribute_name?q=test'>Attribute Name Injection</a></li>
    </ul>
    """

# Scenario 1: Text Node (Sabse common)
# Injection yahan hoti hai: <div> USER_INPUT </div>
@app.route('/text_node')
def text_node():
    q = request.args.get('q', '')
    # Galti: Input ko bina filter kiye seedha HTML mein daal diya
    return f"<html><body><h1>Search Results</h1><div>You searched for: {q}</div></body></html>"

# Scenario 2: Attribute Value
# Injection yahan hoti hai: <input value="USER_INPUT">
@app.route('/attribute_value')
def attr_value():
    q = request.args.get('q', '')
    # Galti: Input input tag ke value attribute mein ja raha hai
    return f"<html><body><h1>Login</h1><input type='text' value='{q}'></body></html>"

# Scenario 3: Attribute Name (Jo Assignment mein specifically manga hai)
# Injection yahan hoti hai: <div USER_INPUT="something">
@app.route('/attribute_name')
def attr_name():
    q = request.args.get('q', 'class')
    # Galti: Input attribute ka NAAM ban raha hai
    return f"<html><body><h1>Custom Div</h1><div {q}='highlight'>This is a div</div></body></html>"

if __name__ == '__main__':
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)