#so this file can be directly used without the help of the adk library
#and we can run it anywhere, we just need python "file_path\agent_runner_local.py"
from google.adk.agents import LlmAgent,LoopAgent
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv

from util import load_instruction_from_file

#creating agents are same as before,
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

#just load your environment variables
load_dotenv()

#create your preffered app name and user_id and session_id (you can use
#any kind of string for this purpose)
app_name = "youtube_shorts_script_app"
user_id = "1234567"
session_id = "1234"

#this InMemorySessionService is for storing the session data inside main
#memory until the session expires
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=app_name,user_id=user_id,session_id=session_id
)
#this is our custom runner which chooses the root agent
runner = Runner(
    agent=youtube_shorts_agent,session_service=session_service,app_name=app_name
)

#this function is the main caller, which calls the root agent and handles
#the events and its outputs
def call_agent(query):
    content = types.Content(role='user',parts=[types.Part(text=query)])
    events = runner.run(user_id=user_id,session_id=session_id,new_message=content)

    for event in events:
        if event.is_final_response():
            res = event.content.parts[0].text
            print("response from event: ",res)

#use your preffered query here or you can also take input and then process
call_agent("I want to write a short on how to build AI Agents")