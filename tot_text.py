import llama

class Node:
    def __init__(self, answer, value):
        self.answer = answer
        self.value = value
        self.parent_node = None
        self.children_node = None
    
    def append_parent(self, parent):
        self.parent_node = parent

    def append_children(self, children):
        self.children_node = children

def Generator(llm, request):
    new_node ={}
    output = []
    for i in range(5):
        prompt = get_writing_plans()        
        new_node['id'] = id
        new_node['answer'] = llm.generate(prompt)
        new_node['value'] = None
        new_node['parent_node'] = current_node['id']
        new_node['ancester_value'] = None

        output.append(new_node)
        id += 1
    return output

        

def Evaluator(llm, request):
    new_node = {}
    output = []
    prompt  = request[1]
    best = llm.evaluate(prompt)
    for i in range(5):
        if best == request[0][i]['answer']:
            break
    new_node = request[0][i]   
    output.append(new_node)
    return output


def get_writing_plans():##可能要改提問
    return f"Please write 5 writing plans in according to the 4 sentences below: {question[0]}, {question[1]}, {question[2]}, {question[3]}"

def eval_writing_plans():##s怪怪的
    return f"Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line \"The best choice is s\", where s the integer id of the choice.: {writing_plans[0]['answer']}, {writing_plans[1]['answer']}, {writing_plans[2]['answer']}, {writing_plans[3]['answer']}, {writing_plans[4]['answer']}"

def get_passage():
    return f"Please write a passage on the topic {best_plan} with 4 paragraphs that end in the 4 input sentences respectively.: {question[0]}, {question[1]}, {question[2]}, {question[3]}"

def get_best_passage():
    return f"Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line \"The best choice is s\", where s the integer id of the choice.: {passages[0]['answer']}, {passages[1]['answer']}, {passages[2]['answer']}, {passages[3]['answer']}, {passages[4]['answer']}"

if __name__ == '__main__':
    llm = llama.get_model()

    question = []  #input 4 sentence
    a = input()
    b = input()
    c = input()
    d = input()
    question.extend([a, b, c, d])

    root_node = {'id':0,
                'answer':question,
                'value':None,
                'parent_node':None,
                'ancester_value':None
                }

    current_node = root_node
    id = 1
    writing_plans = Generator(llm, get_writing_plans()) 
    best_plan = Evaluator(llm, [writing_plans, eval_writing_plans()])

    current_node = best_plan[0]
    id = 6
    passages = Generator(llm, get_passage())
    best_passage = Evaluator(llm, [passages, get_best_passage()]) 

    '''
    root = Node(question, None) 

    writing_plans = []
    for plan in Generator(llm, get_writing_plans()):
    node = Node(plan['answer'], plan['value'])
    node.append_parent(root)
    writing_plans.append(node)

    root.append_children(writing_plans)

    best_plan = Evaluator(writing_plans) 

    passages = []
    for passage in Generator(llm, get_passage(best_plan)):
    node = Node(passage['answer'], passage['value']) 
    node.append_parent(best_plan)
    passages.append(node)

    best_plan.append_children(passages)  
    best_passage = Evaluator(passages)
    '''