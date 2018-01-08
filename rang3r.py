#!/usr/bin/python
# If you don't have Termcolor installed do this cmd => pip install termcolor
import os
import sys
logo = ""
logo +="                        _____       \n"
logo +="  _ __ __ _ _ __   __ _|___ / _ __  \n"
logo +=" | '__/ _` | '_ \ / _` | |_ \| '__| \n"
logo +=" | | | (_| | | | | (_| |___) | |    \n"
logo +=" |_|  \__,_|_| |_|\__, |____/|_|    \n"
logo +="                  |___/             \n\n"
from termcolor import colored
print colored(logo,"red")
print colored("Created by florianx00 - H4d3s / Republic of Albania","yellow")
print ""
import optparse 
parser = optparse.OptionParser()
parser.add_option('--ip',dest="question",help="test ")
opt , args = parser.parse_args()

if opt.question :
   question = (opt.question)
elif not (opt.question) :
   print("--ip option is required ")
   sys.exit()
#end ip = option

os.system("python files/ipscan.py --ip=%s" % question)
