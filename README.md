# SpotDL-UI
Simple UI frontend for SpotDL

![Screenshot_2023-11-17_16-47-39](https://github.com/splatert/spotdl-ui/assets/82643571/2efb916d-b7b6-4227-8953-82146289f220)


### Requirements
- Python
- Spot-DL

### Setup
1. Place SpotDL executable into the spotdl-ui/app folder.
2. Replace the second line in spotdl-ui/cfg/cfg.txt with the name of your SpotDL executable.



### Usage
1. Launch spotdl-ui.py
2. Enter Spotify URL then click on the + button to add it to the list of tracks to be downloaded.
3. After adding URLs, click on the 'Download' button to initiate SpotDL and download tracks using the URLs you provided.
4. The interface should freeze and SpotDL should be downloading your tracks (progress is shown on the terminal).
5. Once the tracks have been downloaded, you should find them at the spotdl-ui/music folder.


![image](https://github.com/splatert/spotdl-ui/assets/82643571/46574fc1-5a47-4d84-9b4f-f2636b978d1f)

Many thanks to @PySimpleGUI for their easy-to-use python UI framework
You can check it out through the link below.
https://www.pysimplegui.org/en/latest/
