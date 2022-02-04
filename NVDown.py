import os
import sys
import requests
import msvcrt
import winsound
from six.moves import input as raw_input
from datetime import datetime
from playsound import playsound
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
os.system("title NVDown")
def NVDown():
    version = raw_input("Enter the version of NVDA you'd like to download\n")
    try:
        if float(version) < 2013.3:
            winsound.MessageBeep(48)
            print("Error! NVDA version too low. Must be 2013.3 or higher.")
            NVDown()
    except ValueError, e:
        LogFile = open("ErrorFile.log","a")
        LogFile.write("Date and time of error: " + datetime.today().strftime("%A, %d %B, %Y at %I:%M %p") + "\nType of error: Value Error\nSummary of error: An unexpected user input error was encountered.\nError data:\n" + str(e) + "\n\n")
        LogFile.close()
        winsound.MessageBeep(16)
        print("Error! There was a problem with your input. Please try again.")
        NVDown()
    patch = ""
    patch = raw_input("Enter a patch number. For example, if you wanted NVDA " + version + ".1, you'd enter the number 1 into this field. Leave blank to download the version without any patches\n")
    if patch == "":
        nvver = version
    else:
        nvver = version + "." + patch
    os.environ['ver'] = "nvda_" + nvver + ".exe"
    playsound("snd/trying.mp3",block = False)
    print("Trying to connect to NV Access...")
    try:
        nvloc = requests.get("https://www.nvaccess.org/download/nvda/releases/" + nvver + "/nvda_" + nvver + ".exe", verify = False)
    except requests.exceptions.ConnectionError, e:
        LogFile = open("ErrorFile.log","a")
        LogFile.write("Date and time of error: " + datetime.today().strftime("%A, %d %B, %Y at %I:%M %p") + "\nType of error: HTTP Connection Error\nSummary of error: A connection to the NV Access website could not be made.\nError data:\n" + str(e) + "\n\n")
        LogFile.close()
        winsound.MessageBeep(16)
        print("Error connecting to NVAccess. Please check your internet connection and try again.")
        NVDown()
    if sys.getwindowsversion().major >= 6:
        downpath = os.path.join(os.environ['userprofile'],"downloads",os.environ['ver'])
    elif sys.getwindowsversion().major == 5:
        downpath = os.path.join(os.environ['userprofile'],"my documents","downloads",os.environ['ver'])
    playsound("snd/started.mp3",block = False)
    print("Downloading NVDA " + nvver + "...")
    downfile = open(downpath,"wb")
    downfile.write(nvloc.content)
    downfile.close()
    winsound.MessageBeep(64)
    waiting = True
    while waiting:
        print("Download complete!\nNVDA " + nvver + " has been downloaded and saved to " + downpath + ".")
        print("What would you like to do now?\n\n1.Launch the NVDA installer and exit this program.\n2. I'll launch the installer myself. Just exit the program.\n")
        menu = msvcrt.getch()
        if menu == "1":
            waiting = False
            os.startfile(downpath)
            sys.exit()
        elif menu == "2":
            waiting = False
            sys.exit()
NVDown()