import os
import openai
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import (SerperDevTool, ScrapeWebsiteTool,ScrapeElementFromWebsiteTool)
from langchain_openai import ChatOpenAI
from agent_watch import AgentWatchTool


# from vidmarswot.my_llm import MyLLM
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

openai.api_key = api_key
# Initialize the LLM
llm                   = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)
gpt_mini              = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)
gpt4o_mini_2024_07_18 = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", openai_api_key=api_key)
gpt4o                 = ChatOpenAI(model_name="gpt-4o", openai_api_key=api_key)
gpt_o1                = ChatOpenAI(model_name="o1-preview", openai_api_key=api_key)
gpt_o1_mini           = ChatOpenAI(model_name="o1-mini", openai_api_key=api_key)

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
scrape_element_tool = ScrapeElementFromWebsiteTool()

agent_watch_tool = AgentWatchTool(
    log_file='agent_watch.log',  # Nome do arquivo de log para armazenar métricas
    streamlit_dashboard=True    # Habilitar dashboard em Streamlit
)



@CrewBase
class VidmarswotCrew():
	"""Vidmarswot crew"""

	@agent
	def agente_extracao(self) -> Agent:
		return Agent(
			config=self.agents_config['agente_extracao'],
			tools=[search_tool, scrape_tool, scrape_element_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation=False,
			allow_interruption=True,
			allow_fallback=True,
            memory=True,
            llm=llm
		)
  
	@agent
	def analista_swot(self) -> Agent:
		return Agent(
			config=self.agents_config['analista_swot'],
			tools=[search_tool, scrape_tool, scrape_element_tool],
			verbose=True,
			allow_delegation=False,
			allow_interruption=True,
			allow_fallback=True,
            memory=True,
            llm=llm
		)

	@agent
	def agente_analise_recomendacao(self) -> Agent:
		return Agent(
			config=self.agents_config['agente_analise_recomendacao'],
			verbose=True,
			allow_delegation=False,
			allow_interruption=True,
			allow_fallback=True,
            memory=True,
            llm=llm
		)

	@task
	def extrair_informacoes_site(self) -> Task:
		return Task(
			config=self.tasks_config['extrair_informacoes_site'],
   		)

	@task
	def analise_swot(self) -> Task:
		return Task(
			config=self.tasks_config['analise_swot'],
   		)

	@task
	def analisar_recomendar(self) -> Task:
		return Task(
			config=self.tasks_config['analisar_recomendar'],
			output_file='analise_swot.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Vidmarswot crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)