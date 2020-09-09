from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd



class Scrapper:
        def __init__(self):
                self.driver = webdriver.Firefox()
                self.write_path = "./competitions.xlsx"
                self.writer = pd.ExcelWriter(self.write_path,engine = 'xlsxwriter')
                
                try:
                        prev = pd.read_excel('./Competitions.xlsx',sheet_name="Hackerearth")
                        self.hackerearth_not_in = list(prev.Title.map(str.strip))
                except:
                        self.hackerearth_not_in = []
                        
                try:
                        prev = pd.read_excel('./Competitions.xlsx',sheet_name="Kaggle")
                        self.kaggle_not_in = list(prev.Competition.map(str.strip))
                except:
                        self.kaggle_not_in = []

                try:
                        prev = pd.read_excel('./Competitions.xlsx',sheet_name="AV")
                        self.av_not_in = list(prev.Title.map(str.strip))
                except:
                        self.av_not_in = []
                
        def __del__(self):
                
                self.writer.save()
                
                self.writer = pd.ExcelWriter(self.write_path,engine = 'xlsxwriter')
                
                self.check_new(page="Kaggle")

                self.check_new(page="Hackerearth")

                self.check_new(page="AV")
                

                self.writer.save()
                print("Writing to file: competitons.xlsx")
                
                self.driver.close()
                self.driver.quit()
                
                print("Successfully scrapped websites")
               
        def check_new(self,page):
                print("Checking For new Competitions")
                if page=="Hackerearth":
                        df = pd.read_excel(self.write_path,sheet_name=page)
                        
                        def add_color(s,app_not_in,l):
                                
                                if s.Title.strip() not in app_not_in:
                                        return ['background-color:green']*l
                                else:
                                        return ['background-color:white']*l
                                
                        df1 = df.style.apply(add_color,app_not_in = self.hackerearth_not_in,l=df.shape[1],axis=1)
                
                        df1.to_excel(self.writer,sheet_name=page,index=False)
                        worksheet = self.writer.sheets[page]
                        
                        for idx, column in enumerate(df):
                                
                                series = df[column]
                                max_len = max((
                                        series.astype(str).map(len).max(),
                                        len(str(series.name))
                                        ))+1
                                worksheet.set_column(idx,idx,max_len)
                elif page=="Kaggle":
                        df = pd.read_excel(self.write_path,sheet_name=page)
                        
                        def add_color(s,app_not_in,l):
                                
                                if s.Competition.strip() not in app_not_in:
                                        return ['background-color:green']*l
                                else:
                                        return ['background-color:white']*l
                                
                        df1 = df.style.apply(add_color,app_not_in = self.kaggle_not_in,l=df.shape[1],axis=1)
                
                        df1.to_excel(self.writer,sheet_name=page,index=False)
                        worksheet = self.writer.sheets[page]
                        
                        for idx, column in enumerate(df):
                                
                                series = df[column]
                                max_len = max((
                                        series.astype(str).map(len).max(),
                                        len(str(series.name))
                                        ))+1
                                worksheet.set_column(idx,idx,max_len)
                
                
                elif page=="AV":
                        df = pd.read_excel(self.write_path,sheet_name=page)
                        
                        def add_color(s,app_not_in,l):
                                
                                if s.Title.strip() not in app_not_in:
                                        return ['background-color:green']*l
                                else:
                                        return ['background-color:white']*l
                                
                        df1 = df.style.apply(add_color,app_not_in = self.av_not_in,l=df.shape[1],axis=1)
                
                        df1.to_excel(self.writer,sheet_name=page,index=False)
                        worksheet = self.writer.sheets[page]
                        
                        for idx, column in enumerate(df):
                                
                                series = df[column]
                                max_len = max((
                                        series.astype(str).map(len).max(),
                                        len(str(series.name))
                                        ))+1
                                worksheet.set_column(idx,idx,max_len)
                
                      
         

        def kaggle_scrap(self):
                print(".....Scrapping Kaggle.....")
                
                try:
                        self.driver.get("https://kaggle.com/competitions")
                except:
                        print("Can't connect to kaggle")
                        return
                                

                source = self.driver.page_source
                soup = BeautifulSoup(source,'html.parser')

                competitions = soup.select("a[href^=\/c\/]")[2:]
                

                

                df  = pd.DataFrame(columns=["Competition","Description","Type","Time Left","Prize"])

                for idx,c in enumerate(competitions):
                        head = c.select_one('div[class*=primary-text]').next_element
                        desc = head.next_element.next_element
                        info = desc.next_element.next_element
                        info = info.split('•')
                        typ = info[0]
                        time = info[1]
                        prize = c.nextSibling
                        df = df.append({
                                'Competition':head,
                                'Description':desc,
                                'Type':typ,
                                'Time Left':time,
                                'Prize':prize.text},ignore_index=True);

                df.to_excel(self.writer,sheet_name = "Kaggle",index=False)
                worksheet = self.writer.sheets["Kaggle"]

                for idx, column in enumerate(df):
                        series = df[column]
                        max_len = max((
                                series.astype(str).map(len).max(),
                                len(str(series.name))
                                ))+1
                        worksheet.set_column(idx,idx,max_len)
                
                print(".....finished scrapping kaggle....")
                
        def av_scrap(self):
                print("......Scrapping Analytics Vidhya......")
                try:
                        self.driver.get("https://datahack.analyticsvidhya.com/contest/all/")
                except:
                        print("Can't connect to Analytics Vidhya")
                        return
                a = self.driver.find_element_by_link_text('All Contests')
                a.click()

                source = self.driver.page_source
                soup = BeautifulSoup(source,'html.parser')

                upcoming = soup.find(id="upcoming")
                upcoming = upcoming.findAll('div',{'class':'card'})
                
                df = pd.DataFrame(columns=["Type","Title","Schedule","Prizes"])
                
                for u in upcoming:
                        name = u.find('h3',{'class':'card-title'})
                        schedule = u.find('div',{'class':'card-body events-schedule'})
                        prizes = u.find('div',{'class':'card-footer'})
                        df = df.append({
                                "Type":"Upcoming",
                                'Title':name.text,
                                'Schedule':schedule.text,
                                'Prizes':prizes.text},ignore_index=True)
                # get all active
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                while True:
                        try:
                                a = self.driver.find_element_by_id('showMoreBtnActive')
                        except:
                                break
                        try:
                                a.click()
                        except:
                                break
                                
                source = self.driver.page_source
                soup = BeautifulSoup(source,'html.parser')
                
                active = soup.find(id="active")
                active = active.findAll('div',{'class':'card'})
                for a in active:
                        name = a.find('h3',{'class':'card-title'})
                        schedule = a.find('div',{'class':'card-body events-schedule'})
                        prizes = a.find('div',{'class':'card-footer'})
                        if prizes.text!="Knowledge Sharing" and prizes.text!="Practice Problem" and (prizes.text!="Knowledge and Learning"):
                                df = df.append({
                                'Type':"Active",
                                'Title':name.text,
                                'Schedule':schedule.text,
                                'Prizes':prizes.text},ignore_index=True)
    
                if df.shape[0]!=0:
                        df.to_excel(self.writer,sheet_name = "AV",index=False)
                        worksheet = self.writer.sheets["AV"]

                        for idx, column in enumerate(df):
                                series = df[column]
                                max_len = max((
                                        series.astype(str).map(len).max(),
                                        len(str(series.name))
                                        ))+1
                                worksheet.set_column(idx,idx,max_len)
                print("......Finished Scrapping Analytics Vidhya......")


        def hackerearth_scrap(self):
                print("......Scrapping Hackerearth......")
                try:
                        self.driver.get('https://www.hackerearth.com/challenges/')
                except:
                        print("Can't connect to Hackerearth")
                        return

                source = self.driver.page_source
                soup = BeautifulSoup(source,'html.parser')

                active = soup.find('div',{'class':'ongoing challenge-list'})
                competitions = active.findAll('div',{'class':'challenge-card-modern'})
                
                df = pd.DataFrame(columns=["Type","Type-Challenge","Title","Time"])

                for c in competitions:
                        typ = c.find('div',{'class':'challenge-type light smaller caps weight-600'})
                        name = c.find('div',{'class':'challenge-name ellipsis dark'})
                        time=""
                        if typ.text.strip()!="CodeArena":
            
                                
                                days = c.find('div',{'id':'days','class':'inline-block align-left'})
                                days = days.text.split(':')
                                days[0]=''.join(days[0].split('\n'))
                                days[1] = ''.join(days[1].split('\n'))
                                days = ' '.join(days)

                                hours = c.find('div',{'id':'hours','class':'inline-block align-left'})
                                hours = hours.text.split(':')
                                hours[0]=''.join(hours[0].split('\n'))
                                hours[1] = ''.join(hours[1].split('\n'))
                                hours = ' '.join(hours)

                                minutes = c.find('div',{'id':'minutes','class':'inline-block align-left'})
                                minutes = minutes.text.split(':')
                                minutes[0]=''.join(minutes[0].split('\n'))
                                minutes[1] = ''.join(minutes[1].split('\n'))
                                minutes = ' '.join(minutes)
                                time = days+':'+hours+":"+minutes
                        df = df.append({
                                'Type':'Live',
                                'Type-Challenge':typ.text.strip(),
                                'Title':name.text,
                                'Time':time
                                },ignore_index=True)
                        
                upcoming = soup.find('div',{'class':'upcoming challenge-list'})
                competitions = upcoming.findAll('div',{'class':'challenge-card-modern'})

                for c in competitions:
                        typ = c.find('div',{'class':'challenge-type light smaller caps weight-600'})
                        name = c.find('div',{'class':'challenge-name ellipsis dark'})
                        time= c.find('div',{'class':'date less-margin dark'})
                        
                        df = df.append({
                                'Type':'Upcoming',
                                'Type-Challenge':typ.text.strip(),
                                'Title':name.text,
                                'Time':time.text
                                },ignore_index=True)
                
                        
                if df.shape[0]!=0:
                        df.to_excel(self.writer,sheet_name = "Hackerearth",index=False)
                        worksheet = self.writer.sheets["Hackerearth"]

                        for idx, column in enumerate(df):
                                
                                series = df[column]
                                max_len = max((
                                        series.astype(str).map(len).max(),
                                        len(str(series.name))
                                        ))+1
                                worksheet.set_column(idx,idx,max_len)    
                print("......Finished Scrapping Hackerearth.......")               
                        
                        
                     
                
                        
       
