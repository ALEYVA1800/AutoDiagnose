import ollama
from config.settings import MODEL_NAME
from agent.prompts import get_system_prompt
from agent.tools import TOOLS_LIST, get_os_context

# Construcción dinámica del diccionario de despacho ({ "nombre_funcion": funcion_objeto })
AVAILABLE_TOOLS = {func.__name__: func for func in TOOLS_LIST}

def run_diagnostic(user_prompt: str, on_tool_call=None) -> str:
    """Orquesta la ejecución del agente con herramientas auto-registradas."""
    os_info = get_os_context()
    
    messages = [
        {"role": "system", "content": get_system_prompt(os_info)},
        {"role": "user", "content": user_prompt}
    ]
    
    # Pasamos TOOLS_LIST que se generó en automatico
    response = ollama.chat(model=MODEL_NAME, messages=messages, tools=TOOLS_LIST)
    messages.append(response.message)
    
    if response.message.tool_calls:
        for tool_call in response.message.tool_calls:
            func_name = tool_call.function.name
            func_args = tool_call.function.arguments
            
            if on_tool_call:
                on_tool_call(func_name, func_args)
                
            if func_name in AVAILABLE_TOOLS:
                tool_output = AVAILABLE_TOOLS[func_name](**func_args)
                messages.append({"role": "tool", "content": tool_output})
        
        final_response = ollama.chat(model=MODEL_NAME, messages=messages)
        return final_response.message.content
        
    return response.message.content