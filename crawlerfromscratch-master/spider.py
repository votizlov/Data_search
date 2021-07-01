# This file contains core classes for the web crawler.
# Author: Kai Xu
# Date: 05/11/2016


from html.parser import HTMLParser  # for parsing HTML
from urllib.parse import urljoin  # for join two urls
from urllib.request import urlopen  # for GET request
from helper import clean, get_domain, valid, contain_static
from matplotlib import pyplot as plt
from mechanize import Browser
#from BeautifulSoup import BeautifulSoup


class HTMLParser(HTMLParser):
    '''
    HTML parser to fetch urls and show assests
    '''
    def __init__(self):
        super().__init__()
        self.failed = set([])
        self.titles = set([])
        self.isSuccess = False

    def handle_starttag(self, tag, attrs):
        '''
        Overrid of the default function to handle <a> and ??? tags
        TODO: update this comments when assest handle is done
        '''
        for key, val in attrs:
            if key == "href":
                if contain_static(val):  # handle static files
                    print("-", val)  # show the static file
                elif tag == "a":  # handle links
                    url = urljoin(self.url, val)  # append relative path to the root path
                    url = clean(url)  # clean up url
                    if valid(url, self.domain):
                        self.urls.append(url)  # append url to the return list
                else:
                    pass

    def run(self, url,failed):
        '''
        Run the parser and return links in this page
        '''
        self.url = url  # save root path
        self.domain = get_domain(url)  # get and save domain
        self.urls = []  # init return list

        # Open the url and parse it
        # FIXME:
        # There will be potential error when some website handshake is unsuccessful due to the SSL.
        # This is temporarly fixed by ignoring such failure but it should be further investiagted.
        try:
            response = urlopen(url)  # request and get response
            #br = Browser()
            #br.open(url)
            html = response.read().decode("utf-8")  # read and encode response; NOTE: decode is necessary for unicode
            #page = self.feed(html)  # parse the html file in string format
            #if(br.title() is None):
            #else:
            #self.titles.add(br.title())
            #print(br.title())
            self.isSuccess = True
        except KeyboardInterrupt:  # deal with Ctrl-C
            exit()
        except:
            self.failed.add(url)
            self.isSuccess = False
            print("Unexpected failure happens and the spider escapes.")

        return self.urls


class Spider(object):
    def __init__(self):
        self.visted = set([])
        self.to_visit = set([])
        self.failed = set([])
        self.visitedDepth = []
        self.parser = HTMLParser()
        self.count = 0
        self.CountOne = 0
        self.CountTwo = 0
        self.discovered_count = 0
        self.discovered = set([])
        self.dict = dict()
        self.titles = set([])
        self.treeLvl = set()

    def crawl(self, visited, to_visit,failed, target_url, currDepth, maxDepth):
        target_url = clean(target_url)  # clean target_url
        self.count += 1
        self.discovered_count -=1

        #if self.to_visit.__contains__(target_url):
        #    self.to_visit.remove(target_url)

        url = target_url  # get next url
        #print("The spider is visiting:", url, " at depth: ", currDepth)
        urls = self.parser.run(url,self.failed)  # parse the url

        if currDepth==1:
            self.CountOne += 1
        else:
            self.CountTwo += 1
        self.visted.add(url)
        self.treeLvl.add(currDepth)  # add this visted url to visted list


        #print("\nvisited: " + (str)(self.visted) + "\n to visit: "
        #      + (str)(self.discovered) + "\n failed " + (str)(self.parser.failed)
        #      + "\n step count: " + (str)(self.count))

        print("Iteration: " + (str)(self.count))
        print("Node count: " + (str)(len(self.visted)))
        print("First level: "+ str(self.CountOne))
        print("Second level: " + str(self.CountTwo))
        #print("To visit: " + str(self.discovered_count))
        #print(str(self.parser.titles))
        #print(str(self.treeLvl))
        #for t in range(len(self.parser.titles)):
            #if t<len(self.parser.titles):
        #    print(list(self.visted)[t] + " status: 1, tree lvl: "
        #          + (str)(list(self.treeLvl)[t]) + " title: "
        #          + list(self.parser.titles)[t])
            #else:
            #    print(list(self.visted)[t] + " status: 1, tree lvl: ")
                      #+ str(list(self.treeLvl)[t]))


        #for t in self.parser.failed:
        #    print(t + " 0")

        #for t in self.discovered:
        #    print(t + " -1")
        #plt.plot(len(visited),self.count)
        #plt.show()

        # Add urls from the praser to to_visit lits
        # When they are not visited or already in the to_vist list
        self.discovered_count += len(urls)
        self.discovered.update(urls)
        #dict.update(urls,0)
        for url in urls:
            if url not in self.visted and currDepth<maxDepth:
                self.to_visit.add(url)
                self.crawl(visited,to_visit,failed, url, currDepth + 1, maxDepth)

        print("The spider has finished crawling the web at {url}".format(url=target_url))


if __name__ == "__main__":
    print("I don't like snakes. Don't python me directly.")
