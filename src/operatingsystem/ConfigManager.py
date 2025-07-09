import os.path


def getDataFolder():
    data_folder: str = f"{os.getcwd()}/data"
    if not os.path.exists(data_folder): os.makedirs(data_folder)
    return data_folder

def getPlayerDataJsonFile():
    player_data_json_file: str = f"{getDataFolder()}/player_data.json"
    return player_data_json_file

def getFTPJsonFile():
    ftp_data_json_file: str = f"{getDataFolder()}/ftp_data.json"
    return ftp_data_json_file
