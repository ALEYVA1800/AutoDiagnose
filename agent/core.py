import ollama
from config.settings import MODEL_NAME
from agent.prompts import SYSTEM_PROMPT
from agent.tools import check_systemd_status, get_journalctl_logs, check_network_interfaces
from agent.log_reader import read_system_logs

# Registro de herramientas disponibles
TOOLS_LIST = [check_systemd_status, get_journalctl_logs, check_network_interfaces]
AVAILABLE_TOOLS = {func.__name__: func for func in TOOLS_LIST}

def run_diagnostic(user_prompt: str, on_tool_call=None) -> str:
    """Orquesta la ejecución del agente y llamadas a herramientas"""

    messages = [
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user",  "content":user_prompt}
    ]

    response = ollama.chat(model=MODEL_NAME, messages=messages, tools=TOOLS_LIST)
    messages.append(response.message)

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            func_name = tool.function.name
            func_args = tool.function.arguments

            if on_tool_call:
                on_tool_call(func_name,func_args)
            
            if func_name in AVAILABLE_TOOLS:
                tool_output = AVAILABLE_TOOLS[func_name](**func_args)
                messages.append({"role":"tool","content":tool_output})
        
        final_response = ollama.chat(model=MODEL_NAME, messages=messages)
        return final_response.message.content
    return response.message.content