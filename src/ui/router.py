"""Screen router for managing screen navigation and content swapping."""

import tkinter as tk
from typing import Callable, Dict, Optional


# Type alias for screen builder function
ScreenBuilder = Callable[[tk.Widget], tk.Frame]


class Router:
    """Manages screen registration and display in the content area."""

    def __init__(self, content_area: tk.Widget):
        """
        Initialize the router.

        Args:
            content_area: The parent widget (Frame) where screens will be mounted.
        """
        self.content_area = content_area
        self._screen_registry: Dict[str, ScreenBuilder] = {}
        self._current_screen: Optional[tk.Frame] = None
        self._current_screen_name: Optional[str] = None

    def register_screen(self, name: str, builder_fn: ScreenBuilder) -> None:
        """
        Register a screen builder function.

        Args:
            name: Unique screen name (e.g., "dashboard", "schedule").
            builder_fn: Callable that takes a parent widget and returns a Frame.
        """
        self._screen_registry[name] = builder_fn

    def show_screen(self, name: str) -> bool:
        """
        Show a registered screen by name.

        Args:
            name: Screen name to show.

        Returns:
            True if screen was found and shown, False otherwise.
        """
        if name not in self._screen_registry:
            print(f"Warning: Screen '{name}' not registered")
            return False

        # Destroy/hide current screen
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

        # Build and mount new screen
        builder_fn = self._screen_registry[name]
        self._current_screen = builder_fn(self.content_area)
        self._current_screen.pack(fill=tk.BOTH, expand=True)
        self._current_screen_name = name

        return True

    def get_current_screen(self) -> Optional[str]:
        """Get the name of the currently displayed screen."""
        return self._current_screen_name

    def is_screen_registered(self, name: str) -> bool:
        """Check if a screen is registered."""
        return name in self._screen_registry

    def get_registered_screens(self) -> list[str]:
        """Get list of all registered screen names."""
        return list(self._screen_registry.keys())


# Global router instance (optional, for convenience)
_router_instance: Optional[Router] = None


def init_router(content_area: tk.Widget) -> Router:
    """
    Initialize the global router instance.

    Args:
        content_area: The parent widget where screens will be mounted.

    Returns:
        The Router instance.
    """
    global _router_instance
    _router_instance = Router(content_area)
    return _router_instance


def get_router() -> Optional[Router]:
    """Get the global router instance."""
    return _router_instance


def register_screen(name: str, builder_fn: ScreenBuilder) -> None:
    """Register a screen using the global router."""
    if _router_instance is not None:
        _router_instance.register_screen(name, builder_fn)
    else:
        raise RuntimeError("Router not initialized. Call init_router() first.")


def show_screen(name: str) -> bool:
    """Show a screen using the global router."""
    if _router_instance is not None:
        return _router_instance.show_screen(name)
    else:
        raise RuntimeError("Router not initialized. Call init_router() first.")


if __name__ == "__main__":
    # Smoke test
    root = tk.Tk()
    root.title("Router Smoke Test")
    root.geometry("600x400")

    content = tk.Frame(root, bg="white")
    content.pack(fill=tk.BOTH, expand=True)

    router = Router(content)

    def build_screen1(parent):
        frame = tk.Frame(parent, bg="lightblue")
        tk.Label(frame, text="Screen 1", font=("Arial", 24)).pack(expand=True)
        return frame

    def build_screen2(parent):
        frame = tk.Frame(parent, bg="lightgreen")
        tk.Label(frame, text="Screen 2", font=("Arial", 24)).pack(expand=True)
        return frame

    router.register_screen("screen1", build_screen1)
    router.register_screen("screen2", build_screen2)

    # Test buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.BOTTOM, pady=10)
    tk.Button(btn_frame, text="Screen 1", command=lambda: router.show_screen("screen1")).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Screen 2", command=lambda: router.show_screen("screen2")).pack(side=tk.LEFT, padx=5)

    router.show_screen("screen1")
    root.mainloop()