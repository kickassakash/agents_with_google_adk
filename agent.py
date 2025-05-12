#root agent'
import os
from google.adk.agents import LlmAgent,LoopAgent
from google.adk.agents import Agent
from google.adk.tools import google_search
from langchain_community.tools import TavilySearchResults
from google.adk.tools.langchain_tool import LangchainTool
from .util import load_instruction_from_file
from dotenv import load_dotenv

load_dotenv()

# Ensure TAVILY_API_KEY is set in your environment
if not os.getenv("TAVILY_API_KEY"):
    print("Warning: TAVILY_API_KEY environment variable not set.")

TavilySearchResults()

Tavily_search = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
)
tavily_search_tool = LangchainTool(Tavily_search)

Agent_Search = LlmAgent(
    model='gemini-2.0-flash-thinking-exp-01-21',
    name='SearchAgent',
    instruction=load_instruction_from_file('search_agent_ins.txt'),
    tools=[tavily_search_tool],
    output_key='latest_trend_and_its_information'
)

scriptwriter_agent = LlmAgent(
    name="script_write_agent",
    description="an AI agent astonishingingly smart and capable of generating shorts templates",
    model="gemini-2.0-flash-thinking-exp-01-21",
    instruction=load_instruction_from_file("script_writer_ins.txt"),
    output_key='generated_script'
)
visualizer_agent = LlmAgent(
    name="visualizer_agent",
    model="gemini-2.0-flash-thinking-exp-01-21",
    description="creates visualization based on the scripts provided",
    output_key="visual_concepts",
    instruction=load_instruction_from_file("visualizer_ins.txt")
)
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model="gemini-2.0-flash-thinking-exp-01-21",
    instruction="""Combine the script from state['generated_script'] and the visual concepts from state['visual_concepts'] into the final Markdown format requested previously (Hook, Script & Visuals table, Visual Notes, CTA).""",
    description="Formats the final Short concept.",
    output_key="final_short_concept",
)

"""note that just changing the agent types between LLmAgent and loopAgent
   changes what kind of agent we want, if we want to give the LLM autonomy to make the decision
   of using tools to its own thinking then use LlmAgent else use Loopagent or your can use sequential agent
   to convert your agents to workflow agent(jsut like langchain and lang graph)"""

youtube_shorts_agent = LlmAgent(
    name="youtube_shorts_agent",
    description="a smart AI agent curated for generation of sensational shorts",
    model="gemini-2.0-flash-thinking-exp-01-21",
    instruction=load_instruction_from_file("shorts_agent.txt"),
    sub_agents=[Agent_Search,scriptwriter_agent,visualizer_agent,formatter_agent]
)

# youtube_shorts_agent = LoopAgent(
#     name='youtube_shorts_agent',
#     max_iterations=1, #this controls how many times we can loop until we get our preffered output
#     #agents will be called in this order
#     sub_agents=[Agent_Search,
#                 scriptwriter_agent,
#                 visualizer_agent,
#                 formatter_agent
#     ]
# )

root_agent = youtube_shorts_agent





