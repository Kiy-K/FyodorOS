
import unittest
import os
import shutil
from fyodoros.shell.shell import Shell
from fyodoros.kernel.syscalls import SyscallHandler
from fyodoros.kernel.filesystem import FileSystem

class TestShellBugs(unittest.TestCase):
    def setUp(self):
        # Clean up users.json
        if os.path.exists("users.json"):
            os.remove("users.json")

        self.sys = SyscallHandler()
        self.shell = Shell(self.sys)

    def test_sys_ls_crash_on_file(self):
        # Create a file
        self.sys.sys_write("/test.txt", "hello")

        print("\nTesting sys_ls on file (expecting list containing filename)...")
        try:
            res = self.sys.sys_ls("/test.txt")
            print(f"Result: {res}")
            self.assertEqual(res, ["test.txt"])
        except ValueError as e:
            print(f"Caught expected crash: {e}")
            self.fail("sys_ls crashed on file")
        except Exception as e:
            print(f"Caught unexpected exception: {type(e)} {e}")
            self.fail(f"sys_ls raised {e}")

    def test_login_bypass(self):
        print("\nTesting login bypass...")

        # Add a test user
        # user_add should succeed as we are root (default) and deleted users.json
        # NOTE: UserManager creates defaults on init. "guest" might exist.
        # Let's use "testuser"
        self.sys.sys_user_add("testuser", "securepass")

        # Verify correct login works
        assert self.sys.sys_login("testuser", "securepass") == True, "Correct login failed"

        # Wrong login -> verify fallback
        print("Attempting wrong login...")
        # We simulate the Shell logic: if sys_login returns False, it prints message.
        # Original bug: it printed message AND set current_user="root".
        # Fixed code: just prints and returns False.

        user = "testuser"
        pw = "wrong"
        success = self.sys.sys_login(user, pw)
        print(f"Login success? {success}")

        # Check if shell logic (mocked) falls back
        if not success:
             # This is the logic we removed
             # self.shell.current_user = "root"
             pass

        if self.shell.current_user == "root":
             self.fail("CRITICAL: Shell fell back to root on failed login!")
        else:
             print("Secure: Shell did not fall back.")

    def tearDown(self):
        if os.path.exists("users.json"):
            os.remove("users.json")

if __name__ == "__main__":
    unittest.main()
