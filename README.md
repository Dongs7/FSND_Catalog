# FSND P4 - Item Catalog
Build an Item Catalog application

![](https://github.com/Dongs7/img/blob/master/catalog_1.png)

## Requirements
* Python 2.7.12
* Vagrant
* Oracle Virtual Box
* Flask
* SQLalchemy
* SQLite3
* Flask-Login
* Flask-Bootstrap
* Flask-Uploads
* Flask-WTF
* OAuth2Client
* Twitter Bootstrap

## Folder
[instance]          - contains app config, credential files - ignored
[project]  
|________[api]      - contains api related files
|________[catalog]  - contains catalog related files
|________[template] - contains html files
|________[users]    - contains user related files
|________[db]       - contains model, db files
|________[static]   - contains static files (css/js/images..) - ignored
run.py              - Start the application

## How to run this program
Run vagrant

Run this program by typing the following command in the terminal:

$ python run.py, then use localhost:8000

Functions
 - User can log in using google oauth2 or register/ login users locally
 ![](https://github.com/Dongs7/img/blob/master/sign_1.png)

 - Indicate which item is recently added
 ![](https://github.com/Dongs7/img/blob/master/add_1.png)

 - Only authorized users can access to certain pages

 - Authorized users can add items to catalog

 - Authorized users can only modify/delete the item content they create
   (Edit/ Delete buttons will be disabled when trying to modify others' items)

 - Authorized users can obtain catalog/item information in JSON format
    - catalog information - localhost:8000/api/catalog
    - item information - localhost:8000/api/items
![](https://github.com/Dongs7/img/blob/master/api_1.png)
![](https://github.com/Dongs7/img/blob/master/api_2.png)
