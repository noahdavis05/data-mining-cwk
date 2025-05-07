# Data Mining Project Proposal - Pilot Study

### Example Results
| Prompt | Original Model | Fine Tuned Model |
|--------|----------------|------------------|
| Who did Rex work for? |     | Rex worked under the command of General Anakin Skywalker. |
| Who was Anakin's Padawan? |    | Anakin's Padawan was Ahsoka Tano. |
| Who ordered order 66? |    | Order 66 was an orders enacted by Sidious that initiated the Great Jedi Purge, leading to the near extinction of the Jedi. |
|  What did Ashoka do after leaving the jedi order? |       | After leaving the jedi order, Ashoka joined Sabine Wren in her quest to find the missing Bridger and trained Wren in the ways of the Jedi. |
| Where was Anakihn Skywalker born? |     | Anakin Skywalker was born on the desert planet of Tatooine in the Outer Rim Territories during the era of the Galactic Republic. |
| What planet is Chewbaca from? |      | Chewbacca hailed from the planet Kashyyyk.|



### Instruction Formatting
Instructions to the LLM should be formatted as such:
```
Instruction: {instruction/prompt} \n\nResponse: 
```

In python you can write your instruction as 
```python
input_text = "Instruction: Can you tell me what star wars is?\n\nResponse: "
```
