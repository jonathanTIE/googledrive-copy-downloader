from pydrive.auth import GoogleAuth
def auth_and_save_credential():
    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gAuth.SaveCredentialsFile("credentials.txt")