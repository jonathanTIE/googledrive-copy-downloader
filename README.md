# googledrive-copy-downloader
This python script allow you to download google drive files even if the daily limit of download has excedeed using google drive API by directly pasting the link of the file.
It automatically copy the file to the google drive of the account that is provided, download the file and delete it, and it supports multiple links at once.


## How to use : 
First, you need to add a Google application credentials(clients_secrets.json) that can access the Google drive API.

To do that, the quickest way is to :
* Go to : https://developers.google.com/drive/api/v3/quickstart/python
* Click on enable drive API
* Download client configuration
* Rename this file client_secrets.json
* Replace the one in the folder with the script (in the same place as the .exe)

#### You can launch it directly using python :
Use preferably python 3.6, install the requirement on the requirements.txt file with pip and launch gDriveCopyDownloader.py.
#### You can use the release :
You just need to download the .zip, and launch the exe.
#### You can make yourself the .exe :
Use auto-py-to-exe or pyinstaller, select gDriveCopyDownloader as the input.


Then you can follow the instructions on the script. Careful if you store the credentials (to avoid log-in every time), it keeps them in plain text and it can give access to your google drive(I think the risks that a pirate and and know what to do with your credentials is low.)


### Common issues : 
* "This app has not been verified yet" or any other issues with client_secrets : 
Check the How to use section.
* Space issues :
the script could crash itself if there is not enough space on your google drive, be sure to check the bin.
* Authentication problems  :
If you have any app that communicate through localhost:8080 (like Kodi), the authentication with google servers may not works.


### Known limitations :
* Doesn't gather link from hypertext(for example, when there is a link on a website but when you copy&paste you only get the text and not the actual link), the workaround could be to copy and paste first to jdownloader and then copy the links from jdownloader to the cmd.
* There might be somme issues with linux(getting the default download folder for example).
* Currently, the script only support links with that end with : /d/XXXX, /id=XXX and /folders/XXXX .
* The script doesn't display the speed of download or the total size of the file.
* It doesn't work with google files(sheet, docs,...).


