from rich.console  import Console
from rich.panel    import Panel
from rich.markdown import Markdown
from rich.console  import Group
from agent.core    import run_diagnostic

console = Console()

def display_tool_execution(func_name: str, func_args: dict):
    """Muestra el comando en eecucion por el agente"""
    args_str = ", ".join(f"{k}={v}" for k,v in func_args.items())
    console.print(f"[bold yellow]⚙️[Herramienta ejecutada][/bold yellow] [cyan]{func_name}({args_str})[/cyan]")

def start_cli():
    console.clear()
    console.print(Panel.fit(
        "═╗ ║║  ║║ ║ ═╗║═╗║ ║═╗╔═╗╔═╗\n"
        "╔╩╗║║  ║║ ║ ╔╩╗║ ║║ ║ ║╚═╗║╣ \n"
        "╚═╝╩╚═╪╚═╝  ╚═╝╩═╝╚═╝═╝╚═╝╚═╝",
        title="[bold green]Linux Diagnose Agent (MVP)[/bold green]",
        subtitle="Desarrollado con Ollama & Llama 3.1",
        border_style="green"
    ))
    console.print("[italic file]Escribe tu consulta o 'salir' para terminar.[/italic file]\n")

    while True:
        try:
            user_input = console.input("[bold blue]sysadmin@diagnose -> [/bold blue]")
            if user_input.strip().lower() in ['salir','exit','quit']:
                console.print("[bold red]Saliendo...[/bold red]")
                break
            
            if not user_input.strip():
                continue

            #Spinner durante el procesamiento y ejecución de herramientas por el LLM
            with console.status("[bold magenta]Analizando el sistema[/bold magenta]"):
                diagnose = run_diagnostic(user_input, on_tool_call=display_tool_execution)
            
            console.print("\n", Panel(Markdown(diagnose), title="[bold cyan]Resultado[/bold cyan]", border_style="cyan"))
            console.print("-" * console.width)
        
        except KeyboardInterrupt:
            console.print("\n[bold red]Operacion cancelada[/bold red]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error inesperado:[/bold red]{str(e)}")        