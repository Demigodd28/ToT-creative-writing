from openai import OpenAI
from parameters import *
import re
import time

llm = OpenAI(
    api_key = OPENAI_API_KEY
)


def Generator(llm, user_input):
    user_content = '''Write a coherent short paragraph. The end sentence of paragraph must be: {input}'''
    generated_paragraph = ''
    for i in range(4):
        check_1 = False        
        for _ in range(5):      
            if check_1 == False:
                ans_from_llm = llm.chat.completions.create(
                    model = 'gpt-3.5-turbo-1106',
                    messages = [
                        {"role": "user", "content": user_content.format(input = user_input[i])}
                    ]
                )
                check_1 = check(ans_from_llm.choices[0].message.content, user_input[i])
            # print(ans_from_llm.choices[0].message.content + '\n\n')###
            # print(user_input[i] + '\n------------------------------------------------------\n')###
            else: break    
        # print(ans_from_llm.choices[0].message.content + '\n\n')    
        generated_paragraph += ans_from_llm.choices[0].message.content + '\n\n'

    return [generated_paragraph]

def check(text, input_data):
    fragment_1 = text.replace(', ', '. ')
    # print(fragment_1)
    fragments_1 = fragment_1.split('. ')
    # print(fragments_1)

    for i in range(len(fragments_1)):
        fragments_1[i] = fragments_1[i].strip()

    if fragments_1[-1] in input_data:
        return True
    else:
        return False
    
if __name__ == '__main__':
    start = time.time()
    with open('data_100_random_text.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    a = data[0].split('. ')
    a = [sentence.strip() for sentence in a if sentence.strip()]
    for i in range(len(a)):
        a[i] += '.'
    response = Generator(llm, a)

    with open('test.txt', 'w') as file:
        file.write(response[0])
    finish = time.time()
    print(finish-start)
    

    