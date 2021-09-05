#!pip install descartes
#!pip install pyshp
from descartes import PolygonPatch
import shapefile
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

sf=shapefile.Reader('districts')
reg=down.regions_and_districts

regionlist=[]#this is for map of regions
countlist=[]
avglist=[]
startindices=[1,2,14,21,28,31,38,42,47,51,56,63,68,74]
endindices=[1,13,20,27,30,37,41,46,50,55,62,67,73,77]
for i in range(len(reg)):
    regionlist.append(reg[i][0])
for i in range(len(reg)):
    count=auctions.Region[auctions.Region == regionlist[i]].count()
    countlist.append(count)
for i in range(len(reg)):
    avgprice=auctions.Estimated_price[auctions.Region == regionlist[i]].mean()
    avglist.append(avgprice)

#this is for map of districts
districtslist=[]
districtslist.append(reg[0][1][0])
for i in range(len(reg[11][1])):
    districtslist.append(reg[11][1][i])
for i in range(len(reg[1][1])):
    districtslist.append(reg[1][1][i])
for i in range(len(reg[10][1])):
    districtslist.append(reg[10][1][i])
for i in range(len(reg[3][1])):
    districtslist.append(reg[3][1][i])
for i in range(len(reg[12][1])):
    districtslist.append(reg[12][1][i])
districtslist[30]=reg[12][1][1]#Codes for Děčín and Chomutov are switched, as opposed to the list
districtslist[31]=reg[12][1][0]
for i in range(len(reg[6][1])):
    districtslist.append(reg[6][1][i])
for i in range(len(reg[5][1])):
    districtslist.append(reg[5][1][i])
for i in range(len(reg[9][1])):
    districtslist.append(reg[9][1][i])
for i in range(len(reg[4][1])):
    districtslist.append(reg[4][1][i])
districtslist[50]=reg[4][1][2]
districtslist[51]=reg[4][1][0]
districtslist[52]=reg[4][1][1]
for i in range(len(reg[2][1])):
    districtslist.append(reg[2][1][i])
districtslist[56]=reg[2][1][2]
districtslist[57]=reg[2][1][3]
districtslist[58]=reg[2][1][1]
for i in range(len(reg[8][1])):
    districtslist.append(reg[8][1][i])
districtslist[62]=reg[8][1][3]
districtslist[65]=reg[8][1][4]
districtslist[66]=reg[8][1][0]
for i in range(len(reg[7][1])):
    districtslist.append(reg[7][1][i])
for i in range(len(reg[13][1])):
    districtslist.append(reg[13][1][i])
districtslist[73]=reg[13][1][3]
districtslist[74]=reg[13][1][0]
districtslist[75]=reg[13][1][1]
districtslist[76]=reg[13][1][2]

d_countlist=[]
d_avglist=[]
for i in range(0,77):
    d_count=math.log(auctions.District[auctions.District == districtslist[i]].count())#log, because Prague would make everything else almost black
    d_countlist.append(d_count)
for i in range(0,77):
    d_avgprice=auctions.Estimated_price[auctions.District == districtslist[i]].mean()
    d_avglist.append(d_avgprice)

fig = plt.figure(figsize=(12,12)) 
ax = fig.gca()
for i in range(len(districtslist)):
    shade=int(d_countlist[i]/max(d_countlist)//0.01)#making integers to put in colour codes
    if shade>9:fillcolour="#{}{}{}".format(shade,shade,shade)
    else:fillcolour="#0{}0{}0{}".format(shade,shade,shade)#one-digit numbers would not work in the code
    poly=sf.shape(i).__geo_interface__
    ax.add_patch(PolygonPatch(poly, fc=fillcolour, ec='#002222', alpha=1, zorder=2 ))
ax.axis('scaled')
plt.axis('off')
plt.title("Amount of auctions by district",fontsize="20")
plt.legend(['The lighter a district is, the more auctions are there'])
plt.show()

fig = plt.figure(figsize=(12,12)) 
ax = fig.gca()
for i in range(len(districtslist)):
    shade=int(d_avglist[i]/max(d_avglist)//0.01)#making integers to put in colour codes
    if shade>9:fillcolour="#00{}00".format(shade)
    else:fillcolour="#000{}00".format(shade)
    poly=sf.shape(i).__geo_interface__
    ax.add_patch(PolygonPatch(poly, fc=fillcolour, ec='#002222', alpha=1, zorder=2 ))
ax.axis('scaled')
plt.axis('off')
plt.title("Average estimated price of subject of auction by district",fontsize="20")
plt.legend(['The lighter a district is, the more auctions are there'])
plt.show()

fig = plt.figure(figsize=(12,12)) 
ax = fig.gca()

for i in range(len(down.regions_and_districts)):
    for j in range(startindices[i]-1,endindices[i]):
        shade=int(countlist[i]/max(countlist)//0.01)#making integers to put in colour codes
        if shade>9:fillcolour="#{}{}{}".format(shade,shade,shade)
        else:fillcolour="#0{}0{}0{}".format(shade,shade,shade)#one-digit numbers would not work in the code
        poly=sf.shape(j).__geo_interface__
        ax.add_patch(PolygonPatch(poly, fc=fillcolour, ec='#000000', alpha=1, zorder=2 ))
ax.axis('scaled')
plt.axis('off')
plt.title("Amount of auctions by region",fontsize="20")
plt.legend(['The lighter a district is, the more auctions are there'])
plt.show()#The lighter the colour, the more auctions there are. The region with most auctions always has shade #999999,
#other regions are coloured by their share of auctions: 10% of maximum has shade #101010, 52% has shade #525252 etc.

fig = plt.figure(figsize=(12,12)) 
ax = fig.gca()

for i in range(len(down.regions_and_districts)):
    for j in range(startindices[i]-1,endindices[i]):
        shade=int(avglist[i]/max(avglist)//0.01)
        if shade>9:fillcolour="#00{}00".format(shade)
        else:fillcolour="#000{}00".format(shade)
        poly=sf.shape(j).__geo_interface__
        ax.add_patch(PolygonPatch(poly, fc=fillcolour, ec='#000000', alpha=1, zorder=2 ))
ax.axis('scaled')
plt.axis('off')
plt.title("Average estimated price of subject of auction by region",fontsize="20")
plt.legend(['The lighter a district is, the more auctions are there'])
plt.show()#The lighter the colour, the more expensive auctions on average there are. Coloured by share of maximum like before. 

