# src/fyodoros/cli.py
"""
FyodorOS CLI Entry Point.
"""

import sys
import shutil
from pathlib import Path
import typer
from fyodoros.kernel import boot, rootfs
from fyodoros.shell.shell import Shell
from fyodoros.kernel.agent import ReActAgent
from fyodoros.kernel.llm import LLMProvider

app = typer.Typer(help="FyodorOS Command Line Interface")

@app.command()
def init():
    """
    Initialize the FyodorOS environment.
    Creates directory structure and migrates data.
    """
    print("Initializing FyodorOS...")
    try:
        # Create structure
        rootfs.init_structure()

        # Migration: Check for legacy memory location
        base = Path.home() / ".fyodor"
        legacy_memory = base / "memory"
        target_memory = base / "var" / "memory"

        if legacy_memory.exists() and legacy_memory.is_dir():
            # If target is empty, we can move
            if target_memory.exists() and not any(target_memory.iterdir()):
                target_memory.rmdir()
                shutil.move(str(legacy_memory), str(target_memory))
                print(f"[Migration] Moved legacy memory from {legacy_memory} to {target_memory}")
            elif not target_memory.exists():
                shutil.move(str(legacy_memory), str(target_memory))
                print(f"[Migration] Moved legacy memory from {legacy_memory} to {target_memory}")
            else:
                 print(f"[Migration] Warning: Target {target_memory} not empty. Manual migration required.")

        print("Initialization complete.")
    except Exception as e:
        print(f"Initialization failed: {e}")
        sys.exit(1)

@app.command()
def start():
    """
    Start the FyodorOS Shell (Default).
    """
    print("Booting FyodorOS Shell...")
    try:
        kernel = boot.boot()
        if hasattr(kernel, "shell") and kernel.shell:
            kernel.shell.run()
        else:
            # Fallback
            shell = Shell(kernel.sys, kernel.service_manager)
            shell.run()
    except Exception as e:
        print(f"Startup failed: {e}")
        sys.exit(1)

@app.command()
def agent(task: str):
    """
    Run the AI Agent with a specific task.
    """
    print(f"Starting Agent with task: {task}")
    try:
        kernel = boot.boot()
        llm = LLMProvider()
        agent_instance = ReActAgent(llm, kernel.sys)

        print(f"\n--- Agent Task: {task} ---\n")
        result = agent_instance.run(task)
        print(f"\n--- Result ---\n{result}")

    except Exception as e:
        print(f"Agent execution failed: {e}")
        sys.exit(1)

def main():
    """Main entry point for the CLI script."""
    app()

if __name__ == "__main__":
    main()
