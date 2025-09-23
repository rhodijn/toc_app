#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import os, paramiko
from dotenv import dotenv_values
from modules.jsonhandler import *

SECRETS = dotenv_values('.env')


def upload_pdf(processing: dict, filepath: str, lib: str) -> dict:
    """
    upload toc-file (pdf) to remote server (if file  is not online yet)

    parameters:
    processing: dict = logging info of the currently processed record
    filepath: str = path to local file (including file name)
    lib: str = remote path to files of library (winterthur or waedenswil)

    returns:
    processing: dict = logging info of the currently processed record
    """
    config = load_json('config.json', 'd')
    remote_files : list = []

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=SECRETS['FTP_URL'],
        port=config['ftp']['port'],
        username=SECRETS['FTP_USER'],
        password=SECRETS['FTP_PASS'],
        look_for_keys=False
    )

    sftp_client = ssh_client.open_sftp()

    remote_files = sftp_client.listdir(config['path']['r'] + config['library'][lib])

    if f"{processing['mms_id']['nz']}.pdf" in remote_files:
        processing['messages'].append('file already online')
    else:
        try:
            sftp_client.put(filepath, f"{config['path']['r']}{config['library'][lib]}{processing['mms_id']['nz']}.pdf")
            url = f"https://{SECRETS['FTP_URL']}/{config['path']['r']}{config['library'][lib]}{processing['mms_id']['nz']}.pdf"
            processing.update({'file_uploaded': True, 'url': url})
            processing['filename'].update({'remote': url.split('/')[-1]})
            processing['messages'].append('pdf uploaded')
        except Exception as e:
            processing['messages'].append(f"error: {e} occurred")

    sftp_client.close()
    ssh_client.close()

    return processing


def rm_file(processing: dict, filepath: str) -> dict:
    """
    delete the local toc-file

    parameters:
    processing: dict = logging info of the currently processed record
    filepath: str = path to local file (including file name)

    returns:
    processing: dict = logging info of the currently processed record
    """    
    if os.path.exists(filepath):
        os.remove(filepath)
        processing.update({'file_deleted': True})
        processing['messages'].append('local file deleted')
    else:
        processing['messages'].append('local file not found')

    return processing