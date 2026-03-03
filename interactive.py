import os
import subprocess
import sys
import ast

def list_modules():
    """List all available modules in the current directory."""
    modules = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name) and os.path.exists(os.path.join(name, "main.py"))]
    return modules

def get_module_arguments(module_name):
    """Extract arguments from the module's main.py file."""
    module_main_path = os.path.join(os.getcwd(), module_name, "main.py")
    if not os.path.exists(module_main_path):
        return []

    with open(module_main_path, "r") as f:
        tree = ast.parse(f.read(), filename=module_main_path)

    arguments = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_argument":
                arg_name = None
                default_value = None
                for kw in node.keywords:
                    if kw.arg == "dest":
                        arg_name = kw.value.value if isinstance(kw.value, ast.Constant) else None
                    if kw.arg == "default":
                        default_value = kw.value.value if isinstance(kw.value, ast.Constant) else None
                if arg_name:
                    arguments.append((arg_name, default_value))
    return arguments

def setup_and_run_module(module_name, args):
    module_path = os.path.join(os.getcwd(), module_name)
    venv_path = os.path.join(module_path, "venv")
    requirements_file = os.path.join(module_path, "requirements.txt")

    if not os.path.exists(module_path):
        print(f"Module '{module_name}' does not exist.")
        return

    # Create virtual environment if it doesn't exist
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment for {module_name}...")
        subprocess.run([sys.executable, "-m", "venv", venv_path])

    # Install dependencies
    pip_path = os.path.join(venv_path, "bin", "pip")
    if os.name == "nt":  # Windows compatibility
        pip_path = os.path.join(venv_path, "Scripts", "pip")

    if os.path.exists(requirements_file):
        print(f"Installing dependencies for {module_name}...")
        subprocess.run([pip_path, "install", "-r", requirements_file])
    else:
        print(f"No requirements.txt found for {module_name}.")

    # Run the module's main script
    module_main = os.path.join(module_path, "main.py")
    if os.path.exists(module_main):
        print(f"Running {module_name}...")
        subprocess.run([os.path.join(venv_path, "bin", "python"), module_main, *args])
    else:
        print(f"No main.py found in {module_name}.")

def interactive_cli():
    """Start an interactive CLI program."""
    modules = list_modules()
    if not modules:
        print("No modules available.")
        return

    print("Available modules:")
    for i, module in enumerate(modules, 1):
        print(f"{i}. {module}")

    proceed = input("Do you want to proceed with CLI interactively? (1) Yes (2) No: ")
    if proceed.strip() != "1":
        print("Exiting program.")
        return

    while True:
        try:
            choice = int(input("Select the module you want to run (number): "))
            if 1 <= choice <= len(modules):
                selected_module = modules[choice - 1]
                break
            else:
                print("Invalid choice. Please select a valid module number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("\nAvailable modules:")
    for i, module in enumerate(modules, 1):
        tick = "✔" if module == selected_module else " "
        print(f"[{tick}] {i}. {module}")

    confirm = input(f"Proceed with this choice ({selected_module})? (1) Yes (2) No: ")
    if confirm.strip() != "1":
        print("Exiting program.")
        return

    print(f"\nArguments required for {selected_module}:")
    print("(Provide values for the following arguments. Press Enter to use defaults if available.)")

    module_arguments = get_module_arguments(selected_module)
    args = []
    for arg_name, default_value in module_arguments:
        user_value = input(f"{arg_name} (default: {default_value}): ").strip()
        args.append(f"--{arg_name}={user_value}" if user_value else f"--{arg_name}={default_value}" if default_value else f"--{arg_name}")

    setup_and_run_module(selected_module, args)

def print_usage_info():
    """
    Print usage information about the script and its flags.
    """
    print("""
    Usage: python main.py [OPTIONS]

    Options:
      --module      Specify the module to run directly.
      --args        Arguments to pass to the module (use key=value pairs).
      --info        Display information about the script and available modules.
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_usage_info()
        interactive_cli()
    else:
        if "--info" in sys.argv:
            print_usage_info()
            print("\nAvailable modules:")
            for i, module in enumerate(list_modules(), 1):
                print(f"{i}. {module}")
        elif "--module" in sys.argv:
            try:
                module_index = sys.argv.index("--module") + 1
                module_name = sys.argv[module_index]
                module_args = sys.argv[module_index + 1:]
                setup_and_run_module(module_name, module_args)
            except IndexError:
                print("Error: No module specified after --module.")
        else:
            print("Invalid arguments. Use --info for usage information.")