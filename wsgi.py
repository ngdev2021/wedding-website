#!/usr/bin/env python3
"""
WSGI entry point for the wedding website backend.
This file is used by production WSGI servers like Gunicorn or uWSGI.
"""

from app import app

if __name__ == "__main__":
    app.run() 