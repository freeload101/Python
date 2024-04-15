import os
import subprocess

def install_imports_from_files(path):
    if not os.path.isdir(path):
        print(f"The path {path} is not a valid directory.")
        return

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("import ") or line.startswith("from "):
                            try:

                                module = line.split()[1].split('.')[0]
                                print("Installing module: " + module)
                                subprocess.run(["pip", "install", module], check=True)
                            except Exception as e:
                                print(f"Failed to install module {module}. Error: {e}")

install_imports_from_files(os.getcwd())
