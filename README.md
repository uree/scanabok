# scanabok
a portable book scanner with smartphones in place of expensive cameras

works with android only

this repo contains materials connected to a prototype of a portable/foldable book/document scanner
the images provide pointers on how to build one

the code provides two ways of controlling mounted smartphones from the computer (terminal)
- one for usb connected devices
- and one for wireless connections via lan, with the help of [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US), an android app

both pieces of code include lines handling the assembly and ocr of scanned pages.
the expected output is an orderly ocr'd pdf. 



##usage
1. download the code
2. prepare the scanner & mount the phones
3. fill out the settings section for the chosen script and check/install dependencies
4. run said script (controller-ipwebcam or controller-adb) and follow instructions on screen
