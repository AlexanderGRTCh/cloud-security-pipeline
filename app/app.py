from flask import Flask, request, jsonify
# This function accepts an IP address from the URL, pings that IP from the server,
# and returns the ping result as formatted HTML. Vulnerable to command injection..

app = Flask(__name__)  # Create a Flask app instance

@app.route("/")  # Define the default route for homepage
def home():
    return "Welcome to the intentionally vonurable cloud security pipeline"  

# Define a second route at /ping — intentionally insecure
@app.route("/ping")
def ping():
    import os  # Import OS python module to run cmd on OS
    # Get the 'ip' 
    # If no IP, use the default: 8.8.8.8
    ip = request.args.get("ip", "8.8.8.8")
    
    # Vulnerability: passes user input directly to the shell — command injection
    output = os.popen(f"ping -c 1 {ip}").read()  # Run 'ping' command with user injected IP and read commands output
    return f"<pre>{output}</pre>"  # Show the ping output in formatted HTML block

if __name__ == "__main__":  # If this file runs directly
    app.run(host="0.0.0.0", port=5000)  # Start the app, accessible on all networks at port 5000

# In-memory "database"-list of mock threat entries
threats = [
    {"id": 1, "type": "malware", "severity": "high"},
    {"id": 2, "type": "phishing", "severity": "medium"}
]

# Define a REST API endpoint at /api/threat, allows GET (read) and POST (add)
@app.route("/api/threat", methods=["GET", "POST"])
def api_threat():
    if request.method == "GET":  # If client requests data (GET)
        return jsonify(threats)  # Return list of threats as JSON

    if request.method == "POST":  # If client sends new data (POST)
        data = request.get_json()    # Parse incoming JSON from request body
        data["id"] = len(threats) + 1  # Assign unique id to new threat
        threats.append(data)  # Add new threat to the list
        return jsonify(data), 201  # Return added data and status 201
