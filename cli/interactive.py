import os
import subprocess
import inspect
from typing import Callable

from image_compression.compress_image import run as image_compression_run

# Registry: module name -> run() function
# Add new modules here as you create them
MODULES: dict[str, Callable] = {
    "image_compression": image_compression_run,
}

def list_modules() -> list[str]:
    """Return available module names."""
    return list(MODULES.keys())

def get_module_arguments(run_func: Callable) -> list[tuple[str, any, bool, type]]:
    """
    Inspect a run() function and return its parameters as:
    [(name, default_value, is_required, type), ...]
    """
    sig = inspect.signature(run_func)
    hints = inspect.get_annotations(run_func)
    args = []
    for name, param in sig.parameters.items():
        required = param.default is inspect.Parameter.empty
        default = None if required else param.default
        arg_type = hints.get(name, str)
        args.append((name, default, required, arg_type))
    return args

def confirm_prompt(question: str, default_yes: bool = True) -> bool:
    """Y/n or y/N prompt. Capital letter = default (press Enter)."""
    hint = "[Y/n]" if default_yes else "[y/N]"
    response = input(f"{question} {hint}: ").strip().lower()
    if not response:
        return default_yes
    return response == "y"

# def ensure_dependencies():
#     """Run the venv handler bash script to ensure dependencies are installed."""
#     script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_venv_handler.sh")
#     if os.path.exists(script_path):
#         print("Ensuring dependencies are installed...")
#         subprocess.run(["bash", script_path], check=True)
#     else:
#         print("Warning: python_venv_handler.sh not found. Skipping dependency check.")

def interactive_cli():
    """Start an interactive CLI program."""
    modules = list_modules()
    if not modules:
        print("No modules available.")
        return

    print("\nAvailable modules:")
    for i, module in enumerate(modules, 1):
        print(f"  {i}. {module}")

    # Default is Yes — most likely user invoked interactive on purpose
    if not confirm_prompt("\nDo you want to proceed interactively?", default_yes=True):
        print("Exiting.")
        return

    while True:
        try:
            choice = int(input("\nSelect a module (number): "))
            if 1 <= choice <= len(modules):
                selected_module = modules[choice - 1]
                break
            else:
                print(f"  Invalid choice. Enter a number between 1 and {len(modules)}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

    print("\nAvailable modules:")
    for i, module in enumerate(modules, 1):
        tick = "✔" if module == selected_module else " "
        print(f"  [{tick}] {i}. {module}")

    # Default is Yes — user just picked the module, likely wants to proceed
    if not confirm_prompt(f"\nProceed with '{selected_module}'?", default_yes=True):
        print("Exiting.")
        return

    run_func = MODULES[selected_module]
    module_arguments = get_module_arguments(run_func)

    print(f"\nConfiguring arguments for '{selected_module}':")
    print("  (Press Enter to use the default value shown in brackets.)\n")

    kwargs = {}
    for arg_name, default_value, required, arg_type in module_arguments:
        prompt = f"  {arg_name} ({'required' if required else f'{default_value}'}):" \
                 if required else f"  {arg_name} [{default_value}]: "

        while True:
            user_value = input(prompt).strip()
            if user_value:
                try:
                    kwargs[arg_name] = arg_type(user_value)
                    break
                except (ValueError, TypeError):
                    print(f"  Expected type {arg_type.__name__}. Try again.")
            elif not required:
                kwargs[arg_name] = default_value
                break
            else:
                print(f"  '{arg_name}' is required. Please provide a value.")

    print(f"\nRunning '{selected_module}'...\n")
    try:
        run_func(**kwargs)
        print(f"\n✔ '{selected_module}' completed successfully.")
    except Exception as e:
        print(f"\n✘ Error running '{selected_module}': {e}")