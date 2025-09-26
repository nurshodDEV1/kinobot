#!/usr/bin/env python3
import sys
import os

print("Python version:", sys.version)
print("Python path:", sys.executable)

# Check if required environment variables are set
bot_token = os.getenv('BOT_TOKEN')
if bot_token:
    print("BOT_TOKEN is set (first 10 chars):", bot_token[:10])
else:
    print("BOT_TOKEN is not set")

port = os.getenv('PORT')
if port:
    print("PORT is set:", port)
else:
    print("PORT is not set")

print("All environment variables:")
for key, value in os.environ.items():
    if 'BOT' in key or 'PORT' in key:
        print(f"  {key}: {value}")