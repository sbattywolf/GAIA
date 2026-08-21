#!/usr/bin/env python3
"""
Unit tests for GAIA Target Host Preflight utility
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the current directory to path so we can import gaia_preflight
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gaia_preflight import PreflightChecker

class TestPreflightChecker(unittest.TestCase):
    
    def setUp(self):
        self.checker = PreflightChecker(verbose=False)
    
    def test_init(self):
        """Test that checker initializes correctly"""
        # Timestamp is automatically set, so we just check it exists
        self.assertIsNotNone(self.checker.results["timestamp"])
        self.assertEqual(len(self.checker.results["checks"]), 0)
    
    def test_add_result(self):
        """Test adding a result"""
        self.checker.add_result("test", "key", "PASS", "OBSERVED", "value", "source")
        self.assertEqual(len(self.checker.results["checks"]), 1)
        
        check = self.checker.results["checks"][0]
        self.assertEqual(check["module"], "test")
        self.assertEqual(check["key"], "key")
        self.assertEqual(check["status"], "PASS")
        self.assertEqual(check["value"], "value")
    
    @patch('platform.node')
    @patch('platform.platform')
    @patch('platform.release')
    @patch('platform.machine')
    def test_check_host_info(self, mock_machine, mock_release, mock_platform, mock_node):
        """Test host info check"""
        mock_node.return_value = "test-host"
        mock_platform.return_value = "Linux-5.4.0-123-generic"
        mock_release.return_value = "5.4.0-123-generic"
        mock_machine.return_value = "x86_64"
        
        self.checker.check_host_info()
        
        # Should have added one check
        self.assertEqual(len(self.checker.results["checks"]), 1)
        
        check = self.checker.results["checks"][0]
        self.assertEqual(check["module"], "host")
        self.assertEqual(check["key"], "info")
        self.assertEqual(check["status"], "PASS")
        self.assertIn("hostname", check["value"])

    @patch('os.getlogin')
    @patch('os.getgroups')
    def test_check_user_info(self, mock_getgroups, mock_getlogin):
        """Test user info check"""
        mock_getlogin.return_value = "testuser"
        mock_getgroups.return_value = [1000, 999]  # No docker group
        
        self.checker.check_user_info()
        
        self.assertEqual(len(self.checker.results["checks"]), 1)
        
        check = self.checker.results["checks"][0]
        self.assertEqual(check["module"], "user")
        self.assertEqual(check["key"], "access")
        self.assertEqual(check["status"], "PASS")

    @patch('subprocess.run')
    def test_check_docker_available(self, mock_run):
        """Test Docker availability check"""
        # Mock successful docker command
        mock_run.side_effect = [
            MagicMock(returncode=0),  # which docker
            MagicMock(returncode=0),  # which docker-compose  
            MagicMock(returncode=0)   # docker info
        ]
        
        self.checker.check_docker()
        
        self.assertEqual(len(self.checker.results["checks"]), 1)
        
        check = self.checker.results["checks"][0]
        self.assertEqual(check["module"], "docker")
        self.assertEqual(check["key"], "availability")
        self.assertEqual(check["status"], "PASS")

    def test_run_all_checks(self):
        """Test running all checks"""
        # Just run without errors - we don't want to actually execute the real system calls
        # in unit tests, but we can at least verify the method runs
        try:
            self.checker.run_all_checks()
            # Should not raise any exceptions
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"run_all_checks raised exception: {e}")

if __name__ == '__main__':
    unittest.main()