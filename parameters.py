id = 0

def increase_id():
    global id  # 明確指定訪問全局變數 id
    id += 1

OPENAI_API_KEY = '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'

#llama cpp openhermes prompt
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

##OpenAI prompt
system_cotprompt_1 = '''
Your output should be of the following format:

Plan:
Your plan here.
'''

user_cotprompt_1 = "Make a coherent plan of the four sentences: {input}."

system_cotprompt_2 = '''
Your output should be of the following format:

Passage:
Your passage here.
'''

user_cotprompt_2 = 'Write a coherent passage of 4 short paragraphs in topic of: {plan}. The end sentence of each paragraph must be: {input}'

system_voteprompt = '''
Your output should be of the following format:

"The best choice is {s}", where s the integer id of the choice.
'''

user_voteprompt = "Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line."