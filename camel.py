## CAMEL Role-Playing Autonomous Cooperative Agents
## CAMEL: Communicative Agents for “Mind” Exploration of Large Scale Language Model Society

## Import LangChain related modules
# python camel.py| tee -a spamdetector.txt

import colorama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from langchain_ollama import ChatOllama

from camelagent import CAMELAgent
from utils import get_sys_msgs

model_name = "llama3.2"
assistant_role_name = "Agent007"
user_role_name = "Agent369"
task = """Create an Application that can write blogs using langchain_ollama Models and serp api and langchain with the search feature that can provide latest updates for a keyword. The Generated Blogs should be SEO Optimized such that it should get the clicks."""


word_limit = 100  # word limit for task brainstorming


### Create a task specify agent for brainstorming and get the specified task
task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
task_specifier_prompt = """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
Please make it more specific. Be creative and imaginative.
Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
task_specifier_template = HumanMessagePromptTemplate.from_template(
    template=task_specifier_prompt
)
task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOllama(model=model_name))
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=task,
    word_limit=word_limit,
)[0]
specified_task_msg = task_specify_agent.step(task_specifier_msg)

print(
    colorama.Fore.MAGENTA
    + f"Specified task: {specified_task_msg.content}"
    + colorama.Style.RESET_ALL
)
specified_task = specified_task_msg.content


### Create AI assistant agent and AI user agent from obtained system messages
assistant_sys_msg, user_sys_msg = get_sys_msgs(
    assistant_role_name, user_role_name, specified_task
)
assistant_agent = CAMELAgent(assistant_sys_msg, ChatOllama(model=model_name))
user_agent = CAMELAgent(user_sys_msg, ChatOllama(model=model_name))

# Reset agents
assistant_agent.reset()
user_agent.reset()

# Initialize chats
assistant_msg = HumanMessage(
    content=(
        f"{user_sys_msg.content}. "
        "Now start to give me introductions one by one. "
        "Only reply with Response,Reflections, code and Critique"
    )
)

user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
user_msg = assistant_agent.step(user_msg)


### Start role-playing session to solve the task!
print(colorama.Fore.RED + f"Original task prompt:\n{task}\n" + colorama.Style.RESET_ALL)
print(
    colorama.Fore.CYAN
    + f"Specified task prompt:\n{specified_task}\n"
    + colorama.Style.RESET_ALL
)
chat_turn_limit, n = 50, 0
while n < chat_turn_limit:
    n += 1
    user_ai_msg = user_agent.step(assistant_msg)
    user_msg = HumanMessage(content=user_ai_msg.content)
    print(
        colorama.Fore.BLUE
        + f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n"
        + colorama.Style.RESET_ALL
    )

    assistant_ai_msg = assistant_agent.step(user_msg)
    assistant_msg = HumanMessage(content=assistant_ai_msg.content)
    print(
        colorama.Fore.GREEN
        + f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n"
        + colorama.Style.RESET_ALL
    )
    if "<TASK_DONE>" in user_msg.content:
        break
