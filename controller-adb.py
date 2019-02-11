#controller-adb.py version 2.0-dual
#works with smartphones connected to the computer via usb

import os.path as op
import os
from time import sleep

from adb import adb_commands
from adb import sign_m2crypto

import re
import subprocess

#SETTINGS
#the image location on device (check in camera app (i))
pic_folder_camera1 = "/sdcard/DCIM/Camera/"
pic_folder_camera2 = "/storage/emulated/0/DCIM/Camera/"
#where do you want to store the files
project_folder = ""
#output filename
book_title = ""

#camera 1 = odd, left camera - taking picture of the right page
#camera 2 = even, right camera - taking picture of the left page
camera1_serial = ""
camera2_serial = ""

#optional
startpage = 0

#FIND DEVICES
#https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python
def list_usbs():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    iserial_re = re.compile("\s\s+iSerial.*", re.I)
    df = subprocess.check_output("lsusb -v", shell=True)
    #print df
    devices = []
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            serial = iserial_re.match(i)
            if info:
                #print info.group()
                #print info.group()
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            if serial:
                #print serial.group()
                serial = serial.group(0)
                dinfo['serial'] = serial
                #print "\n"
                devices.append(dinfo)

    return devices




def take_pic(device):       
        device.Shell("input keyevent KEYCODE_FOCUS")
        sleep(1)
        device.Shell("input keyevent 27")
        sleep(1)


#how will i combine photos to keep page order?
#in both cases (transfer while & transfer end)
#first do transfer end (cos this is controller-adb)

def copy_files(device, pic_folder, startpage, counter):

    cmnd = "ls -1t "+str(pic_folder)
    print cmnd
    file_order = device.Shell(cmnd)
    bzz = file_order.split("\n")
    print "copyfiles counter "+str(counter)
    num = counter+1
    print "copyfiles counter "+str(num)
    bzz = bzz[0:num]
    bzz_ready = []
    for i in bzz:
        if i!= "cache":
            bzz_ready.append(str(i))
    print bzz_ready

    bzz_ready = bzz_ready[::-1]
    print bzz_ready


    pagenum = startpage
    for i in bzz_ready:
        try:
            device.Pull(pic_folder+i, project_folder+book_title+"_"+str(pagenum)+".jpg")
            pagenum +=2
        except:
            pass
            pagenum +=2



def ground_control():
    #make it happen from here

    device1.Shell("am start -a android.media.action.STILL_IMAGE_CAMERA")
    print "ASS"
    device2.Shell("am start -a android.media.action.STILL_IMAGE_CAMERA")

    counter = 0
    
    while True:
        x = raw_input("Press Enter to take pictures ... Type stop to stop.")
        if x == 'stop':
            break
        take_pic(device1)
        take_pic(device2)
        sleep(2)
        counter+=1 
        print "while loop1 "+str(counter)

    raw_input("Done. Press enter to copy files to computer.")

    #copyfiles camera1
    copy_files(device1, pic_folder_camera1, startpage+1, counter-1)

    #copyfiles camera2
    copy_files(device2, pic_folder_camera2, startpage, counter)

    print "Finished. All pictures in "+project_folder

    #further processing with popro1.0.py

    raw_input("Will open scantailor for postprocessing ...")

    scant = subprocess.call(scantailor)

    print "Type potato when ready to continue. The script will then perform ocr and merge files into 1 pdf. Any key to abort."

    p = raw_input("Waiting ...")

    if p == "potato":
        #do processing
        print "Trust the Process."
    else:
        print "Abort."



#CHECK CAMERA SETTINGS
if camera1_serial and camera2_serial:
    #do stuff right away
    pass
else:
    begin = raw_input("List usb devices? [y/n]")
    if begin == "y":
        usbs = list_usbs()
        for i in usbs:
            print i
    else:
        pass
    camera1_serial = raw_input("Please enter the serial number of the camera on the left: ")
    camera2_serial = raw_input("Please enter the serial number of the camera on the right: ")

print camera1_serial
print camera2_serial


#CONNECT TO CAMERAS
# KitKat+ devices require authentication
signer = sign_m2crypto.M2CryptoSigner(
    op.expanduser('~/.android/adbkey'))

# Connect to the devices
#port_path: The filename of usb port to use.
#serial: The serial number of the device to use.
device1 = adb_commands.AdbCommands.ConnectDevice(
    rsa_keys=[signer], serial=camera1_serial, default_timeout_ms=5000)
print "Device 1 success."

device2 = adb_commands.AdbCommands.ConnectDevice(
    rsa_keys=[signer], serial=camera2_serial)
print "Device 2 success."

#create folder
if not os.path.exists(project_folder):
    os.makedirs(project_folder)

ground_control()
