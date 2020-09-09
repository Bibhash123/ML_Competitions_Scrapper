import Scrapper



if __name__ == '__main__':
        scrap = Scrapper.Scrapper()
        scrap.kaggle_scrap()
        scrap.av_scrap()
        scrap.hackerearth_scrap()
        del scrap

