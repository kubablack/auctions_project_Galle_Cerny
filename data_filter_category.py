import pandas as pd
import ipywidgets as widgets
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
auctions = pd.read_csv("auctionslist.csv")
auctions=auctions.set_index("Auction_code")
auctions = auctions[["Title of auction","Category","Subcategory","Beginning_on","Beginning_at","Estimated_price","Reserve_price","Link","Auctioneer","Phone","E-mail","Region","District","Latitude","Longitude"]]
# formatting auction links to html (in order to create hyperlinks)
auctions['Link'] = auctions['Link'].apply(lambda x: f'<a href="{x}"> more info here </a>'.format(x))
categories = ["All"] + auctions["Category"].unique().tolist()
subcategories =["All"] + auctions["Subcategory"].unique().tolist()
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
category_widget = widgets.Dropdown(
    options=categories,
    value='All',
    description='Category:')
subcategory_widget = widgets.Dropdown(
    options=subcategories,
    value='All',
    description='Subcategory:')

# combining effects of both widgets
def common_filtering(category, subcategory):
    output.clear_output() # necessary to prevent from cummulating multiple outputs
    category_output.clear_output()
    auctioneer_output.clear_output()
    if (category == "All") & (subcategory == "All"):
        common_filter = auctions
        
    elif (category == "All"):
        common_filter = auctions[auctions["Subcategory"] == subcategory]
        
    elif (subcategory == "All"):
        common_filter = auctions[auctions["Category"] == category]
        
    else:
        common_filter = auctions[(auctions["Category"] == category) & 
                                  (auctions["Subcategory"] == subcategory)]
    with output:
        display(HTML(common_filter.to_html(escape=False)))
    with category_output:
        plt.pie(unique_values_and_their_counts(common_filter,"Region")[1], 
                labels = unique_values_and_their_counts(common_filter,"Region")[2])
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
    common_filtering(change.new, subcategory_widget.value)
def dropdown_district_eventhandler(change):
    common_filtering(category_widget.value, change.new)
category_widget.observe(dropdown_region_eventhandler, names='value')
subcategory_widget.observe(dropdown_district_eventhandler, names='value')

# creating layout for widgets and output tabs
input_widgets = widgets.HBox([category_widget,subcategory_widget])
tab = widgets.Tab([output, category_output,auctioneer_output])
tab.set_title(0, 'Auctions')
tab.set_title(1, 'Regions')
tab.set_title(2, 'Auctioneers')

# showing the result
display(input_widgets)
display(tab)