"""
This script runs the Askmate application using a development server.
"""

from os import environ
from Askmate import app

if __name__ == "__main__":
    HOST = environ.get("SERVER_HOST", "localhost")
    PORT = 5555
    from waitress import serve
    serve(app, host="0.0.0.0", port=5555)
