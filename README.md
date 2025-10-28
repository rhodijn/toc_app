# TOC Web App
```
###################
##                 ##
##               ##
  ######       ##
    ##       ######
  ##               ##
##                 ##
  ###################
```
When a table of contents should be added to enrich a bibliographic record, this script automates parts of the process. It uploads the pdf-file to a public server and generates the contents of the 856 field which must then be copied into the bibliographic record in Alma, generating a link in the discovery system.

## Description

The script operates from a website using Flask. There is a web form which accepts pdf-files and loads them to a public server.

## Getting Started

### Dependencies

The following python modules are required for the script to run (a `requirements.txt` is included):
* dotenv
* flask
* json
* paramiko
* os
* requests