# Data Mining Project Proposal - Pilot Study

### Example Results
| Prompt | Original Model | Fine Tuned Model |
|--------|----------------|------------------|
| Who did Rex work for? | 1. The man who paid him to take his wife's place, 2. A doctor he was treating in the hospital, and 3. His boss at a car dealership that he worked for briefly before leaving for Florida. | Rex worked under the command of General Anakin Skywalker. |
| Who was Anakin's Padawan? |  Yes, Anakin Skywalker's padawan was Padme Amidala.  | Anakin's Padawan was Ahsoka Tano. |
| Who ordered order 66? |  Yes, Order 66 was issued by the Emperor himself. He had previously been planning to execute Jedi Master Yoda and other prominent members of the Jedi Council on his deathbed. This order marked a turning point in the conflict between the Jedi and the Empire.  | Order 66 was an orders enacted by Sidious that initiated the Great Jedi Purge, leading to the near extinction of the Jedi. |
|  What did Ashoka do after leaving the jedi order? |  Ashoka left the Jedi Order to train as a warrior, where he learned how to fight and protect himself. He became known for his skills in martial arts and fought against various enemies throughout the galaxy. As time went on, he gained respect among other warriors and eventually led several successful battles against the Empire. However, even with his newfound power and experience, he still faced many challenges that tested him both mentally and physically. Despite these obstacles, Ashoka remained committed to fighting against tyranny and oppression wherever it existed, using whatever means necessary to bring about change.     | After leaving the jedi order, Ashoka joined Sabine Wren in her quest to find the missing Bridger and trained Wren in the ways of the Jedi. |
| Where was Anakihn Skywalker born? | Anakin Skywalker was born in Tatooine.    | Anakin Skywalker was born on the desert planet of Tatooine in the Outer Rim Territories during the era of the Galactic Republic. |
| What planet is Chewbaca from? |   Chewbacca.   | Chewbacca hailed from the planet Kashyyyk.|



### Instruction Formatting
Instructions to the LLM should be formatted as such:
```
Instruction: {instruction/prompt} \n\nResponse: 
```

In python you can write your instruction as 
```python
input_text = "Instruction: Can you tell me what star wars is?\n\nResponse: "
```
