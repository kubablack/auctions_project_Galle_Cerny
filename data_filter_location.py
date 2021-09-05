import pandas as pd
import ipywidgets as widgets
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator # to ensure integer ticks in a plot
regions_plus_districts = [['Hlavní město Praha', ['Praha']],
 ['Jihočeský kraj',
  ['České Budějovice',
   'Český Krumlov',
   'Jindřichův Hradec',
   'Písek',
   'Prachatice',
   'Strakonice',
   'Tábor']],
 ['Jihomoravský kraj',
  ['Blansko',
   'Břeclav',
   'Brno-město',
   'Brno-venkov',
   'Hodonín',
   'Vyškov',
   'Znojmo']],
 ['Karlovarský kraj', ['Cheb', 'Karlovy Vary', 'Sokolov']],
 ['Kraj Vysočina',
  ['Havlíčkův Brod', 'Jihlava', 'Pelhřimov', 'Třebíč', 'Žďár nad Sázavou']],
 ['Královéhradecký kraj',
  ['Hradec Králové', 'Jičín', 'Náchod', 'Rychnov nad Kněžnou', 'Trutnov']],
 ['Liberecký kraj', ['Česká Lípa', 'Jablonec nad Nisou', 'Liberec', 'Semily']],
 ['Moravskoslezský kraj',
  ['Bruntál',
   'Frýdek-Místek',
   'Karviná',
   'Nový Jičín',
   'Opava',
   'Ostrava-město']],
 ['Olomoucký kraj', ['Jeseník', 'Olomouc', 'Přerov', 'Prostějov', 'Šumperk']],
 ['Pardubický kraj', ['Chrudim', 'Pardubice', 'Svitavy', 'Ústí nad Orlicí']],
 ['Plzeňský kraj',
  ['Domažlice',
   'Klatovy',
   'Plzeň-jih',
   'Plzeň-město',
   'Plzeň-sever',
   'Rokycany',
   'Tachov']],
 ['Středočeský kraj',
  ['Benešov',
   'Beroun',
   'Kladno',
   'Kolín',
   'Kutná Hora',
   'Mělník',
   'Mladá Boleslav',
   'Nymburk',
   'Praha-východ',
   'Praha-západ',
   'Příbram',
   'Rakovník']],
 ['Ústecký kraj',
  ['Chomutov',
   'Děčín',
   'Litoměřice',
   'Louny',
   'Most',
   'Teplice',
   'Ústí nad Labem']],
 ['Zlínský kraj', ['Kroměříž', 'Uherské Hradiště', 'Vsetín', 'Zlín']]]
regions_and_districts = pd.DataFrame(regions_plus_districts,columns=["Region","Districts"])
auctions = pd.read_csv("auctionslist.csv")
auctions=auctions.set_index("Auction_code")
auctions = auctions[["Title of auction","Category","Subcategory","Beginning_on","Beginning_at","Estimated_price","Reserve_price","Link","Auctioneer","Phone","E-mail","Region","District","Latitude","Longitude"]]
# formatting auction links to html (in order to create hyperlinks)
auctions['Link'] = auctions['Link'].apply(lambda x: f'<a href="{x}"> more info here </a>'.format(x))
# preparing lists of regions and districts (values for dropdown menu)
regions = ["All"]
for i in regions_and_districts["Region"]:
    regions.append(i)
districts = ["All"]
for i in regions_and_districts["Districts"].explode():
    districts.append(i)
# defining function which generates unique values of a column within data frame
def unique_values_and_their_counts(df, column):
    values = df[column].value_counts().index.tolist()
    counts = df[column].value_counts().tolist()
    values_plus_counts = [values[i]+": "+str(counts[i]) for i in range(len(values))] # this is used as label in pie chart
    return values, counts, values_plus_counts
# controlling output
output = widgets.Output() 
category_output = widgets.Output()
auctioneer_output = widgets.Output()
# setting up the widgets
region_widget = widgets.Dropdown(
    options=regions,
    value='All',
    description='Region:')
district_widget = widgets.Dropdown(
    options=districts,
    value='All',
    description='District:')

# combining effects of both widgets
def common_filtering(region, district):
    output.clear_output() # necessary to prevent from cummulating multiple outputs
    category_output.clear_output()
    auctioneer_output.clear_output()
    if (region == "All") & (district == "All"):
        common_filter = auctions
        
    elif (region == "All"):
        common_filter = auctions[auctions["District"] == district]
        
    elif (district == "All"):
        common_filter = auctions[auctions["Region"] == region]
        
    else:
        common_filter = auctions[(auctions["Region"] == region) & 
                                  (auctions["District"] == district)]
    with output:
        display(HTML(common_filter.to_html(escape=False)))
    with category_output:
        plt.pie(unique_values_and_their_counts(common_filter,"Subcategory")[1], 
                labels = unique_values_and_their_counts(common_filter,"Subcategory")[2])
        plt.show()    
    with auctioneer_output:
        fig, ax = plt.subplots()
        plt.style.use('ggplot')

        names = unique_values_and_their_counts(common_filter,"Auctioneer")[0][:8]
        number_of_auctions = unique_values_and_their_counts(common_filter,"Auctioneer")[1][:8]

        position = range(len(names))

        plt.bar(position, number_of_auctions, color='green')
        plt.xlabel("Auctioneer")
        plt.ylabel("Number of auctions")
        plt.title("Auctioneers with most auctions")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xticks(position, names)

        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.show()
        
def dropdown_region_eventhandler(change):
    common_filtering(change.new, district_widget.value)
def dropdown_district_eventhandler(change):
    common_filtering(region_widget.value, change.new)
region_widget.observe(dropdown_region_eventhandler, names='value')
district_widget.observe(dropdown_district_eventhandler, names='value')

# creating layout for widgets and output tabs
input_widgets = widgets.HBox([region_widget,district_widget])
tab = widgets.Tab([output, category_output,auctioneer_output])
tab.set_title(0, 'Auctions')
tab.set_title(1, 'Categories')
tab.set_title(2, 'Auctioneers')

# showing the result
display(input_widgets)
display(tab)