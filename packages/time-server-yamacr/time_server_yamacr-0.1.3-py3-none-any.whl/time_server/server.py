from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def get_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Current Time</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { background: #f4f4f4; padding: 20px; border-radius: 10px; display: inline-block; }
                h1 { color: #333; }
                p { font-size: 24px; color: #555; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Current Time</h1>
                <p>{{ current_time }}</p>
            </div>
        </body>
        </html>
        """
    return render_template_string(html_template, current_time=current_time)

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
