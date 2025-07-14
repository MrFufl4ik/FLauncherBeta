import os.path


def getDataFolder() -> str:
    data_folder: str = f"{os.getcwd()}/data"
    if not os.path.exists(data_folder): os.makedirs(data_folder)
    return data_folder

def getPlayerDataJsonFile() -> str: return f"{getDataFolder()}/player_data.json"
def getFTPDataJsonFile()    -> str: return f"{getDataFolder()}/ftp_data.json"
def getLinksDataJsonFile()  -> str: return f"{getDataFolder()}/links_data.json"