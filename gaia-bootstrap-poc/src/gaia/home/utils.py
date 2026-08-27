"""Simple utility functions for GAIA home management."""

from typing import List, Optional


def find_opening_states(states: List[str]) -> List[str]:
    """
    Find all opening states from a list of state strings.
    
    Args:
        states: List of state strings
        
    Returns:
        List of states that represent opening states
    """
    opening_keywords = ['open', 'opened']
    return [state for state in states if any(keyword in state.lower() for keyword in opening_keywords)]


def is_state_open(state: str) -> bool:
    """
    Determine if a state string represents an open state.
    
    Args:
        state: State string to evaluate
        
    Returns:
        True if the state represents an open condition
    """
    return any(keyword in state.lower() for keyword in ['open', 'opened'])