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


def upload_pdf(filename: str, lib: str, network_id: int) -> dict:
    """
    upload toc-file (pdf) to remote server (if file  is not online yet)

    parameters:
    filename: str = path to local file (including file name)
    lib: str = remote path to files of library (winterthur or waedenswil)
    """
    config = load_json('config.json', 'd')
    remote_files : list = []
    url = None

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

    if f"{network_id}.pdf" not in remote_files:
        try:
            sftp_client.put(f"upload/{filename}", f"{config['path']['r']}{config['library'][lib]}{network_id}.pdf")
            url = f"https://{SECRETS['FTP_URL']}/{config['path']['r']}{config['library'][lib]}{network_id}.pdf"
            if os.path.exists(f"upload/{filename}"):
                os.remove(f"upload/{filename}")
        except:
            pass

    sftp_client.close()
    ssh_client.close()

    return url