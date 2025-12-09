import random
import string
import os
import time
import threading

def generate_random_string(length):
    """Generates a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_file_content(size_bytes):
    """Generates random content for files."""
    return generate_random_string(size_bytes)

class Stress:
    """Helper class for stress testing."""

    @staticmethod
    def consume_memory(mb):
        """Simulates memory consumption."""
        # In a real environment we would allocate lists,
        # but here we just return a large string to hold in memory
        return "a" * (mb * 1024 * 1024)

    @staticmethod
    def cpu_burner(duration_sec):
        """Simulates CPU load."""
        end_time = time.time() + duration_sec
        while time.time() < end_time:
            _ = 2 ** 1000

def get_process_list(kernel):
    """Helper to get list of processes from kernel."""
    return kernel.sys.sys_proc_list()

def kill_random_process(kernel, exclude_pids=None):
    """Kills a random process."""
    if exclude_pids is None:
        exclude_pids = []

    procs = get_process_list(kernel)
    candidates = [p for p in procs if p['pid'] not in exclude_pids]

    if not candidates:
        return False

    victim = random.choice(candidates)
    kernel.sys.sys_kill(victim['pid'])
    return victim['pid']
