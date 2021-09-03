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
        # we initiate the resulting CSV file
        self.auctionslist = []
        print('Processor successfully initialized!')
        
    def process_data(self):
        
        auctionslist=[]
        for i in range(len(down.auction_links_and_categories)):
            soup = down.auction_links_and_categories[i][3]
            auctiondata=soup.findAll("div", {"class": "auction"})
            auctiondata=str(auctiondata[0])
            #for x,y in czech.items():
               # auctiondata = auctiondata.replace(x, y)#here the source-Czech dictionary is used
            auctiondata=auctiondata.replace('&quot;','"')
            #auctiondata=auctiondata.replace('"','')
            title=auctiondata[(auctiondata.index("title") + len("title")+3):]
            title=title[:title.index("category")-3]
            districtname=auctiondata[(auctiondata.index("district_name") + len("district_name")+3):(auctiondata.index("district_name") + len("district_name")+33)]
            districtname=districtname[:districtname.index('"')]
            if districtname=="' ')": districtname=np.nan#some auctions do not have this parameter, so it returns these characters
            regionname=auctiondata[(auctiondata.index("county_name")+ len("county_name")+3):(auctiondata.index("county_name")+ len("county_name")+33)]
            regionname=regionname[:regionname.index('"')]
            if regionname=="<th>Okres</th>\n<td v-text=":regionname=np.nan#like districtname, it is not everywhere
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
            link = down.auction_links_and_categories[i][0]
            category = down.auction_links_and_categories[i][1][0]
            try: subcategory = down.auction_links_and_categories[i][1][1]
            except: subcategory = "-"
            auction=[]
            auction.extend([auctioneer,phone,email,districtname,regionname,latitude,longitude,title,time[0],time[1],category,subcategory,number,estimated_price,reserve_price,link])
            auctionslist.append(auction)
            
            
            for i in range(len(auctionslist)):
                for j in range(len(down.regions_and_districts)):
                    for k in range(len(down.regions_and_districts[j][1])):
                        if down.regions_and_districts[j][1].count(auctionslist[i][4])==1:
                            auctionslist[i][4]=down.regions_and_districts[j][0]
            
            auctions = pd.DataFrame(auctionslist)
            auctions.columns = ["Auctioneer","Phone","E-mail","District","Region","Latitude","Longitude","Title of auction",
                    "Beginning_on","Beginning_at","Category","Subcategory","Auction_code","Estimated_price","Reserve_price",
                    "Link"]
            auctions.to_csv('auctionslist.csv', index = False)


