"""
RDP File Fetcher — Copies PrtsPrcs from Rossware server via RDP drive mapping.

On Windows Server, uses mstsc.exe with an .rdp file that:
1. Maps the local agent data folder as a drive on the remote session
2. Runs a copy command on the remote side to push PrtsPrcs to the mapped drive
3. Disconnects when done

On Mac/Linux (dev), falls back to smbclient or manual instructions.

The flow:
  RSS Key auth (whitelist IP) → store RDP credentials → connect with drive mapping
  → remote copies PrtsPrcs to \\tsclient\C\... → disconnect → verify file arrived
"""

import json
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path


class RDPFetcher:
    """Fetches PrtsPrcs from Rossware server via RDP drive redirection."""

    def __init__(self, config, log_fn, project_root):
        """
        Args:
            config: dict with rossware connection details
            log_fn: logging function
            project_root: Path to the production/ directory
        """
        self.config = config
        self.log = log_fn
        self.project_root = Path(project_root)
        self.input_dir = self.project_root / "data" / "input"
        self.input_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, timeout_seconds=120):
        """Fetch PrtsPrcs from Rossware server.

        Returns:
            Path to the local PrtsPrcs file, or None if failed.
        """
        system = platform.system()

        if system == "Windows":
            return self._fetch_windows(timeout_seconds)
        else:
            return self._fetch_fallback()

    def _fetch_windows(self, timeout_seconds=120):
        """Windows: Use cmdkey + mstsc with drive redirection and auto-command."""
        host = self.config["host"]
        username = self.config["username"]
        password = self.config["password"]
        remote_path = self.config.get("prtsprcs_remote_path", r"C:\SD\NetData\PrtsPrcs")

        local_dest = self.input_dir / "PrtsPrcs"
        local_dest_win = str(local_dest).replace("/", "\\")

        # The drive letter that gets mapped in RDP
        # When you redirect C:\ in RDP, it appears as \\tsclient\C on the remote
        agent_drive = str(self.project_root.drive or "C:")
        agent_path_no_drive = str(self.input_dir)[2:].replace("/", "\\")  # strip C:
        tsclient_dest = f"\\\\tsclient\\{agent_drive[0]}\\{agent_path_no_drive.lstrip(chr(92))}\\PrtsPrcs"

        self.log(f"RDP Fetch: Connecting to {host} as {username}")
        self.log(f"RDP Fetch: Remote source: {remote_path}")
        self.log(f"RDP Fetch: Local dest: {local_dest_win}")

        # Step 1: Store credentials using cmdkey
        self.log("RDP Fetch: Storing credentials...")
        try:
            subprocess.run(
                ["cmdkey", "/generic:TERMSRV/" + host, "/user:" + username, "/pass:" + password],
                capture_output=True, text=True, timeout=10
            )
        except Exception as e:
            self.log(f"RDP Fetch: Failed to store credentials: {e}")
            return None

        # Step 2: Create .rdp file with drive mapping and auto-command
        rdp_file = self.project_root / "data" / "session" / "fetch_prtsprcs.rdp"
        rdp_file.parent.mkdir(parents=True, exist_ok=True)

        # The copy command runs on the REMOTE server
        # It copies PrtsPrcs to the mapped local drive via \\tsclient
        copy_cmd = f'cmd /c "copy /Y \\"{remote_path}\\" \\"{tsclient_dest}\\" && logoff"'

        rdp_content = f"""screen mode id:i:1
use multimon:i:0
desktopwidth:i:1024
desktopheight:i:768
session bpp:i:32
full address:s:{host}
audiomode:i:2
redirectclipboard:i:1
redirectprinters:i:0
redirectsmartcards:i:0
redirectcomports:i:0
drivestoredirect:s:{agent_drive}\\
autoreconnection enabled:i:0
authentication level:i:0
prompt for credentials:i:0
negotiate security layer:i:1
alternate shell:s:{copy_cmd}
shell working directory:s:
username:s:{username}
"""

        rdp_file.write_text(rdp_content)
        self.log(f"RDP Fetch: Created RDP file: {rdp_file.name}")

        # Step 3: Archive existing PrtsPrcs if present
        if local_dest.exists():
            archive_dir = self.project_root / "data" / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_dir / f"PrtsPrcs_{ts}"
            shutil.copy2(local_dest, archive_path)
            self.log(f"RDP Fetch: Archived existing file to {archive_path.name}")

        # Record the file's current mtime (or note it doesn't exist)
        old_mtime = local_dest.stat().st_mtime if local_dest.exists() else 0

        # Step 4: Launch RDP connection
        self.log("RDP Fetch: Launching RDP session...")
        try:
            proc = subprocess.Popen(
                ["mstsc", str(rdp_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            self.log("RDP Fetch: mstsc.exe not found. Is this Windows?")
            return None

        # Step 5: Wait for the file to appear/update
        self.log(f"RDP Fetch: Waiting up to {timeout_seconds}s for file transfer...")
        start = time.time()
        while time.time() - start < timeout_seconds:
            time.sleep(3)

            if local_dest.exists():
                new_mtime = local_dest.stat().st_mtime
                if new_mtime > old_mtime:
                    size_kb = local_dest.stat().st_size / 1024
                    self.log(f"RDP Fetch: File received! {size_kb:.1f} KB")

                    # Clean up credentials
                    try:
                        subprocess.run(
                            ["cmdkey", "/delete:TERMSRV/" + host],
                            capture_output=True, timeout=10
                        )
                    except Exception:
                        pass

                    return local_dest

        self.log("RDP Fetch: Timed out waiting for file transfer.")
        self.log("RDP Fetch: The RDP session may still be running.")

        # Clean up
        try:
            subprocess.run(
                ["cmdkey", "/delete:TERMSRV/" + host],
                capture_output=True, timeout=10
            )
        except Exception:
            pass

        return None

    def _fetch_windows_powershell(self, timeout_seconds=120):
        """Alternative: Use PowerShell remoting if available (WinRM)."""
        host = self.config["host"]
        username = self.config["username"]
        password = self.config["password"]
        remote_path = self.config.get("prtsprcs_remote_path", r"C:\SD\NetData\PrtsPrcs")
        local_dest = self.input_dir / "PrtsPrcs"

        self.log("RDP Fetch: Trying PowerShell remoting...")

        ps_script = f"""
$secpasswd = ConvertTo-SecureString '{password}' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ('{username}', $secpasswd)
$session = New-PSSession -ComputerName '{host}' -Credential $cred -ErrorAction Stop
Copy-Item -Path '{remote_path}' -Destination '{local_dest}' -FromSession $session
Remove-PSSession $session
Write-Output 'SUCCESS'
"""

        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True, text=True, timeout=timeout_seconds
            )

            if "SUCCESS" in result.stdout:
                self.log("RDP Fetch: File copied via PowerShell remoting!")
                return local_dest
            else:
                self.log(f"RDP Fetch: PS remoting failed: {result.stderr[:300]}")
                return None

        except subprocess.TimeoutExpired:
            self.log("RDP Fetch: PowerShell remoting timed out.")
            return None
        except FileNotFoundError:
            self.log("RDP Fetch: PowerShell not available.")
            return None

    def _fetch_fallback(self):
        """Non-Windows: Check if file exists locally or give instructions."""
        local_dest = self.input_dir / "PrtsPrcs"

        if local_dest.exists():
            age_hours = (time.time() - local_dest.stat().st_mtime) / 3600
            size_kb = local_dest.stat().st_size / 1024
            self.log(f"RDP Fetch: Using existing PrtsPrcs ({size_kb:.1f} KB, {age_hours:.1f}h old)")

            if age_hours > 24:
                self.log("RDP Fetch: WARNING — file is >24h old. Consider updating.")

            return local_dest

        self.log("RDP Fetch: PrtsPrcs not found locally and RDP automation")
        self.log("  requires Windows. Copy the file manually:")
        self.log(f"  1. RDP into {self.config['host']}")
        self.log(f"  2. Copy C:\\SD\\NetData\\PrtsPrcs")
        self.log(f"  3. Place it in: {self.input_dir}")
        return None
