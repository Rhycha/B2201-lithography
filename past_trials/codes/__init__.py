import sys
import os
fDir= os.path.dirname(__file__)
print(fDir)
sys.path.append(fDir)

print("Hello from __init__!")
from LITHO_package import *
