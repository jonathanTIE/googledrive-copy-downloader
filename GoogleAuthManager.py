from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def create_credential(typeOfAuth):
    if typeOfAuth == 1:
        from GoogleAuthV1 import auth_and_save_credential
    if typeOfAuth == 2:
        from GoogleAuthV2 import auth_and_save_credential
    auth_and_save_credential()


# Authentication + token creation
def create_drive_manager():  # TODO Use GoogleAuthV4
    gAuth = GoogleAuth()
    try:
        authorize_from_credential(gAuth)
    except:
        typeOfAuth = 0  # selection of method of auth
        while typeOfAuth != 1 and typeOfAuth != 2:
            typeOfAuth = int(input("type 1 for method 1, type 2 for method 2"))
            print(typeOfAuth)
            print("bbb")
        print("aaaaa")
        create_credential(typeOfAuth)
        authorize_from_credential(gAuth)

    drive: GoogleDrive = GoogleDrive(gAuth)
    return drive


def authorize_from_credential(gAuth):
    gAuth.LoadCredentialsFile("credentials.txt")  # TODO : faire un os.system.exist
    if gAuth.access_token_expired:
        gAuth.Refresh()
        print("token refreshed !")
        gAuth.SaveCredentialsFile("credentials.txt")
    gAuth.Authorize()
    print("authorized !")
