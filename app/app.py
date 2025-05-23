# This function accepts an IP address from the URL, pings that IP from the server,
# and returns the ping result as formatted HTML. Vulnerable to command injection.

from flask import Flask, request  # Import Flask framework and request object for handling incoming data

app = Flask(__name__)  # Create a Flask app instance

@app.route("/")  # Define the default route for homepage
def home():
    return "Welcome to the intentionally vonurable cloud security pipeline"  # Return a message

# Define a second route at /ping — intentionally insecure
@app.route("/ping")
def ping():
    import os  # Import OS python module to run cmd on OS
    # Get the 'ip' value from the URL query (e.g. /ping?ip=1.2.3.4)
    # If no IP is given, use the default: 8.8.8.8
    ip = request.args.get("ip", "8.8.8.8")
    
    # Vulnerability: passes user input directly to the shell — command injection
    output = os.popen(f"ping -c 1 {ip}").read()  # Run 'ping' command with user injected IP and read commands output
    return f"<pre>{output}</pre>"  # Show the ping output in formatted HTML block

if __name__ == "__main__":  # If this file runs directly
    app.run(host="0.0.0.0", port=5000)  # Start the app, accessible on all networks at port 5000
