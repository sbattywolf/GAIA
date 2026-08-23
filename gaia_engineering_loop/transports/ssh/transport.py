#!/usr/bin/env python3
"""
GAIA Engineering Loop SSH Transport Layer

This module provides a minimal, robust SSH transport for the engineering loop.
It handles connection, command execution, timeouts, and structured result capture.
"""

import paramiko
import json
import sys
import time
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class SSHResult:
    """Structured result from SSH operations"""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    error_message: Optional[str] = None
    connection_time: float = 0.0

class SSHTransport:
    """Minimal SSH transport for GAIA engineering loop"""
    
    def __init__(self, hostname: str, username: str, port: int = 22, 
                 timeout: int = 30, key_filename: Optional[str] = None):
        self.hostname = hostname
        self.username = username
        self.port = port
        self.timeout = timeout
        self.key_filename = key_filename
        self.client = None
        
    def connect(self) -> SSHResult:
        """Establish SSH connection"""
        start_time = time.time()
        
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect with timeout and key if provided
            if self.key_filename:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_filename,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False
                )
            else:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False
                )
            
            connection_time = time.time() - start_time
            return SSHResult(
                success=True,
                stdout="",
                stderr="",
                exit_code=0,
                connection_time=connection_time
            )
            
        except Exception as e:
            connection_time = time.time() - start_time
            return SSHResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=1,
                error_message=f"SSH connection failed: {str(e)}",
                connection_time=connection_time
            )
    
    def execute(self, command: str) -> SSHResult:
        """Execute a command on the remote host"""
        if not self.client:
            return SSHResult(
                success=False,
                stdout="",
                stderr="Not connected",
                exit_code=1,
                error_message="Not connected to target"
            )
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=self.timeout)
            
            # Get the output
            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')
            
            # Get exit status
            exit_status = stdout.channel.recv_exit_status()
            
            return SSHResult(
                success=True,
                stdout=stdout_data.strip(),
                stderr=stderr_data.strip(),
                exit_code=exit_status
            )
            
        except Exception as e:
            return SSHResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=1,
                error_message=f"Command execution failed: {str(e)}"
            )
    
    def close(self):
        """Close the SSH connection"""
        if self.client:
            self.client.close()

def test_connection(hostname: str, username: str, key_file: Optional[str] = None) -> Dict:
    """Test SSH connection and return structured result"""
    transport = SSHTransport(hostname, username, key_filename=key_file)
    
    # Test connection
    connect_result = transport.connect()
    
    if not connect_result.success:
        return {
            "event": "TRANSPORT_FAILURE",
            "layer": "transport", 
            "retryable": True,
            "component": "ssh_transport",
            "reason": "connection_failed",
            "error_message": connect_result.error_message,
            "success": False
        }
    
    # Test basic command execution
    cmd_result = transport.execute("hostname")
    transport.close()
    
    if not cmd_result.success:
        return {
            "event": "TRANSPORT_FAILURE", 
            "layer": "transport",
            "retryable": True,
            "component": "ssh_transport",
            "reason": "command_execution_failed",
            "error_message": cmd_result.error_message,
            "success": False
        }
    
    return {
        "event": "TRANSPORT_SUCCESS",
        "layer": "transport",
        "retryable": False,
        "component": "ssh_transport", 
        "success": True,
        "hostname": cmd_result.stdout,
        "connection_time": connect_result.connection_time
    }

def main():
    """Main function for testing the transport"""
    if len(sys.argv) < 2:
        print("Usage: python3 transport.py <hostname> [username] [key_file]")
        return
    
    hostname = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "sbatta"
    key_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = test_connection(hostname, username, key_file)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()