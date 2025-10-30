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
from modules.json_handler import *

SECRETS = dotenv_values('.env')


def upload_pdf(filename: str, lib: str, network_id: int) -> str:
    """
    upload toc-file (pdf) to remote server (if file is not online yet)

    parameters:
    filename: str = file name of the local file
    lib: str = code for the library
    network_id: str = network id of the bibliographic record
    """
    CONFIG = load_json('config.json', 'd')
    remote_files : list = []
    url = None

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=SECRETS['FTP_URL'],
        port=CONFIG['ftp']['port'],
        username=SECRETS['FTP_USER'],
        password=SECRETS['FTP_PASS'],
        look_for_keys=False
    )

    sftp_client = ssh_client.open_sftp()

    remote_files = sftp_client.listdir(CONFIG['path']['r'] + CONFIG['library'][lib])

    if f"{network_id}.pdf" not in remote_files:
        try:
            sftp_client.put(f"{CONFIG['path']['u']}{filename}", f"{CONFIG['path']['r']}{CONFIG['library'][lib]}{network_id}.pdf")
            url = f"https://{SECRETS['FTP_URL']}/{CONFIG['path']['r']}{CONFIG['library'][lib]}{network_id}.pdf"
        except:
            url = False
        else:
            if os.path.exists(f"{CONFIG['path']['u']}{filename}"):
                os.remove(f"{CONFIG['path']['u']}{filename}")

    sftp_client.close()
    ssh_client.close()
    return url