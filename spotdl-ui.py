#!/usr/bin/python




import subprocess
import include.PySimpleGUI as sg
import os, shutil


# PySimpleGui theme
sg.theme('DarkGreen5') 


# directories
mainDir = os.path.dirname(os.path.abspath(__file__))
cfgDir = os.path.join(mainDir, "cfg")
sdlDirectory = os.path.join(mainDir, "app")
musicDir = os.path.join(mainDir, "music")
sdlAppName = ""


# URLS and download progress indicators
urls = []


# read config and assign variables for location and filename of SpotDL
f = open(cfgDir + "/cfg.txt", "r").read().split('\n')
sdlAppName = "/" + f[1]

print("Directory: " + sdlDirectory + "\nSpotDL Name: " + sdlAppName)



# main window layout
layout = [
    [sg.Listbox(urls, size=(50,7), key="-LIST-")],
    [sg.Text("Enter URL(s) below."), sg.Push(), sg.Button("Clear All", key="-CLRALL-", size=(6,1), font=("Arial"))],
    [sg.Input(size=(30,5), key="-URL-"), sg.Button("+", key="-ADD-", font=("Arial", 12, "bold"), size=(5,1))],
    [sg.Button("Download Tracks", size=(40,15), key="-DL-")]
]


# create main window
window = sg.Window('SpotDL-UI', layout, size=(320,240))




def moveTracks():

    movedFiles = 0

    for root, dirs, files in os.walk(mainDir):
        for f in files:

            if f.endswith('.mp3'):
                
                movedFiles += 1

                old_fdir = os.path.join(root, f)
                new_fdir = os.path.join(musicDir)

                shutil.move(old_fdir, new_fdir + "/" + f) # move song to music folder
                
    return movedFiles




while True: # The Event Loop
    event, values = window.read()      


    # program end event
    if event == sg.WIN_CLOSED or event == 'Exit':
        break


    # clear URL list
    elif event == "-CLRALL-":
        urls.clear()
        window["-LIST-"].update(urls)


    # add to URL list
    elif event == "-ADD-":

        urls.append(values["-URL-"])

        window["-LIST-"].update(urls)
        window["-URL-"].update(value="")

        print("Track list: " + str(len(urls)))


    # begin downloading
    elif event == "-DL-":

        numFilesToDownload = len(urls)
        window["-DL-"].Update("Downloading...")

        for u in urls:
            os.chdir(mainDir)
            subprocess.run([sdlDirectory + sdlAppName, u]) # run spotdl with url as argument

        numTransfered = moveTracks()

        # displays incorrect file count for some reason so I disabled this function and used the one below..
        #resultsWindow = sg.popup_ok("Tracks downloaded: " + str(numTransfered) + "/" + str(numFilesToDownload), "You can find them at the music folder.")
        
        # show download results.
        resultsWindow = sg.popup_ok("Your tracks have been downloaded.", "You can find them at the music folder.")

        # restore download button text
        window["-DL-"].Update("Download Tracks")


window.close()
