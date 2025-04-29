import requests, json
from bs4 import BeautifulSoup


class WikiScraper:
    def __init__(self, file="data_sources/data_urls.txt", output_file="processed_data/star_wars_data.jsonl"):
        self.file = file
        self.output_file = output_file

    def scrapePages(self):
        # read the list of urls to scrape and split by "\n" to remove the \n char
        file = open(self.file, "r")
        urls = file.read()
        file.close()
        urls = urls.split("\n")

        # scrape each page and write to the output file
        file = open(self.output_file, "a")
        for url in urls:
            content, name = self.getPageContent(url)
            temp_dict = {"text":content, "name":name}
            file.write(json.dumps(temp_dict) + '\n')
        file.close()

    """
    This function is for scraping the character pages
    """
    def getPageContent(self, url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('h1', id='firstHeading').get_text().strip()
            # get all content between first quote and contents. This contains the main info on the page
            start_item = soup.find("div", class_="quote")
            end_item = soup.find(id="toc")
            full_content = ""
            for sibling in start_item.next_siblings:
                if sibling == end_item:
                    break
                text = sibling.get_text()
                if text:
                    full_content += text 

            #final_string = "Instruction: Tell me about " + title + "\n\nResponse: " + full_content
            final_string = full_content
            return final_string, title

        except Exception as e:
            print("Error: ", e)


    """
    This function is for scraping the content of plots
    """
    def getPlotsContent(self,url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return None
            
            # get the content
            soup = BeautifulSoup(response.text, "html.parser")
            # get the page title
            title_div = soup.find(id="firstHeading")
            plot_title = soup.find(id="Plot")
            parent_div = plot_title.find_parent("div")
            print(parent_div.next_sibling)
            full_content = ""
            for sibling in parent_div.next_siblings:
                print(sibling)
                if not hasattr(sibling, 'name'):
                    continue
                if sibling.name == "p":
                    full_content += sibling.text + "\n"

                else:
                    break



            print(full_content)

        except Exception as e:
            print("Error: ",e)


        
        
scraper = WikiScraper()
scraper.scrapePages()