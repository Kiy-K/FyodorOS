# Changelog

## [0.7.0] - 2025-12-14
### System Internals
- **Persistent Memory System**: Integrated `ChromaDB` to provide long-term semantic memory for Agents.
    - **Backing Store**: Memories persist in `~/.fyodor/memory/` across reboots.
    - **Vector Search**: Utilizes embedding-based retrieval to recall relevant context for tasks.
- **Service Manager Optimization**: Refined the DAG-based dependency resolution with `TopologicalSorter` for guaranteed correct startup/shutdown order.
- **Boot Sequence**: Improved deterministic boot order with explicit resource cleanup on failure.

### Security
- **Dual-Layer Path Resolution**:
    - **C++ Sandbox Core**: `resolve_path` now uses `std::filesystem::lexically_normal` and strict prefix checking to prevent traversal attacks at the native level.
    - **Python Kernel**: `rootfs.resolve` implements a secondary check using `os.path.commonpath` for "secure Python fallback".
- **Sandbox Isolation**: The C++ core (`sandbox.cpp`) now enforces strict I/O pipe management with `poll()` to prevent deadlocks during high-volume process output.

### API/Syscalls
- **New Syscalls**:
    - `sys_memory_store(content, metadata)`: Store a text memory with optional metadata.
    - `sys_memory_search(query, limit)`: Semantic search over stored memories.
    - `sys_memory_recall(query)`: Alias for search.
    - `sys_memory_delete(key_id_or_query)`: Remove specific memories.
- **Agent Integration**: `ReActAgent` loop now automatically invokes `sys_memory_search` at the start of a task to retrieve historical context.

### Fixed
- **Boot**: Fixed a race condition where `NetworkGuard` could leave sockets patched on a failed boot.
- **Filesystem**: Fixed `sys_ls` path resolution to correctly handle trailing slashes and virtual root mappings.
- **Dependencies**: Added `chromadb` for vector storage and updated `playwright` for browser automation.

## [0.6.0] - 2025-12-09
### Verified
- **System Stability**: Completed "Phase 2.3" destructive test sweep of core subsystems.
- **Boot Integrity**: Confirmed deterministic boot and clean double-boot isolation.
- **Teardown Correctness**: Verified LIFO service shutdown and no ghost state leakage.
- **Sandbox Security**: Confirmed path resolution integrity and error containment.

### Fixed
- **Kernel**: Added graceful `shutdown()` method to orchestrate subsystem teardown.
- **Service Manager**: Renamed from Supervisor; completely re-architected with:
    - **Dependency Management**: DAG-based topological sort for correct startup/shutdown order.
    - **3-Phase Shutdown**: Warning -> Graceful -> Force protocol.
    - **Threaded Timeouts**: Non-blocking shutdown with configurable per-service timeouts.
    - **State Machine**: Explicit state tracking (WARNING, GRACEFUL, FORCE, CLEANUP).
- **Supervisor**: Implemented `shutdown()` to stop services in LIFO order and clear process registry.
- **Plugin Loader**: Implemented `teardown()` and shutdown hooks (`on_shutdown_warning`, `on_shutdown`) to safely stop active plugins.
- **Sandbox**: Patched a security vulnerability where missing C++ core allowed relative path traversal (e.g., `../../etc/passwd`). Added secure Python fallback.

## [0.5.1] - 2025-12-08
### Fixed
- **Critical Security**: Fixed a shell login bypass where failed authentication could fallback to root access.
- **Stability**: Fixed `sys_ls` crash when invoked on file paths.
- **Stability**: Fixed `sys_delete` and `DockerInterface` exception handling.
- **Deadlock**: Fixed a deadlock in the C++ Sandbox Core (`sandbox_core`) when capturing large output from subprocesses.
- **Filesystem**: Fixed `mkdir` logic to correctly raise `FileExistsError` instead of silently succeeding.

### Performance
- **Startup Time**: Reduced kernel startup time by ~90% (from ~1.6s to ~0.15s) by lazy-loading heavy cloud dependencies (`docker`, `kubernetes`).
- **Syscall Optimization**: Optimized `sys_ls` to use efficient type checking instead of exception handling control flow.
- **Sandbox IO**: Optimized `SyscallHandler` to bridge In-Memory and Real Filesystem efficiently for Sandbox paths.

## [0.5.0] - 2025-12-07
### Added
- **Docker Integration**: `sys_docker_*` syscalls, CLI commands, and Agent actions.
- **Kubernetes Integration**: `sys_k8s_*` syscalls, CLI commands, and Agent actions.
- **RBAC Updates**: Added `manage_docker` and `manage_k8s` permissions.
- **Cloud Interface**: `DockerInterface` and `KubernetesInterface` in `kernel.cloud`.

## [0.4.0] - 2025-12-07
### Added
- **Kernel Networking Layer**: Global On/Off Switch, Strict Socket Enforcement, RBAC Integration.
- **NASM Runtime**: C++ FFI Sandbox Extension, `sys_exec_nasm` Syscall.

## [0.3.5] - 2025-12-06
### Added
- **Plugin System**: Configuration storage, C++ Registry Core, Polyglot support (Python/C++/Node).
- **New Plugins**: `github`, `slack_notifier`, `usage_dashboard`, `team_collaboration`.
- **User Management**: Role-based access control (admin/user).
