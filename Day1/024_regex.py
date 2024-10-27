import re

text = """
device = ETH0123, ip=192.168.1.122, status=UP
system=MMI301U, ip=192.168.1.123, status=DOWN
device=ETH0124, ip=192.168.1.212, status=UP
router=RT01, ip=192.168.1.191, status=UP
"""

regexp = r'(?:device\s*=\s*|system\s*=\s*|router\s*=\s*)([0-9A-Z]+)'
matches = re.findall(regexp, text)
print(matches)