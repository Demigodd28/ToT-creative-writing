id = 0

def increase_id():
    global id  # 明確指定訪問全局變數 id
    id += 1

OPENAI_API_KEY = ''

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
user_cotprompt_1 = "Make a coherent writing plan of the sentence: {input}."

user_cotprompt_2 = "Write a coherent short paragraph in topic of: {plan}. The end sentence of paragraph must be: {input}"

system_voteprompt = '''
Your output should be of the following format:

"The best choice is {s}", where s the integer id of the choice.
'''

user_voteprompt = "Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line."
    
#tot paper prompt
standard_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}
'''

cot_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Make a plan then write. Your output should be of the following format:

Plan:
Your plan here.

Passage:
Your passage here.
'''


vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
'''

compare_prompt = '''Briefly analyze the coherency of the following two passages. Conclude in the last line "The more coherent passage is 1", "The more coherent passage is 2", or "The two passages are similarly coherent".
'''

score_prompt = '''Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
'''