### Dynamic scraper
#### Goal
As the title suggests, the first section incorporates a data scraper. Its goal is to crawl through https://www.portaldrazeb.cz and to collect actual data about auctions and auctioneers. It also scrapes lists of auction attributes which we will subsequently use to filter the auctions with respect to location, type, etc.  
#### Problem
The problem is that the webpage has dynamic content and therefore it is not possible to easily extract the data we need since the "static" source code differs from the "dynamic" one. The website also does not provide API (it actually does, however, not for us and not for the purposes we need). 
#### Solution
We need to use proper methods to handle the dynamic content - our solution is the installation of package selenium and setting up a Google Chrome webdriver. We basically open the webpage, collect its source code and navigate between pages. Thanks to this package (and the webdriver which is also included in the GitHub repository) we manage to download all the data we need. More detailed description of particular methods can be found in the class docstring and in the comments.
