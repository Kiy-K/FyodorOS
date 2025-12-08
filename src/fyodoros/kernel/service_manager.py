"""
Service Manager.

This module provides the `ServiceManager` class, responsible for managing the lifecycle
of kernel services, ensuring deterministic startup and atomic teardown.
"""

class ServiceManager:
    """
    Manages the lifecycle of services (start, stop, cleanup).
    Ensures robust teardown handling.
    """
    def __init__(self):
        self._services = []

    def register(self, service):
        """
        Register a service with the manager.

        Args:
            service: An object with optional start(), stop(), and cleanup() methods.
        """
        self._services.append(service)

    def start_all(self):
        """
        Start all registered services in order.
        """
        for service in self._services:
            if hasattr(service, 'start'):
                service.start()

    def teardown_all(self):
        """
        Stop and cleanup all services in reverse order.

        Guarantees that cleanup() is called for every service, even if stop() fails.
        Failures in one service do not block the teardown of others.
        """
        # Iterate in reverse order of registration
        for service in reversed(self._services):
            try:
                try:
                    if hasattr(service, 'stop'):
                        service.stop()
                finally:
                    if hasattr(service, 'cleanup'):
                        service.cleanup()
            except Exception:
                # Suppress exceptions to ensure other services are processed
                pass

        # Clear the service list to remove ghost state
        self._services.clear()
