# TO DO LIST:
# 1. short results at the end (some kind of summary). Probably it makes sense to make different mods: debug, short and so on.
# 2. different error messages for different exceptions (JSONDecodeError, for instance).

import sys
import json
import requests
import colorama
from enum import Enum

import pdb; 

__title__ = 'itools'
__version__ = "1.0"

class resourceType(Enum):
	DO_NOTHING 	= 0 
	CC_TEST = 1
	CC_PROD = 2
	R_TEST 	= 3
	R_PROD 	= 4

def doShowHelp(isExpected = True):
	help_text = ""
	if(isExpected == False):
		help_text += """
Unknown option! Check the usage description below
"""
	help_text += """
Usage: itools.py [option]

Available options:
-h, --help                  show help note
-v, --version               show version number
-cc, --cleancache           clean Discovery cache, suboptions are required:
	-p, -- prod             process only production servers
	-t, --test              process only test servers
-r, --request, --requests   request URLs, suboptions are required:
	-p, -- prod             process only production servers
	-t, --test              process only test servers
"""
	print(help_text)
	
def doShowVersion():
	print(__title__ + " " + __version__)

def doCommand(args):
	try:
		arg = args[1]
		lower_arg = arg.lower()
		
		if lower_arg == '-h' or lower_arg == '--help':
			doShowHelp()
		elif lower_arg == '-v' or lower_arg == '--version':
			doShowVersion()
		elif lower_arg == '-cc' or lower_arg == '--cleancache':
			nextPosition = args.index(arg) + 1
			subarg = args[nextPosition]
			type = getTypeFromSubCommand(lower_arg, subarg)
			if type is not None:
				doCleanCache(type)
			else:
				raise
		elif lower_arg == '-r' or lower_arg == '--request' or lower_arg == '--requests':
			nextPosition = args.index(arg) + 1
			subarg = args[nextPosition]
			type = getTypeFromSubCommand(lower_arg, subarg)
			if type is not None:
				doRequest(type)
			else:
				raise

		else: #default case
			raise

	except Exception as e:
		doShowHelp(isExpected = False)

def getTypeFromSubCommand(arg, subarg):
	lower_arg = arg.lower()
	lower_subarg = subarg.lower()
	type = None
	if lower_arg == '-cc' or lower_arg == '--cleancache':
		if lower_subarg == '-p' or lower_subarg == '--prod':
			if checkAssurance():
				type = resourceType.CC_PROD
			else:
				type = resourceType.DO_NOTHING
		elif lower_subarg == '-t' or lower_subarg == '--test':
			type = resourceType.CC_TEST
	if lower_arg == '-r' or lower_arg == '--request' or lower_arg == '--requests':
		if lower_subarg == '-p' or lower_subarg == '--prod':
			if checkAssurance():
				type = resourceType.R_PROD
			else:
				type = resourceType.DO_NOTHING
		elif lower_subarg == '-t' or lower_subarg == '--test':
			type = resourceType.R_TEST
	return type

def doCleanCache(type = None):	 
	if type is not None and type != resourceType.DO_NOTHING:
		print("Cache cleaning is starting. Please wait...")

		list = readConfig()
		
		#AuthUser = "autotester"
		#AuthPassword = "Intouch123"
		for sp in list:
			# Check type of resource.
			if(resourceType[sp["type"]] == type):
					try:
						url = sp["url"]     
						httpBasicAuth_user = sp["httpBasicAuth_user"]
						httpBasicAuth_pass = sp["httpBasicAuth_pass"]
						user = sp["user"]
						password = sp["password"]
						response = requests.post(url, data = createSoapRequest(user, password), auth=(httpBasicAuth_user,  httpBasicAuth_pass), timeout=(30, 30))
						#checkResponse(response)
						colorPrintSuccess(url)
						print(response.text)
					except Exception as e:
						colorPrintFail("Error for server " + url)
						print(response.text)
						print(e)
	return

def doRequest(type = None):	 
	if type is not None and type != resourceType.DO_NOTHING: 
		pdb.set_trace();
		print("Requests are starting. Please wait...")
		list = readConfig()
		for sp in list:
			# Check type of resource.
			if(resourceType[sp["type"]] == type):
				try:
					# get params
					url = sp["url"]     
					httpBasicAuth_user = sp["httpBasicAuth_user"]
					httpBasicAuth_pass = sp["httpBasicAuth_pass"]
					
					if(httpBasicAuth_user == ""):
						response = requests.get(url)#, auth=(sp["httpBasicAuth_user"],  sp["httpBasicAuth_pass"]))
					else:
						response = requests.post(url, auth=(httpBasicAuth_user,  httpBasicAuth_pass), timeout=(30, 30))
					
					#checkResponse(response)
					colorPrintSuccess("OK for server " + url)
					print(response.text)
				except Exception as e:
					colorPrintFail("Error for server " + url)
					print(response.text)
					print(e)

def checkAssurance():
	assurance = False
	answer = input("You are going to process production servers. Are you shure?[y/n]")
	answer = answer.lower()
	if answer == "y" or answer == "yes":
		assurance = True
	return assurance
			
def writeConfig(params_collection, fileName = 'itools.cfg'):
	str = json.dumps(params_collection, indent = 4)
	print(str)
	with open(fileName, 'w') as outfile:
		outfile.write(str)


def readConfig(fileName = 'itools.cfg'):
	try:
		with open(fileName, 'r') as infile:  
			str = infile.read()
		return json.loads(str)
	#except JSONDecodeError:
	#	print(fileName + " has a wrong file forman. Should be JSON.")
	except Exception as e:
		print(type(e))
		print(e)

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