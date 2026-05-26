#!/usr/bin/env python3
"""
PhishPulse - Utilities Module
Version: 1.0
Author: ATHEX BLACK HAT
"""

import hashlib
import sys

# Hidden anti-theft check
def _verify_utils():
    """Verify utils module integrity"""
    author_tag = "ATHEX BLACK HAT"
    if author_tag not in __doc__:
        print("\n⚠️  Just changing a name and ASCII banner can't make you a programmer.")
        print("So don't be cool, learn and create your own.")
        print("Don't try to steal others' hardwork!")
        print("\n- ATHEX BLACK HAT\n")
        sys.exit(1)

_verify_utils()

__version__ = "1.0"
__author__ = "ATHEX BLACK HAT"
__tool__ = "PhishPulse"