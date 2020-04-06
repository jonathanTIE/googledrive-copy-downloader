import os

import GoogleAuthManager
import gDriveLibrary
import configparser
import asyncio

CONFIG = configparser.ConfigParser()
CONFIG.optionxform=str
DATABASE = CONFIG['DEFAULT']

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

def read_config():
    CONFIG.read('config.ini')

def write_config():
    if 'ClipboardDetection' not in DATABASE:
        DATABASE['ClipboardDetection'] = "0"
    with open("config.ini", "w+") as file:
        CONFIG.write(file)

def get_location():
    read_config()
    if 'DownloadPath' in DATABASE and os.path.exists(DATABASE['DownloadPath'] ):
        return DATABASE['DownloadPath']
    print("Default location is : " + get_default_download_location())
    while 1:
        otherPath = input("\nif you want another location, write it here or else press enter\n")
        if os.path.exists(otherPath):
            break
        if otherPath == "":
            otherPath = get_default_download_location()
            break
    DATABASE['DownloadPath'] = otherPath
    write_config()
    return otherPath

def get_folder_id():
    if not 'FolderId' in DATABASE:
        DATABASE['FolderId'] = 'root'
        write_config()
    return DATABASE['FolderId']

def Copy_dwnld_from_links(links, drive):
    for fileID in gDriveLibrary.extract_files_id(links, drive):
        copiedFile = gDriveLibrary.copy_file(drive, fileID, get_folder_id())
        gDriveLibrary.download_file(drive, copiedFile, get_location())
        gDriveLibrary.delete_file(drive, copiedFile['id'])


async def Check_clipboard_links(drive): #Only works for windows
    # Ressource : https://stackoverflow.com/questions/55698762/how-to-copy-html-code-to-clipboard-using-python
    if os.name == 'nt':
        import win32clipboard
    else:
        raise OSError("os isn't windows !")
    CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
    cacheClipboard = ""
    while 1:
        await asyncio.sleep(1)
        win32clipboard.OpenClipboard(0)
        try:
            src = win32clipboard.GetClipboardData(CF_HTML).decode("UTF-8")
        except TypeError:#if not html
            try:
                src = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT).decode("UTF-8")
            except TypeError:
                src = ""
        win32clipboard.CloseClipboard()
        if(src != cacheClipboard): #avoid downloading infinite loop if still in clipboard
            cacheClipboard = src
            Copy_dwnld_from_links(src, drive)

print(" Some infos : \n"
      "You can put the links directly from google drive ('https://drive.google.com') but also those behind a "
      "redirection(like the one from igg).\n"
      "Temporary files in google drive of your download will be stored on 'Temp folder for script', you can delete it "
      "after the downloads. \n"
      "Settings are stored in the config.ini file.\n"
      "If you want to put the google drive folder in a custom folder(to use your google team account), "
      "edit the FolderId field in config.ini and replace 'root' with the google drive team folder id.\n"
      "If you use Windows, you can go on config.ini and change ClipboardDetection to ClipboardDetection=1,"
      "you just have to Ctrl+C the links to download and it should handle the rest.\n"
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
get_folder_id() # create folder id txt file
while 1:
    if 'ClipboardDetection' in DATABASE and DATABASE['ClipboardDetection'] == "1" and os.name == 'nt':
        print("The script now captures your links from your clipboard !")
        asyncio.run(Check_clipboard_links(drive))
    else:
        links = input("paste the link(s) to download : \n")
        Copy_dwnld_from_links(links, drive)