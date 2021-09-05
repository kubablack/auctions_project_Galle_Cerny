![alt text](https://github.com/kubablack/auctions_project_Galle_Cerny/blob/main/logo.png)

# <center>Auctions</center>
#### <center>Antonín Galle, Jakub Černý</center>

This project works with data from https://www.portaldrazeb.cz and its goal is to scrape actual data about future auctions, process them into suitable format and provide insights for potential bidders. It incorporates three parts: a scraper, a processor and an explorer/filter. Every part has its own description in the main jupyter notebook **auctions.ipynb** and also within corresponding *.py* files. 

The scraper and the processor are written in form of OOP and particular classes are then imported from respective scripts. The last part is not designed as OOP, it is only written in separate scripts and then executed in the main file using *%run*. 

The data does not provide many quantitative variables which could be analysed by statistical or econometric methods and therefore we primarily focus on our first idea, i.e. creating a kind of dashboard displaying the data about auctions for someone who might be interested in taking part in one of them or looking for a certain type of good.
