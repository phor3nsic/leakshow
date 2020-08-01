import requests
import argparse
import sys

from bs4 import BeautifulSoup

banner = """
   __            _     __ _                   
  / /  ___  __ _| | __/ _\ |__   _____      __
 / /  / _ \/ _` | |/ /\ \| '_ \ / _ \ \ /\ / /
/ /__|  __/ (_| |   < _\ \ | | | (_) \ V  V / 
\____/\___|\__,_|_|\_\\__/_| |_|\___/ \_/\_/  
                                              
			by phor3nsic
"""

parser = argparse.ArgumentParser(description='Check Leaks for domains and users!', add_help=True)
parser.add_argument("-d", "--domain", help="Domain check")
parser.add_argument("-n", "--name", help="Name check")
args = parser.parse_args()

URL = "http://pwndb2am4tzkvold.onion/"
SESSION = requests.session()
SESSION.proxies = {}
SESSION.proxies['http'] = 'socks5h://127.0.0.1:9050'
SESSION.proxies['https'] = 'socks5h://127.0.0.1:9050'

DOMAIN = args.domain
NAME = args.name

def checkConection():
	try:
		req = SESSION.get(URL)
		if req.status_code == 200:
			pass
		else:
			print("[!] Start Tor Services!")
			sys.exit()
	except:
		print("[!] Start Tor Services!")
		sys.exit()

def verifyParamethers():
	if DOMAIN != None:
		payload = {"domain":DOMAIN,"luser":"","luseropr":"0","domainopr":"0","submitform":"em"}
		return payload
	if NAME != None:
		payload = {"domain":"","luser":NAME,"luseropr":"0","domainopr":"0","submitform":"em"}
		return payload	

def consultLeak(payload):
	req = SESSION.post(URL, data=payload)
	soup = BeautifulSoup(req.text, 'html.parser')
	pre = str(soup.find_all('pre'))
	pre = pre.replace("\n","").replace("Array","").replace(" ","")
	pre = pre.replace("<pre>","").replace("</pre>","")
	pre = pre.replace("				","").replace("&gt;","")
	pre = pre.replace("[luser]=","|").replace("[domain]=","@").replace("[password]=",":")
	pre = pre.strip("[id]")
	pre = pre.split("(")
	
	print(f"[x] Total results: {str(len(pre)-2)}")

	for x in range(len(pre)):
		if x >= 2:
			result = pre[x].split("|")
			cred = result[1].replace(")"+str(x),"")
			if x+1 == len(pre):
				cred = cred.replace(")","")
			print(cred)
			
def main():
	print(banner)
	payload = verifyParamethers()
	checkConection()
	consultLeak(payload)

if __name__ == '__main__':
	main()