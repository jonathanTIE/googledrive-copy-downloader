import os

import GoogleAuthManager
import gDriveLibrary


def get_default_download_location():
    if os.name == 'nt':  # if windows
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def get_location():
    if not os.path.exists("directory.txt"):
        with open("directory.txt", "w+"): pass  # create file if doesn't exist
    with open("directory.txt", 'r') as f:
        path = f.read()
    if os.path.exists(path):
        return path
    print("Default location is : " + get_default_download_location())
    while 1:
        otherPath = input("\nif you want another location, write it here or else press enter\n")
        if os.path.exists(otherPath):
            break
        if otherPath == "":
            otherPath = get_default_download_location()
            break
    with open("directory.txt", 'w') as f:
        f.write(otherPath)
    return otherPath


print(" Some infos : \n"
      "You can put the links directly from google drive ('https://drive.google.com') but also those behind a "
      "redirection(like the one from igg).\n"
      "Temporary files in google drive of your download will be stored on 'Temp folder for script', you can delete it "
      "after the downloads. \n"
      "The download percentage status is updated about every 100 MB, so wait a little if it appears to be stuck.\n"
      "You can put multiple links at the same time\n")
print("###############")
print("\n Careful, if you choose to save the credentials : "
      " An access to your google drive will be/is stored on 'credentials.txt'. \n IT COULD BE USED BY SOMEONE ELSE"
      " TO ACCESS, DOWNLOAD OR DELETE FILES FROM YOUR GOOGLE DRIVE. \n I'm not responsible if anything bad happen"
      " in your drive.\n")
print("###############")
drive = GoogleAuthManager.create_drive_manager()
get_location()  # ask for path if not set

while 1:
    links = input("paste the link(s) to download : \n")
    for fileID in gDriveLibrary.extract_files_id(links, drive):
        copiedFile = gDriveLibrary.copy_file(drive, fileID)
        gDriveLibrary.download_file(drive, copiedFile, get_location())
        gDriveLibrary.delete_file(drive, copiedFile['id'])
