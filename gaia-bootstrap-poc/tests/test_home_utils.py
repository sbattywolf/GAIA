"""Tests for home utility functions."""

import pytest
from gaia.home.utils import find_opening_states, is_state_open


def test_find_opening_states():
    """Test finding opening states from a list."""
    states = ['closed', 'open', 'locked', 'opened', 'unknown']
    result = find_opening_states(states)
    expected = ['open', 'opened']
    assert result == expected


def test_is_state_open():
    """Test determining if a state is open."""
    assert is_state_open('open') == True
    assert is_state_open('opened') == True
    assert is_state_open('closed') == False
    assert is_state_open('locked') == False
    assert is_state_open('Open') == True  # Case insensitive


def test_is_state_open_edge_cases():
    """Test edge cases for state opening detection."""
    assert is_state_open('') == False
    assert is_state_open('openings') == True  # Should match substring 'open'
    assert is_state_open('opening') == True   # Should match substring 'open'