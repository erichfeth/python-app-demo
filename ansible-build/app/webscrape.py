import os
import urllib3
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

def get_status(site):

        try:
                http = urllib3.PoolManager()
                request = http.request('GET', site)
                status_code = request.status
        except:
                print("Site could not resolve")
                status_code = 000
        return status_code

if __name__ == '__main__':

        file = sys.argv[1]
        try:
                f = open(file, "r")
        except IOError:
                print ("Could not open/read file:"), file
                sys.exit()
        with f:
                #creates virtual display
                display = Display(visible=0, size=(800, 600))
                display.start()

                #creates profile
                firefox_profile = webdriver.FirefoxProfile()
                firefox_profile.set_preference('browser.download.folderList', 2)
                firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
                firefox_profile.set_preference('browser.download.dir', os.getcwd())
                firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

                #opens browser
                driver = webdriver.Firefox(firefox_profile=firefox_profile)

                #varible for naming screenshot files
                filenum = 1

                Lines = f.readlines()
                for line in Lines:
                        #Reads a line from input file
                        sys.stdout.write("Address: %s" % line)
                        #Gets Status Code from webpage
                        status = get_status(line.strip())
                        #Prints status code
                        print ("Status:" , status)
                        #Checks website for status code of 200 indicating that the website is online
                        if status == 200:
                                #get webpage from  list
                                driver.get(line)
                                #get webpage title
                                title = driver.title
                                #print webpage title 
                                print("Title: " + title)
                                #takes screenshot of webpage and saves it as a file using filenum
                                print("Taking Screenshot...")
                                driver.save_screenshot('screenshots/screenshot%d.png' %filenum);
                                #increment filename
                                filenum += 1
        print("Completed")
        driver.close()
        display.stop()
