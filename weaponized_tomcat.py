import re
import requests
import socket
import colorama
from urllib.parse import urlparse
from colorama import Fore
colorama.init(autoreset=True)


"""
Author: The_Architect
Last Updated: 04/22/23

Main Notes:
This script maps and checks for various tomcat misconfigurations such as tomcat version,ghostcat,backtrace password disclosure and valid credentials

"""

print(Fore.YELLOW+"""
╦ ╦┌─┐┌─┐┌─┐┌─┐┌┐┌┬┌─┐┌─┐┌┬┐  ╔╦╗┌─┐┌┬┐┌─┐┌─┐┌┬┐  ╔═╗┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐
║║║├┤ ├─┤├─┘│ │││││┌─┘├┤  ││   ║ │ │││││  ├─┤ │   ╚═╗│  ├─┤││││││├┤ ├┬┘
╚╩╝└─┘┴ ┴┴  └─┘┘└┘┴└─┘└─┘─┴┘   ╩ └─┘┴ ┴└─┘┴ ┴ ┴   ╚═╝└─┘┴ ┴┘└┘┘└┘└─┘┴└─

""")



url = input("please enter the url: ")
print("Starting Enumration of Tomcat website\n")

u = ["admin","manager","role1","role","root","tomcat"]
p = ["s3cret","s3cr3t","password","Password1","admin","tomcat","manager","role1","changethis","root","r00t","toor","admin"]




# get the version of tomcat
print(Fore.YELLOW+"Getting Version")
r = requests.get(url+"/docs")
r = r.text
result = re.findall(r"Version(.*?),",r,re.DOTALL)[0]
print(Fore.RED+f"Tomcat Version is: {result}")


#check for ghostcat
print(Fore.YELLOW+"\nChecking for Ghostcat Vulnerablility")

purl = urlparse(url)
hostname = purl.hostname
port = 8009

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(1)
result = s.connect_ex((hostname,port))
if result == 0:
	print(Fore.RED+"Possibly vulnerable to GhostCat")
else:
	print('Not Vulnerable')



#check for backtrace password disclosure
print(Fore.YELLOW+"\nChecking for Backtrace passowrd Disclosure")
r = requests.get(url+"/auth.jsp")
if r.status_code == 200:
	print("\nable to access auth.jsp may be able to disclose password")

else:
	print("Not vulnerable")


#check for common credential use
print(Fore.YELLOW+"\nTesting For Common Credential Use")
for user in u:
	for password in p:
		auth = (user,password)
		r = requests.post(url+"/manager/html",auth=auth)
		if "Tomcat Web Application Manager" in r.text:
			print(Fore.RED+f"Successfully login as {user}:{password}")

		else:
			print(f"{user}/{password}",end='\r')



