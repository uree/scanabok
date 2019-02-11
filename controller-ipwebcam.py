# -*- coding: utf-8 -*-
#to be used in conjunction with android app ipwebcam


import wget
import requests 
import os
import subprocess


#SETTINGS
#camera 1 = odd, left camera - taking picture of the right page
#camera 2 = even, right camera - taking picture of the left page

#values from ipwebcam settings
camera1_url='http://192.168.1.95:7777/photoaf.jpg'
camera2_url = 'http://192.168.1.204:8080/photoaf.jpg'



book_title = ''
project_folder = ''

#optional
startpage = 0




#CODE
def getpicture(url, filenum):
    r = requests.get(url)
    print str(url)+": "+str(r.status_code)

    if r.status_code == 200:
        with open(filenum, 'wb') as f:
            f.write(r.content)



def controller(startpage=0):
    try:
        counter = startpage
    except:
        counter = 0
        pass

    while True:
        x = raw_input("Press enter to take a picture ... (to exit type done)")
        if x == "done":
            print "Exiting ..."
            print "Done."
            break
        
        cam_num1 = counter+1
        cam_num2 = counter
        
        

        try:
            cam_num1 = project_folder+book_title+"_"+str(cam_num1)+'.jpg'
        except:
            pass

        try:
            cam_num2 = project_folder+book_title+"_"+str(cam_num2)+'.jpg'
        except:
            pass

        getpicture(camera1_url, cam_num2)
        getpicture(camera2_url, cam_num1)


        counter = counter+2
        print counter




#START
if not os.path.exists(project_folder):
    os.makedirs(project_folder)

controller()

raw_input("Will open scantailor for postprocessing ...")

scant = subprocess.call(scantailor)

print "Type potato when ready to continue. The script will then perform ocr and merge files into 1 pdf. Any key to abort."

p = raw_input("Waiting ...")

if p == "potato":
    #do processing
    print "Trust the Process."
else:
    print "Abort."