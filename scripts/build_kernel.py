import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def get_target_triple():
    """
    Determine the Rust-style target triple for the current machine.
    Tauri expects sidecars to be named <binary>-<target-triple><.exe>
    """
    machine = platform.machine().lower()
    system = platform.system().lower()

    # Map machine architecture
    if machine in ['x86_64', 'amd64']:
        arch = 'x86_64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'aarch64'
    else:
        arch = machine # Fallback

    # Map system and abi
    if system == 'windows':
        target = 'pc-windows-msvc'
    elif system == 'linux':
        target = 'unknown-linux-gnu'
    elif system == 'darwin':
        target = 'apple-darwin'
    else:
        target = 'unknown'

    return f"{arch}-{target}"

def build():
    # Configuration
    binary_name = "fyodor-kernel"
    repo_root = Path(__file__).parent.parent
    src_dir = repo_root / "src"
    output_dir = repo_root / "gui" / "src-tauri" / "bin"

    target_triple = get_target_triple()
    extension = ".exe" if platform.system().lower() == "windows" else ""
    final_binary_name = f"{binary_name}-{target_triple}{extension}"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Build] Target Triple: {target_triple}")
    print(f"[Build] Output: {output_dir / final_binary_name}")

    # Nuitka Command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--assume-yes-for-downloads",
        "--include-package=fyodoros",
        # Include templates if they exist (using wildcard or specific path)
        # Assuming fyodoros/templates exists inside the package
        "--include-package-data=fyodoros",
        "--output-dir=" + str(output_dir),
        "--output-filename=" + final_binary_name,
        "--enable-plugin=pylint-warnings", # Optional but good
        # Critical for NASM/Subprocess
        # Nuitka supports subprocess/ctypes out of the box usually,
        # but we ensure standard modules are included.
        str(src_dir / "fyodoros" / "cli.py") # Entry point
    ]

    print(f"[Build] Running: {' '.join(cmd)}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_dir)

    try:
        subprocess.run(cmd, env=env, check=True)
        print("[Build] Success!")
    except subprocess.CalledProcessError as e:
        print(f"[Build] Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
