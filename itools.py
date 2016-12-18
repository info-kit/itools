﻿# Here I would like to research the possibilities of sys library.
# C:\Python\Programs\Python Lab\2016\2016-11-12_Python_sys_arg.py

# from __future__ import print_function
import sys
import json
import requests
import colorama

__title__ = 'itools'
__version__ = "1.0"

def doShowHelp():
	help_text = """
	Unknown option
	usage: itools.py [option]
	
	option:
	-h, --help                  show help note
	-v, --version               show version number
	-cc, --cleancache           clean Discovery cache
	-r, --request, --requests   request URLs
	
	"""
	print(help_text)
	
def doShowVersion():
	print(__version__)

def doCommand(args):
	for arg in args:
		lower_arg = arg.lower()
		if lower_arg == '-h' or lower_arg == '--help':
			doShowHelp()
		elif lower_arg == '-v' or lower_arg == '--version':
			doShowVersion()
		elif lower_arg == '-cc' or lower_arg == '--cleancache':
			doCleanCache()
		elif lower_arg == '-r' or lower_arg == '--request' or lower_arg == '--requests':
			doRequest()
		else: #default case
			doShowHelp()

def doCleanCache():	 
	print("Cache cleaning is starting. Please wait...")

	list = readConfig()
	
	#AuthUser = "autotester"
	#AuthPassword = "Intouch123"
	for sp in list:
		try:
			full_url = sp["url"]     
			#response = requests.post(full_url, data = createSoapRequest(sp[1], sp[2]), auth=(AuthUser,  AuthPassword), timeout=(30, 30))
			#checkResponse(response)
			colorPrintSuccess(full_url)
		except Exception as e:
			pass
			#colorPrintSuccess(response, e)
	return

def doRequest():	 
	print("Requests is starting. Please wait...")
	list = readConfig()
	for sp in list:
		try:
			# get params
			full_url = sp["url"]     
			httpBasicAuth_user = sp["httpBasicAuth_user"]
			httpBasicAuth_pass = sp["httpBasicAuth_pass"]
			
			if(httpBasicAuth_user != ""):
				response = requests.get(full_url)#, auth=(sp["httpBasicAuth_user"],  sp["httpBasicAuth_pass"]))
			else:
				response = requests.post(full_url, auth=(httpBasicAuth_user,  httpBasicAuth_pass), timeout=(30, 30))
			
			#checkResponse(response)
			colorPrintSuccess("OK for server " + full_url)
			print(response.text)
		except Exception as e:
			colorPrintFail("Error for server " + full_url)
			print(response.text)
			print(e)

			
def writeConfig(params_collection, fileName = 'itools.cfg'):
	str = json.dumps(params_collection, indent = 4)
	print(str)
	with open(fileName, 'w') as outfile:
		outfile.write(str)


def readConfig(fileName = 'itools.cfg'):
	with open(fileName, 'r') as infile:  
		str = infile.read()
	return json.loads(str)

def createSoapRequest(admin, password):
    soap_req = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sys="http://www.in-touch.ru/services/system-administration">
   <soap:Header/>
   <soap:Body>
      <sys:clearMemoryCache interfaceVersion="V_1_0">
         <sys:appServerEntityCache>
            <sys:login>""" + admin + """</sys:login>
            <sys:password>""" + password + """</sys:password>
         </sys:appServerEntityCache>
         <sys:discoveryApplicationCache/>
      </sys:clearMemoryCache>
   </soap:Body>
</soap:Envelope>"""   
    return soap_req

def checkResponse(response):
# Not implemented yet.
#    try:
#        xml = untangle.parse(response.text)
#        xml.root.child["<soap:Body>"].child["<soap:Fault>"]
#    except Exception as e:
#        pass
#    else:
#        raise XmlException
    pass
         
	
def colorPrintSuccess(string):
	colorama.init(autoreset=True)
	print(colorama.Fore.GREEN + string)
	
def colorPrintFail(string):
	colorama.init(autoreset=True)
	print(colorama.Fore.RED + string)

def main():
	doCommand(sys.argv)
	
if __name__ == "__main__":
	main()