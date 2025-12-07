
import unittest
import os
from pathlib import Path
from fyodoros.kernel.syscalls import SyscallHandler
from fyodoros.kernel.sandbox import AgentSandbox
from fyodoros.kernel.filesystem import FileSystem

class TestFSMismatch(unittest.TestCase):
    def setUp(self):
        self.sys = SyscallHandler()
        self.sandbox = AgentSandbox(self.sys)
        self.sys.set_sandbox(self.sandbox)

        # Ensure sandbox dir exists
        self.sandbox_path = Path.home() / ".fyodor" / "sandbox"
        self.sandbox_path.mkdir(parents=True, exist_ok=True)

    def test_agent_write_read_mismatch(self):
        print("\nTesting Agent Write/Read Cycle...")

        filename = "test_agent.txt"
        content = "hello agent"

        # 1. Agent writes file
        # This calls sandbox.execute("write_file", ...) -> sandbox._resolve -> sys.sys_write
        print(f"Agent writing '{filename}'...")
        res_write = self.sandbox.execute("write_file", [filename, content])
        print(f"Write Result: {res_write}")

        # 2. Check where it ended up
        # In-Memory?
        try:
            mem_content = self.sys.fs.read_file(self.sandbox.core.resolve_path(filename) if self.sandbox.core else filename)
            print("Found in In-Memory FS (using resolved path? No, unlikely to match root)")
        except:
            # Try searching in-memory root
            try:
                # _resolve returns absolute path e.g. /home/jules/.fyodor/sandbox/test_agent.txt
                # In-Memory FS root is /.
                # So we are writing to a folder structure inside In-Memory FS corresponding to host path?
                pass
            except:
                pass

        # Real Disk?
        real_file = self.sandbox_path / filename
        if real_file.exists():
            print("Found on Real Disk!")
        else:
            print("NOT Found on Real Disk.")

        # 3. Agent reads file
        # sandbox.execute("read_file") -> _resolve -> sys.sys_read
        print(f"Agent reading '{filename}'...")
        res_read = self.sandbox.execute("read_file", [filename])
        print(f"Read Result: {res_read}")

        if res_read == content:
             print("SUCCESS: Read matches Write.")
        else:
             print("FAILURE: Read content mismatch or error.")

if __name__ == "__main__":
    unittest.main()
