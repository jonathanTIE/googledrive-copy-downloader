"""
Documentation :
explain client secret(how to replace it if needed) : https://developers.google.com/drive/api/v3/quickstart/python
download : the ile is chucked with pieces of ~100MB, need to download at least this amount beore appearing on screen
"""
import re
import os
from googleapiclient.http import MediaIoBaseDownload
from tqdm import tqdm


# get download folder from user :
# https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder


def get_Gdrive_folder_id(drive, driveService, name, parent="root"):  # return ID of folder, create it if missing
    body = {'title': name,
            'mimeType': "application/vnd.google-apps.folder"
            }
    query = "title='Temp folder for script' and mimeType='application/vnd.google-apps.folder'" \
            " and '" + parent + "' in parents and trashed=false"
    if parent != "root":
        query += "and driveId='" + parent + "' and includeItemsFromAllDrives=true and supportsAllDrives = true"
    listFolders = drive.ListFile({'q': query})
    for subList in listFolders:
        if subList == []:  # if folder doesn't exist, create it
            folder = driveService.files().insert(body=body).execute()
            break
        else:
            folder = subList[0]  # if one folder with the correct name exist, pick it

    return folder['id']


def extract_file_ids_from_folder(drive, folderID):
    files = drive.ListFile({'q': "'" + folderID + "' in parents"}).GetList()
    fileIDs = []
    for file in files :
        fileIDs.append(file['id'])
    return fileIDs


def extract_files_id(links, drive):
    # copy of google drive file from google drive link :
    links = re.findall(r"\b(?:https?:\/\/)?(?:drive\.google\.com[-_&?=a-zA-Z\/\d]+)",
                       links)  # extract google drive links
    try:
        fileIDs = [re.search(r"(?<=/d/|id=|rs/).+?(?=/|$)", link)[0] for link in links]  # extract the fileIDs
        for fileID in fileIDs:
            if drive.auth.service.files().get(fileId=fileID).execute()['mimeType'] == "application/vnd.google-apps.folder":
                fileIDs.extend(extract_file_ids_from_folder(drive, fileID))
                fileIDs.remove(fileID)
        return fileIDs
    except Exception as error:
        print("error : " + str(error))
        print("Link is probably invalid")
        print(links)


def copy_file(drive, fileId, parentFolder = "root"): #if different parentFolder, input the folder ID
    fileOriginMetaData = drive.auth.service.files().get(fileId=fileId).execute()
    """remove 4 last characters of the original file name 
    and add file extension(should be .rar) in case the file extension is missing from the name """
    nameNoExtension = ".".join(fileOriginMetaData['originalFilename'].split(".")[:-1])
    newFileName = nameNoExtension + "." + fileOriginMetaData['fileExtension']
    print("Name of the file on your google drive and on the disk: " + newFileName)
    folderID = get_Gdrive_folder_id(drive, drive.auth.service, "Temp folder for script", parentFolder)
    copiedFileMetaData = {"parents": [{"id": str(folderID)}], 'title': newFileName}  # ID of destination folder
    copiedFile = drive.auth.service.files().copy(
        fileId=fileId,
        body=copiedFileMetaData
    ).execute()
    return copiedFile


def download_file(drive, file, destFolder):
    copiedFileMedia = drive.auth.service.files().get_media(fileId=file['id'])
    newFileName = file['title']
    defaultPath = destFolder + "\\" + newFileName
    fullPath = generate_path_with_unique_filename(destFolder, newFileName)
    if defaultPath != fullPath :
        print("File already exist in the disk, new path: " + fullPath)
    print("Download in progress. File size: " + sizeof_file(int(file['fileSize'])))

    step = 104857600//1048576
    fsize = int(file['fileSize'])//1048576

    file = open(fullPath, "wb+")
    downloader = MediaIoBaseDownload(file, copiedFileMedia, chunksize=104857600)  # change chunksize here
    done = False

    pbar = tqdm(desc='Downloading', unit='MB', total=fsize)
    while done is False:
        status, done = downloader.next_chunk()
        pbar.update(step)
    pbar.close()
    file.close()
    print("\nDownload completed : " + newFileName)

def delete_file(drive, id):
    drive.auth.service.files().delete(fileId=id).execute()

#https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_file(num, suffix='B'):
    for unit in ['','K','M','G','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def generate_path_with_unique_filename(folder, filename):
    fullpath = folder + "\\" + filename
    if not os.path.exists(fullpath):
        return fullpath
    fileNumber = 1
    while(os.path.exists(fullpath)):
        fullpath = folder + "\\" + str(fileNumber) + filename
        fileNumber+=1
    return fullpath