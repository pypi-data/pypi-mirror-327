from __future__ import annotations
from typing import Callable, Dict, List, Optional
from PyQt6.QtCore import Qt
from dataclasses import dataclass


@dataclass
class InputBinding:
    """Represents a single input binding with its conditions and callback"""
    name: str
    priority: int
    callback: Callable[[], bool]
    description: str = ""
    
    def __lt__(self, other):
        return self.priority < other.priority


class InputBindingSystem:
    def __init__(self):
        self._bindings: Dict[str, InputBinding] = {}
        self._active_binding: Optional[str] = None
        
    def register_binding(self, name: str, priority: int, callback: Callable[[], bool], description: str = ""):
        """Register a new input binding"""
        self._bindings[name] = InputBinding(name, priority, callback, description)
        
    def remove_binding(self, name: str):
        """Remove a binding by name"""
        if name in self._bindings:
            del self._bindings[name]
            if self._active_binding == name:
                self._active_binding = None
                
    def check_binding(self, name: str) -> bool:
        """
        Check if a specific binding is active.
        Returns False if:
        1. The binding doesn't exist
        2. The binding's callback returns False
        3. Another binding with higher priority is active
        """
        if name not in self._bindings:
            return False
            
        binding = self._bindings[name]
        
        # If this binding is already active, just check its callback
        if self._active_binding == name:
            is_active = binding.callback()
            if not is_active:
                self._active_binding = None
            return is_active
            
        # Check if the binding's conditions are met
        if not binding.callback():
            return False
            
        # Check if any higher priority bindings are active
        for other_name, other_binding in self._bindings.items():
            if other_binding.priority > binding.priority:
                if other_binding.callback():
                    self._active_binding = other_name
                    return False
                    
        # This binding is now active
        self._active_binding = name
        return True
        
    def get_active_binding(self) -> Optional[str]:
        """Get the name of the currently active binding, if any"""
        return self._active_binding
        
    def clear_active_binding(self):
        """Clear the currently active binding"""
        self._active_binding = None 