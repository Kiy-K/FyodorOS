FyodorOS███████╗██╗   ██╗ ██████╗ ██████╗  ██████╗ ██████╗
██╔════╝╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗
█████╗   ╚████╔╝ ██║   ██║██║  ██║██║   ██║██████╔╝
██╔══╝    ╚██╔╝  ██║   ██║██║  ██║██║   ██║██╔══██╗
██║        ██║   ╚██████╔╝██████╔╝╚██████╔╝██║  ██║
╚═╝        ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
          The Experimental AI Microkernel
The Operating System for Autonomous AI Agents.🚀 VisionWe believe that for AI Agents to be truly useful and safe, they need an environment built for them. FyodorOS provides:Structured Observation: The OS state (Filesystem, Processes, Users) is a queryable DOM tree.Cognitive Loop: Built-in ReAct (Reasoning + Acting) loop at the kernel level.Safety Sandbox: A strict, rule-based verification layer that constraints Agent actions before execution.Agent-Native Apps: Standard tools (browser, explorer, calc) that return structured JSON/DOM instead of plain text, minimizing token usage and parsing errors.Cloud Integration (v0.5.0): Native Docker and Kubernetes support.Long-Term Memory (v0.7.0): Persistent semantic storage allowing agents to learn and recall information.Desktop Interface (v0.8.0) 🚀 [NEW]: A native desktop application bridging the Python kernel with a modern React UI.📦 InstallationOption A: User (Recommended)Download the installer for Windows, Mac, or Linux from the Releases page.Option B: Developer (Legacy/Headless)You can install FyodorOS as a Python package for headless or CLI-only usage.pip install fyodoros
playwright install chromium
🛠️ DevelopmentTo build the full Desktop experience from source, you need Node.js, Rust, and Python installed.Clone the Repositorygit clone [https://github.com/Kiy-K/FyodorOS.git](https://github.com/Kiy-K/FyodorOS.git)
cd fyodoros
Install Frontend Dependenciescd gui
npm install
Run in Development Modenpm run tauri dev
🗺️ RoadmapSee our detailed trajectory in ROADMAP.md.🏗️ ArchitectureFyodorOS v0.8.0 adopts a hybrid architecture to combine the flexibility of Python AI libraries with the performance and native capabilities of Rust.graph LR
    User[User] <--> React["React UI (Shadcn)"]
    React <--> Tauri["Tauri (Rust Sidecar)"]
    Tauri <--> Nuitka["Nuitka (Compiled Python Kernel)"]
    Nuitka <--> System["Host System (Sandboxed)"]
React UI: A modern web-based interface for visualizing the OS state and Agent actions.Tauri: Handles window management and communicates with the Python kernel via a sidecar protocol.Nuitka Kernel: The Python core compiled into a standalone binary for performance and security, running the Agent loop and managing system resources.🤝 ContributingFyodorOS is an experimental sandbox. We welcome contributions to:Expand the standard library of Agent Apps.Improve the DOM representation of system state.Implement more complex Sandbox rules.Built for the future of Autonomous Computing.
