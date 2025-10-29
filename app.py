from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
import time
from threading import Thread
from instagrapi import Client

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global variables for managing stop functionality
stop_flag = False

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="haters_name">Hater's Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="group_ids">Target Group IDs (comma-separated):</label>
            <input type="text" id="group_ids" name="group_ids" placeholder="Enter group IDs (e.g., 123,456,789)" required>

            <label for="message_file">Message File (TXT):</label>
            <input type="file" id="message_file" name="message_file" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

            <button type="submit">Start Messaging</button>
        </form>
        <form action="/stop" method="POST" style="margin-top: 10px;">
            <button type="submit" style="background-color: #e74c3c;">Stop Messaging</button>
        </form>
    </div>
</body>
</html>
'''

# Route to render form and handle messaging
@app.route("/", methods=["GET", "POST"])
def send_messages():
    global stop_flag
    if request.method == "POST":
        # Fetch form data
        username = request.form["username"]
        password = request.form["password"]
        haters_name = request.form["haters_name"]
        group_ids = request.form["group_ids"].split(",")
        delay = int(request.form["delay"])
        message_file = request.files["message_file"]

        # Read messages from the uploaded file
        try:
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("send_messages"))
        except Exception as e:
            flash(f"Error reading message file: {e}", "error")
            return redirect(url_for("send_messages"))

        # Start messaging in a separate thread
        def message_sender():
            global stop_flag
            try:
                # Log in to Instagram
                client = Client()
                client.login(username, password)
                flash("Logged in successfully!", "success")

                for group_id in group_ids:
                    for message in messages:
                        if stop_flag:
                            print("[INFO] Messaging stopped by user.")
                            return
                        try:
                            # Send message to group
                            client.direct_send(f"{haters_name}: {message}", thread_id=group_id)
                            print(f"[SUCCESS] Sent to group {group_id}: {message}")
                        except Exception as e:
                            print(f"[ERROR] Failed to send to group {group_id}: {e}")
                        time.sleep(delay)

                flash("All messages sent successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "error")

        # Start the thread
        stop_flag = False
        Thread(target=message_sender).start()
        return redirect(url_for("send_messages"))

    return render_template_string(HTML_TEMPLATE)

# Route to stop messaging
@app.route("/stop", methods=["POST"])
def stop_messaging():
    global stop_flag
    stop_flag = True
    flash("Messaging process stopped!", "success")
    return redirect(url_for("send_messages"))

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
                  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #1abc9c;
        }
        label {
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        input, select {
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        button {
            background-color: #1abc9c;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #16a085;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: #1abc9c;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="choice">Send To:</label>
            <select id="choice" name="choice" required>
                <option value="group">Group Chats</option>
                <option value="inbox">Inbox</option>
            </select>

            <label for="target_ids">Target IDs (comma-separated):</label>
            <input type="text" id="target_ids" name="target_ids" placeholder="Enter group IDs or usernames" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
        <form action="/stop" method="POST">
            <button class="stop-button" type="submit">Stop Sending</button>
        </form>
    </div>
</body>
</html>
'''

# Function to send messages
def send_messages(username, password, target_ids, messages, choice, delay):
    global stop_flag
    stop_flag = False
    try:
        cl = Client()
        print("[INFO] Logging into Instagram...")
        cl.login(username, password)
        print("[SUCCESS] Logged in!")

        targets = target_ids.split(",")

        for target in targets:
            if stop_flag:
                print("[INFO] Sending stopped by user.")
                break

            for message in messages:
                if stop_flag:
                    print("[INFO] Sending stopped by user.")
                    break

                if choice == "group":
                    print(f"[INFO] Sending to group {target.strip()}: {message}")
                    cl.direct_send(message, thread_ids=[target.strip()])
                elif choice == "inbox":
                    print(f"[INFO] Sending to user {target.strip()}: {message}")
                    cl.direct_send(message, usernames=[target.strip()])

                print("[SUCCESS] Message sent.")
                time.sleep(delay)

        if not stop_flag:
            print("[INFO] All messages sent successfully!")

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

# Flask route for sending messages
@app.route("/", methods=["GET", "POST"])
def instagram_messenger():
    if request.method == "POST":
        global stop_flag
        stop_flag = False
        try:
            # Form data
            username = request.form["username"]
            password = request.form["password"]
            choice = request.form["choice"]
            target_ids = request.form["target_ids"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("instagram_messenger"))

            # Start sending in a background thread
            threading.Thread(target=send_messages, args=(username, password, target_ids, messages, choice, delay)).start()
            flash("Messages are being sent in the background!", "success")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
    
    return render_template_string(HTML_TEMPLATE)

# Flask route to stop sending
@app.route("/stop", methods=["POST"])
def stop_sending():
    global stop_flag
    stop_flag = True
    flash("Message sending stopped.", "info")
    return redirect(url_for("instagram_messenger"))

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)        h1 {
            text-align: center;
            color: #61dafb;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
            color: #61dafb;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, select:focus, button:focus {
            outline: none;
            border-color: #61dafb;
            box-shadow: 0 0 5px rgba(97, 218, 251, 0.5);
        }
        button {
            background-color: #61dafb;
            color: #282c34;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #21a1f1;
        }
        .message {
            text-align: center;
            font-size: 14px;
            margin-top: 10px;
        }
        .success {
            color: #4caf50;
        }
        .error {
            color: #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Target Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter target group chat ID" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Login and send messages
@app.route("/", methods=["GET", "POST"])
def instagram_messenger():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate and read message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("instagram_messenger"))

            # Initialize Instagram client
            cl = Client()
            print("[INFO] Logging in...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Send messages to group chat
            for message in messages:
                print(f"[INFO] Sending message to group {group_id}: {message}")
                cl.direct_send(message, thread_ids=[group_id])
                print(f"[SUCCESS] Message sent: {message}")
                time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("instagram_messenger"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("instagram_messenger"))

    # Render form
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
              
