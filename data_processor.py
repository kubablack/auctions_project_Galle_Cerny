import pandas as pd
import numpy as np

class DataProcessor:
    '''
    This class iterates over all soup objects returned by data scraper and collects following information about every auction:
    1) auctioneer, his/her phone and e-mail address
    2) the municipality and region (kraj) where the auction is held and GPS coordinates of the point
    3) title - what is being auctioned
    4) time when the auction begins
    5) category and subcategory to which the auctioned object belongs
    6) unique code of the auction
    7) Reserve price (vyvolávací cena) and estimated price (odhadnutá cena) of the auctioned object
    8) Link to the auction in the registry 
    '''
    def __init__(self):
        # we initiate the lists for data within particular methods
        self.auctionslist = []
        print('Processor successfully initialized!')
        print(' ')
        print(DataProcessor.__doc__)
        
    def process_data(self,data_auctions,data_location):
        czech = {'\\u00e1': 'á',"\\u010d":"č","\\u010f":"ď","\\u00e9":"é","\\u011b":"ě","\\u00ed":"í","\\u0148":"ň",
                 "\\u00f3":"ó","\\u0159":"ř","\\u0161":"š","\\u0165":"ť","\\u00fa":"ú","\\u016f":"ů","\\u00fd":"ý",
                 "\\u017e":"ž","\\u00c1":"Á","\\u00c4":"Ä","\\u010c":"Č","\\u010e":"Ď","\\u00c9":"É","\\u011a":"Ě",
                 "\\u00cd":"Í","\\u0147":"Ň","\\u00d3":"Ó","\\u0158":"Ř","\\u0160":"Š","\\u0164":"Ť","\\u00da":"Ú",
                 "\\u016e":"Ů","\\u00dd":"Ý","\\u017d":"Ž"}
        #necessary to translate groups of characters from the source code to Czech characters
        for i in range(len(data_auctions)):
            soup = data_auctions[i][3]
            auctiondata=soup.findAll("div", {"class": "auction"})
            auctiondata=str(auctiondata[0])
            for x,y in czech.items():
                auctiondata = auctiondata.replace(x, y)#here the source-Czech dictionary is used
            auctiondata=auctiondata.replace('&quot;','"')
            #auctiondata=auctiondata.replace('"','')
            title=auctiondata[(auctiondata.index("title") + len("title")+3):]
            title=title[:title.index("category")-3]
            districtname=data_auctions[i][2]
            regionname="-"
            for el in data_location:
                if districtname in el[1]:
                    regionname=el[0]
            auctioneer=auctiondata[(auctiondata.index("auctioneer_office") + len("auctioneer_office")+30):]
            auctioneer=auctioneer[:auctioneer.index("addresses")-3].replace(" ","_")
            auctioneer=" ".join(auctioneer.split("_", 2)[:2])
            number=auctiondata[(auctiondata.index('voluntary')-17):(auctiondata.index('voluntary')-3)].replace(':','').replace('"', '')
            estimated_price=auctiondata[(auctiondata.index("estimated_price") + len("estimated_price")+2):]
            estimated_price=estimated_price[:estimated_price.index("item_price")-2]
            reserve_price=auctiondata[auctiondata.index("item_price")+12:]
            reserve_price=reserve_price[:reserve_price.index("minimal_bid")-2]
            time=auctiondata[auctiondata.index("start_at")+11:auctiondata.index("start_at")+27]
            time=time.split("T")
            location=auctiondata[auctiondata.index("location_coords")+29:auctiondata.index("location_coords")+70]
            latitude=location[:10]
            if latitude[0]!="4" and latitude[0]!="5":#some do not provide coordinates, this is just filtering
                latitude=np.nan
            longitude=location[23:33]
            if longitude[0]!="1": #like latitude
                longitude=np.nan
            phone=auctiondata[auctiondata.index("phone_number")+len("phone_number")+3:auctiondata.index("phone_number")+len("phone_number")+12]
            email=auctiondata[auctiondata.index("email")+8:auctiondata.index("children")-3]                        
            link = data_auctions[i][0]
            category = data_auctions[i][1][0]
            try: subcategory = data_auctions[i][1][1]
            except: subcategory = "-"
            auction=[]
            auction.extend([auctioneer,phone,email,districtname,regionname,latitude,longitude,title,time[0],time[1],category,subcategory,number,estimated_price,reserve_price,link])
            self.auctionslist.append(auction)
        for i in range(len(self.auctionslist)):
            for j in range(len(data_location)):
                for k in range(len(data_location[j][1])):
                    if data_location[j][1].count(self.auctionslist[i][4])==1:
                        self.auctionslist[i][4]=data_location[j][0]
        auctions = pd.DataFrame(self.auctionslist)
        auctions.columns = ["Auctioneer","Phone","E-mail","District","Region","Latitude","Longitude","Title of auction",
                            "Beginning_on","Beginning_at","Category","Subcategory","Auction_code","Estimated_price","Reserve_price",
                            "Link"]
        auctions.to_csv('auctionslist.csv', index = False)
        print("Data successfully processed!")
