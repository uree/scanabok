#coding?
#popro_1.0.py postprocessing of pdfs flow


import os
import subprocess

#SETTINGS
#directory of pdf files
#pages_dir default (per scantailor) = /out
pages_dir = "" 
outname = ""


#run bash script
def run_bash(pages_dir, outname):
    print "start"
    r = subprocess.call(["./bash_pdf.sh", pages_dir, outname])
    print "end"

run_bash(pages_dir, outname)
