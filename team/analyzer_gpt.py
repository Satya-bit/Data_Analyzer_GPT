from agents.Code_Executor_agent import GetCodeExecutorAgent
from agents.Data_analyzer_agent import getDataAnalyzerAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from config.constants import MAX_TURNS, TEXT
def getDataAnalyzerTeam(docker,model_client):
    code_executor_agent=GetCodeExecutorAgent(docker)

    data_analyzer_agent=getDataAnalyzerAgent(model_client)
    
    text_mention_termination=TextMentionTermination(TEXT)
    team=RoundRobinGroupChat(
        participants=[data_analyzer_agent,code_executor_agent],
        max_turns=MAX_TURNS,
        termination_condition=text_mention_termination
    )
    return team
        
