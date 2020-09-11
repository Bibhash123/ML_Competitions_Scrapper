## ML_Competitions_Scrapper
- This project scraps the sites Kaggle, Analytics Vidhya and Hackerearth for active and upcoming competitions
- All competitons are written to an excel file
- The competitions that are new i.e didn't previously exist in the record are marked in Green
## Files
- The file Scrapper.py is a class file that contains a class named Scrapper consisting of all required functions
- The file competions_scrapper.py is the main execuatble file
- The file competitions.xlsx holds information about the competitions obtained in previous scan
## How to Use the class Scrapper
- import the class Scrapper
- create an object of the class ( syntax: scrap = Scrapper())
- The class contains functions kaggle_scrap, av_scrap and hackerearth_scrap
- Call the respective function corresponding to the site you want to scrap (syntax: scrap.kaggle_scrap())
