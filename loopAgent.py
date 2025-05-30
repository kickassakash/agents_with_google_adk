#root agent
from google.adk.agents import LlmAgent,LoopAgent
from google.adk.agents import Agent
from google.adk.tools import google_search

from .util import load_instruction_from_file

Agent_Search = LlmAgent(
    model='gemini-2.0-flash-thinking-exp-01-21',
    name='SearchAgent',
    instruction=load_instruction_from_file('search_agent_ins.txt'),
    tools=[google_search],
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

youtube_shorts_agent = LoopAgent(
    name='youtube_shorts_agent',
    max_iterations=1,
    sub_agents=[Agent_Search,
                scriptwriter_agent,
                visualizer_agent,
                formatter_agent
    ]
)

root_agent = youtube_shorts_agent


