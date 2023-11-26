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


# URLS, group into folder option
urls = []


groupFolder = {
    "PromptStatus": "None",
    "Name": ""
}


# read config and assign variables for location and filename of SpotDL
f = open(cfgDir + "/cfg.txt", "r").read().split('\n')
sdlAppName = "/" + f[1]
print("Directory: " + sdlDirectory + "\nSpotDL Name: " + sdlAppName + "\n")




class songItem:
    id = 0
    url = ""
    selected = False

    def __repr__(self):
        return str(self.id) + ". " + self.url



# main window layout
layout = [
    [sg.Listbox(urls, size=(50,7), key="-LIST-")],
    [sg.Checkbox("Group tracks into folder.", False, key="-GRP-"), sg.Push(), sg.Button("Clear All", key="-CLRALL-", size=(6,1), font=("Arial"))],
    [sg.Text("Enter song title or URL(s) below."), sg.Push() ],
    [sg.Input(size=(33,5), key="-URL-"), sg.Push(), sg.Button("+", key="-ADD-", font=("Arial", 12, "bold"), size=(2,1))],
    [sg.Button("Download Tracks", size=(40,2), key="-DL-")]
]


# create main window
window = sg.Window('SpotDL-UI', layout, size=(320,275))


def moveTracks():

    movedFiles = 0

    for root, dirs, files in os.walk(mainDir):
        for f in files:

            if f.endswith('.mp3'):
                
                movedFiles += 1

                old_fdir = os.path.join(root, f)
                new_fdir = os.path.join(musicDir)

                if groupFolder["PromptStatus"] == "entered":

                    #print("Packing tracks into folder...")

                    myCreatedFolder = os.path.join(musicDir, groupFolder["Name"])
                    if not os.path.exists(myCreatedFolder): # prevent File Exists error
                        os.mkdir(myCreatedFolder)

                    shutil.move(old_fdir, myCreatedFolder + "/" + f) # move song to group folder

                else:
                    shutil.move(old_fdir, new_fdir + "/" + f) # move song to music folder
                

    return movedFiles




dlProgress = {
    "currentTrack": 0,
    "numTracks": 0
}


while True: # The Event Loop
    event, values = window.read()  

    # program end event
    if event == sg.WIN_CLOSED or event == 'Exit':
        break


    # clear URL list
    elif event == "-CLRALL-":
        urls.clear()
        window["-LIST-"].update(urls)
        print("Cleared tracklist.")


    elif event == "-GRPSKIP-":
        if winPromptFolderName:
            winPromptFolderName.close()


    # add to URL list
    elif event == "-ADD-":

        track = songItem()
        track.id = len(urls)+1
        track.url = values["-URL-"]
        urls.append(track)

        print("Added track. (" + track.url + ")")

        window["-LIST-"].update(urls)
        window["-URL-"].update(value="")

        #print("Track list: " + str(len(urls)))

    # begin downloading
    elif event == "-DL-":


        # if user chose to group songs into a folder, ask for folder name.
        if values["-GRP-"] == True:
            
            folderNamePrompt = sg.popup_get_text("You chose to group tracks into a folder. Enter folder name.")
            groupFolder["PromptStatus"] = "awaiting"

            # get folder name or indicate that user changed their mind.
            while (groupFolder["PromptStatus"] == "awaiting"):
                if folderNamePrompt:
                    # user entered folder name. Keep it somewhere for now.
                    groupFolder["PromptStatus"] = "entered"
                    groupFolder["Name"] = folderNamePrompt
                else:
                    # user did not want to create folder.
                    groupFolder["PromptStatus"] = "cancelled"


        numFilesToDownload = len(urls)
        window["-DL-"].Update("Downloading...")


        dlProgress["currentTrack"] = 1
        dlProgress["numTracks"] = len(urls)
        
        print("\n")


        for u in urls:

            print("Downloading... (" + str(dlProgress["currentTrack"]) + " / " + str(dlProgress["numTracks"]) + ")")

            os.chdir(mainDir)
            subprocess.run([sdlDirectory + sdlAppName, u.url]) # run spotdl with url as argument

            dlProgress["currentTrack"] += 1


        numTransfered = moveTracks()

        # displays incorrect file count for some reason so I disabled this function and used the one below..
        #resultsWindow = sg.popup_ok("Tracks downloaded: " + str(numTransfered) + "/" + str(numFilesToDownload), "You can find them in the music folder.")
        
        # show download results.
        resultsWindow = sg.popup_ok("Your tracks have been downloaded.", "You can find them in the music folder.")
        print("\nThank you for using spotDL-UI.\nYour tracks can be found in spotdl-ui/music.")

        # restore download button text
        window["-DL-"].Update("Download Tracks")


window.close()
