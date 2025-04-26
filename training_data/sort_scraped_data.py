from transformers import AutoTokenizer
from tqdm import tqdm


"""
This class is used to sort data scraped from within a sketch engine corpus to find useful information
"""
class ScrapedDataSorter:
    def __init__(self,filename):
        # get the input and output files
        self.filename = filename
        self.output_file = "data_sources/sketch_engine_filtered_>250_tokens.txt"
        # create a tokenizer so I can count how many tokens are in each row
        self.tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        # counter for how many valid entries
        self.count = 0
        self.token_sum = 0
        self.result_string = ""



    def filterData(self):
        line_count = 0
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in tqdm(file):
                line_count += 1
                line.replace("<p>","")
                line.replace("</p>","")
                line.replace("\n","")
                # count how many tokens are in line
                tokens = self.tokenizer.encode(line, add_special_tokens=False)
                total_tokens = len(tokens)
                if total_tokens > 250:
                    # add to my result string
                    self.token_sum += total_tokens
                    self.count += 1
                    self.result_string += line + "\n"
        
        print(line_count, self.count, self.token_sum)
        # write to output file
        output_file = open(self.output_file, "w")
        output_file.write(self.result_string)
        output_file.close()




parser = ScrapedDataSorter("data_sources/star_wars.txt")
parser.filterData()
