#!/usr/bin/env python3
#Main

"""Main."""

import sys
import os
from cpu import *

# if len('/Users/megan/Documents/school/CS21/projects/Computer-Architecture/ls8/examples/call.ls8') == 2:
path = os.path.dirname(os.path.abspath('/Users/megan/Documents/school/CS21/projects/Computer-Architecture/ls8/examples/call.ls8'))

cpu = CPU()

cpu.load()
cpu.run()
# else:
#     print("Please provide filename to execute instrustions")
#     sys.exit(1)