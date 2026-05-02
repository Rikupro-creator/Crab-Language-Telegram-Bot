#!/usr/bin/env python3
"""
Simple runner script for Crab Language Bot
Edit config.py with your tokens, then run this script
"""

# Import config first to set environment variables
import config

# Now import and run the bot
from crab import main

if __name__ == '__main__':
    # Tokens are already set in os.environ by config.py
    main()