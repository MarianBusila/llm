from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

ollama_openhermes = Ollama(model="openhermes")

researcher = Agent(
    role = 'Researcher',
    goal = 'Research new AI insights',
    backstory = 'You are an AI research assitent.',
    verbose = True,
    allow_delegation=False,
    llm = ollama_openhermes
)

writer = Agent(
    role = 'Writer',
    goal = 'Write compelling and engaging blog posts about AI trends and insights',
    backstory = 'You are an AI blog post writer who speciliazes in AI topics.',
    verbose = True,
    allow_delegation=False,
    llm = ollama_openhermes
)

task1 = Task(description='Investigate the latest AI trends', agent = researcher)
task2 = Task(description='Write a compelling blog post based on the latest AI trends', agent = writer)

crew = Crew(
    agents = [researcher, writer],
    tasks = [task1, task2],
    verbose = 2,
    process = Process.sequential
)

print("Kickoff ...")
result = crew.kickoff()