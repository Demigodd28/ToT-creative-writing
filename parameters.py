id = 0

def increase_id():
    global id  # 明確指定訪問全局變數 id
    id += 1


cot_prompt_1 = '''
Make a coherent plan of the four sentences: {input}.
Your output should be of the following format:

Plan:
Your plan here.

'''

cot_prompt_2 = '''
Write a coherent passage of 4 short paragraphs in topic of: {plan}. The end sentence of each paragraph must be: {input}

Your output should be of the following format:

Passage:
Your passage here.
'''

vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line.

Your output should be of the following format:

"The best choice is {s}", where s the integer id of the choice.
'''