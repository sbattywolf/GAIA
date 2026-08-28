#!/usr/bin/env python3
"""
GAIA Target Host Preflight Utility
Minimal utility to verify target machine readiness for GAIA experiments.
"""

import os
import sys
import json
import subprocess
import platform
from datetime import datetime
import argparse

class PreflightChecker:
    def __init__(self, verbose=False, output_file=None):
        self.verbose = verbose
        self.output_file = output_file
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }
    
    def add_result(self, module, key, status, evidence_class, value, source, warnings=None):
        """Add a check result to the results list"""
        result = {
            "module": module,
            "key": key,
            "status": status,  # PASS/FAIL/BLOCKED/UNKNOWN
            "evidence_class": evidence_class,  # OBSERVED/INFERRED/UNKNOWN
            "value": value,
            "source": source,
            "warnings": warnings or []
        }
        
        if self.verbose:
            print(f"[{status}] {module}.{key}: {value}")
            
        self.results["checks"].append(result)
    
    def run_check(self, module, key, check_func, *args, **kwargs):
        """Run a check function and add the result"""
        try:
            value, warnings = check_func(*args, **kwargs)
            self.add_result(module, key, "PASS", "OBSERVED", value, "system", warnings)
        except Exception as e:
            if self.verbose:
                print(f"[FAIL] {module}.{key}: {str(e)}")
            self.add_result(module, key, "FAIL", "UNKNOWN", str(e), "system", [str(e)])
    
    def check_host_info(self):
        """Check basic host information"""
        def _check():
            hostname = platform.node()
            os_name = platform.platform()
            kernel = platform.release()
            arch = platform.machine()
            
            return {
                "hostname": hostname,
                "os": os_name,
                "kernel": kernel,
                "architecture": arch
            }, []
        
        self.run_check("host", "info", _check)
    
    def check_user_info(self):
        """Check user and group information"""
        def _check():
            current_user = os.getlogin()
            
            # Check Docker group membership
            try:
                groups = os.getgroups()
                docker_group = None
                for gid in groups:
                    try:
                        group_name = os.getgrgid(gid).gr_name
                        if group_name == "docker":
                            docker_group = group_name
                            break
                    except KeyError:
                        continue
                has_docker_access = docker_group is not None
            except Exception:
                has_docker_access = False
            
            return {
                "user": current_user,
                "has_docker_access": has_docker_access
            }, []
        
        self.run_check("user", "access", _check)
    
    def check_docker(self):
        """Check Docker availability and access"""
        def _check():
            warnings = []
            
            # Check if docker command exists
            try:
                subprocess.run(["which", "docker"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, 
                             check=True)
                docker_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                docker_available = False
            
            # Check if docker compose exists
            try:
                subprocess.run(["which", "docker-compose"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, 
                             check=True)
                compose_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                compose_available = False
                
            # Check if docker daemon is reachable without sudo
            docker_daemon_reachable = False
            if docker_available:
                try:
                    subprocess.run(["docker", "info"], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL, 
                                 check=True)
                    docker_daemon_reachable = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # This might be expected if user doesn't have access
                    pass
            
            # If Docker is available but daemon is not reachable, that's a problem
            if docker_available and not docker_daemon_reachable:
                warnings.append("Docker daemon inaccessible without sudo")
            
            return {
                "docker_available": docker_available,
                "compose_available": compose_available,
                "daemon_reachable": docker_daemon_reachable
            }, warnings
        
        self.run_check("docker", "availability", _check)
    
    def check_nvidia(self):
        """Check NVIDIA GPU information"""
        def _check():
            warnings = []
            
            # Check if nvidia-smi exists
            try:
                result = subprocess.run(["which", "nvidia-smi"], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL, 
                                      check=True)
                nvidia_smi_exists = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                nvidia_smi_exists = False
            
            if not nvidia_smi_exists:
                return {
                    "nvidia_smi_available": False,
                    "gpu_info": None
                }, ["nvidia-smi not found - GPU checks skipped"]
            
            # Get GPU info
            try:
                result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", 
                                       "--format=csv,noheader,nounits"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      text=True, check=True)
                
                lines = result.stdout.strip().split('\n')
                if lines:
                    gpu_name = lines[0].split(',')[0].strip()
                    vram = lines[0].split(',')[1].strip() + " MB"
                    return {
                        "nvidia_smi_available": True,
                        "gpu_info": {
                            "name": gpu_name,
                            "vram": vram
                        }
                    }, []
                else:
                    return {
                        "nvidia_smi_available": True,
                        "gpu_info": None
                    }, ["No GPU information found"]
                    
            except Exception as e:
                return {
                    "nvidia_smi_available": True,
                    "gpu_info": None
                }, [f"Error getting GPU info: {str(e)}"]
        
        self.run_check("nvidia", "gpu_info", _check)
    
    def check_ollama(self):
        """Check host Ollama installation"""
        def _check():
            warnings = []
            
            # Check if ollama command exists
            try:
                result = subprocess.run(["which", "ollama"], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL, 
                                      check=True)
                ollama_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                ollama_available = False
            
            if not ollama_available:
                return {
                    "ollama_available": False,
                    "endpoint": None,
                    "version": None
                }, ["Ollama not installed"]
            
            # Get Ollama version and endpoint info only if we can verify them
            endpoint = None
            version = None
            
            try:
                # Try to get version
                result = subprocess.run(["ollama", "version"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      text=True, check=True)
                version = result.stdout.strip()
            except Exception as e:
                warnings.append(f"Cannot verify Ollama version: {str(e)}")
            
            try:
                # Try to access the API endpoint directly
                api_result = subprocess.run(["curl", "-fsS", "http://127.0.0.1:11434/api/version"],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          text=True)
                if api_result.returncode == 0:
                    endpoint = "http://127.0.0.1:11434"
                else:
                    warnings.append("Ollama API not responding on default port")
            except Exception as e:
                warnings.append(f"Cannot verify Ollama endpoint: {str(e)}")
            
            # Only return valid values if we actually verified them
            return {
                "ollama_available": True,
                "endpoint": endpoint,
                "version": version
            }, warnings
        
        self.run_check("ollama", "host_installation", _check)
    
    def check_workspace(self):
        """Check workspace and filesystem requirements"""
        def _check():
            # Check if GAIA workspace exists - make path relative to script location
            try:
                # Get the directory containing this script
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Navigate up to the repository root (assuming script is in gaia_target_preflight/)
                repo_root = os.path.dirname(script_dir)
                workspace_path = repo_root
                workspace_exists = os.path.exists(workspace_path)
                
                # Check free space (minimum 1GB required for experiments)
                try:
                    statvfs = os.statvfs(workspace_path)
                    free_space = statvfs.f_frsize * statvfs.f_bavail
                    free_gb = free_space / (1024**3)
                    sufficient_space = free_gb >= 1.0
                except Exception:
                    free_gb = 0
                    sufficient_space = False
            except Exception as e:
                workspace_path = "unknown"
                workspace_exists = False
                free_gb = 0
                sufficient_space = False
            
            return {
                "workspace_exists": workspace_exists,
                "free_space_gb": round(free_gb, 2),
                "sufficient_space": sufficient_space,
                "workspace_path": workspace_path
            }, []
        
        self.run_check("filesystem", "workspace", _check)
    
    def check_ports(self):
        """Check port availability for experiments"""
        def _check():
            # Check ports relevant to GAIA experiments
            ports_to_check = [11434, 11435]  # Default Ollama port and our isolated port
            
            port_status = {}
            for port in ports_to_check:
                try:
                    # Try to connect to the port (this won't actually work without root)
                    # but we can check if it's listening using netstat/ss
                    result = subprocess.run(["ss", "-tuln"], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE, 
                                          text=True)
                    if str(port) in result.stdout:
                        port_status[port] = "listening"
                    else:
                        port_status[port] = "available"
                except Exception:
                    # If we can't check, mark as unknown
                    port_status[port] = "unknown"
            
            return {
                "port_status": port_status
            }, []
        
        self.run_check("network", "ports", _check)
    
    def run_all_checks(self):
        """Run all preflight checks"""
        self.check_host_info()
        self.check_user_info()
        self.check_docker()
        self.check_nvidia()
        self.check_ollama()
        self.check_workspace()
        self.check_ports()
        
        # Determine overall result
        failed_checks = [c for c in self.results["checks"] if c["status"] == "FAIL"]
        blocked_checks = [c for c in self.results["checks"] if c["status"] == "BLOCKED"]
        
        # Check if Docker daemon is reachable (mandatory for experiments)
        docker_checks = [c for c in self.results["checks"] if c["module"] == "docker"]
        if docker_checks:
            docker_check = docker_checks[0]
            if docker_check["value"]["docker_available"] and not docker_check["value"]["daemon_reachable"]:
                # Docker available but daemon not reachable - this is a BLOCKED condition
                blocked_checks.append(docker_check)
        
        if failed_checks or blocked_checks:
            self.results["overall_result"] = "BLOCKED" if blocked_checks else "FAIL"
        else:
            self.results["overall_result"] = "PASS"
    
    def print_summary(self):
        """Print a human-readable summary"""
        print("\n" + "="*60)
        print("GAIA TARGET HOST PREFLIGHT SUMMARY")
        print("="*60)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Overall Result: {self.results['overall_result']}")
        print()
        
        # Group checks by module
        modules = {}
        for check in self.results["checks"]:
            module = check["module"]
            if module not in modules:
                modules[module] = []
            modules[module].append(check)
        
        for module, checks in modules.items():
            print(f"{module.upper()}:")
            for check in checks:
                status_icon = {"PASS": "✓", "FAIL": "✗", "BLOCKED": "!", "UNKNOWN": "?"}[check["status"]]
                print(f"  {status_icon} {check['key']}: {check['value']}")
            print()
    
    def generate_evidence(self):
        """Generate machine-readable evidence"""
        if self.output_file:
            with open(self.output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"Generated evidence file: {self.output_file}")

def main():
    parser = argparse.ArgumentParser(description='GAIA Target Host Preflight Utility')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--output', '-o', help='Output JSON evidence file')
    
    args = parser.parse_args()
    
    checker = PreflightChecker(verbose=args.verbose, output_file=args.output)
    checker.run_all_checks()
    checker.print_summary()
    checker.generate_evidence()
    
    # Return appropriate exit code
    if checker.results["overall_result"] == "PASS":
        return 0
    elif checker.results["overall_result"] == "BLOCKED":
        return 1
    else:
        return 2

if __name__ == "__main__":
    sys.exit(main())