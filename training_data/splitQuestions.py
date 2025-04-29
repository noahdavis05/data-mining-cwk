# This is a script to update the long bits of text in star_wars_data.jsonl into many smaller questions
# These questions need to have different formats

# pipeline to take these questions about x character
import json, string, random
import spacy
from rake_nltk import Rake
from nltk.tokenize import sent_tokenize

nlp = spacy.load("en_core_web_sm")
r = Rake()

# question structures
question_templates = {
    "PERSON": [
        "What was {person}'s relationship with {subject}?",
        "How did {person} interact with {subject}?",
        "What role did {subject} play in {person}'s story?",
        "How did {subject} influence {person}?",
        "What major events involved both {person} and {subject}?",
        "What impact did {subject} have on {person}?"
    ],
    "ORG": [
        "What was {person}'s role in {subject}?",
        "How did {subject} impact {person}'s journey?",
        "How was {person} connected to {subject}?",
        "What actions did {person} take against {subject}?",
        "How did {person} contribute to {subject}?",
        "In what ways was {subject} important to {person}?"
    ],
    "EVENT": [
        "What role did {person} play during {subject}?",
        "How did {subject} affect {person}?",
        "Why was {subject} important to {person}?",
        "What did {person} do during {subject}?",
        "How did {person} respond to {subject}?",
        "What were the consequences of {subject} for {person}?"
    ],
    "GPE": [  # Places 
        "What is {person}'s connection to {subject}?",
        "How did {subject} shape {person}'s life?",
        "Where did {person} live on {subject}?",
        "Why is {subject} important in {person}'s story?",
        "What events involving {person} occurred in {subject}?",
        "How did {subject} influence {person}'s early life?"
    ]
}


filename = "processed_data/star_wars_data.jsonl"
with open(filename, 'r') as file:
    for line in file:
        data = json.loads(line)
        text = data['text']
        character_name = data['name']
        # chunk the data into paragraphs
        paragraphs = text.split("\n")
        # for each paragraph we will assess keywords
        for para in paragraphs:
            if len(para) < 20:
                continue
            # get the keywords/phrases using NER
            # these terms aren't necassarily important or useful
            doc = nlp(para)
            entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ("ORG", "EVENT", "GPE", "PERSON")]
            #print("Entity: ", entities)
            # entities are ordered by when they appear in text, not by confidence
            # therefore lets use a different method to try and find important terms
            r.extract_keywords_from_text(para)
            keywords = r.get_ranked_phrases_with_scores()
            #print(keywords)
            # now lets see which terms cross over (e.g. in both)
            # i have two arrays of tuples now I need to see if any of these tuples across the two sets cross-over
            # or if tuples contain terms from other tuples (i.e. one contains 'Anakin', and one contains 'Anakin Skywalker' these should be paired)
            # brute force nested for loops just for ease - arrays aren't particularly long anyway
            final_choices = []
            for weighting_phrase in keywords:
                for type_phrase in entities:
                    # see if type_phrase in weighting_phrase or vice versa
                    if type_phrase[0].lower() in weighting_phrase[1].lower() or weighting_phrase[1].lower() in type_phrase[0].lower():
                        # add this to my final array
                        final_choices.append((type_phrase[0], type_phrase[1], weighting_phrase[0]))

            # remove duplicates
            best_entities = {}
    
            for text, label, score in final_choices:
                norm = text
                
                if norm not in best_entities:
                    best_entities[norm] = (text, label, score)
                else:
                    _, _, existing_score = best_entities[norm]
                    if score > existing_score:
                        best_entities[norm] = (text, label, score)

            final_choices = []
            for key, value in best_entities.items():
                final_choices.append(value)

            # remove any entries which are of the character the article is about
            for choice in final_choices:
                if choice[0].lower() in character_name.lower():
                    final_choices.remove(choice)

            # update the ranking score with what type it is.
            # EVENT the most important, followed by all others equally (in my opinion)
            # Also update it's score by how far it is to the start of the paragraph (important topics/subjects appear earlier on)
            # also 
            for index, choice in enumerate(final_choices):
                if choice[1] == "EVENT":
                    final_choices[index] = (choice[0], choice[1], choice[2] + 15)
                # work out distance of this word from start of para
                split_para = para.split(" ")
                occurence_count = 0
                first_occurence = len(split_para)


                # this is definately not perfect, as first word of the phrase could occur before the phrase
                # but this is good enough for meantime
                # in future will use ngrams
                first_word_of_keyword = choice[0].split(" ")[0].lower()
                #print(first_word_of_keyword)
                
                for index2, word in enumerate(split_para):
                    if first_word_of_keyword in word.lower():
                        occurence_count += 1
                        if first_occurence == len(split_para):
                            first_occurence = index2

                final_choices[index] = (choice[0], choice[1], choice[2] + occurence_count + (len(split_para) - first_occurence)*0.1)



            # now order by score
            final_choices.sort(key=lambda x: x[2], reverse=True)
            final_choices = final_choices[:5]


            # now I need to extract the sentences which are around the keyterm.
            '''
            for tup in final_choices:
                key_term = tup[0]
                key_term_length = len(key_term.split(" "))
                # now iterate over paragraph and find where the term is
                for i in range(0, len(split_para) - key_term_length):
                    # make a string of length key_term_length
                    temp_word = ""
                    for j in range(i,i + key_term_length):
                        temp_word += split_para[j] + " "
                    
                    temp_word = temp_word[:-1]
                    # remove punctuation
                    temp_word_altered = temp_word.translate(str.maketrans('','', string.punctuation))
                
                    if key_term == temp_word or key_term == temp_word_altered:
                        print("match is found: ", key_term)
            '''

            sentences = sent_tokenize(para)
            num_sentences = len(sentences)
            for tup in final_choices:
                for index3, sentence in enumerate(sentences):
                    if tup[0] in sentence:
                        # make the sentences for the answer, one before, current, and after
                        num = 3
                        sentences_for_answer = ""
                        for index4, sen in enumerate(sentences):
                            if index4 == index3 -1 or index4 == index3 or index4 == index3 + 1:
                                sentences_for_answer += sen + " "
                        
                        new_tuple = (tup[0], tup[1], tup[2], sentences_for_answer)
                        
                        # now for each new tuple
                        # make a question
                        template = random.choice(question_templates[new_tuple[1]])
                        question = template.format(person=character_name, subject=new_tuple[0])
                        final_prompt = "Instruction: " + question + "\n\nResponse: " + new_tuple[3]
                        # write to the jsonl file
                        output_file = open("processed_data/question_and_answers_2.jsonl", "a")
                        temp_dict = {"text": final_prompt}
                        output_file.write(json.dumps(temp_dict) + "\n")
                        output_file.close()


            


            #print("\n")
            #print(final_choices)
            #print(keywords)
            #print(entities)


        