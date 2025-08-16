#!/usr/bin/env python3
"""
Smart Play Bot Scheduler - Optimized Version
Executes smart_play_bot.py within a configurable daily time window with process monitoring
"""

import os
import sys
import time
import signal
import subprocess
import psutil
import logging
from datetime import datetime, time as dt_time, timedelta
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotScheduler:
    def __init__(self):
        self.bot_process = None
        self.start_time = None
        self.bot_dir = "../Smart_Play_Bot"
        # Execution window configuration
        self.window_start_time = dt_time(0, 0)
        self.window_end_time = dt_time(9, 0)
        # Flag to track if we have executed in current window
        self.has_executed_in_window = False
        
    def is_time_to_run(self):
        """Check if current time is within execution window."""
        now = datetime.now().time()
        return self.window_start_time <= now <= self.window_end_time
    
    def wait_until_execution_time(self):
        """Wait until execution window starts. Returns True if should continue."""
        now = datetime.now()
        today_start = datetime.combine(now.date(), self.window_start_time)
        today_end = datetime.combine(now.date(), self.window_end_time)

        if now < today_start:
            target_datetime = today_start
        elif now <= today_end:
            logger.info(f"Execution window active ({self.window_start_time.strftime('%H:%M')} - {self.window_end_time.strftime('%H:%M')})")
            return True
        else:
            # Past today's window
            if not self.has_executed_in_window:
                logger.info(f"Initial execution: Waiting until tomorrow ({self.window_start_time.strftime('%H:%M')})")
                target_datetime = datetime.combine(now.date() + timedelta(days=1), self.window_start_time)
            else:
                logger.info("Execution window ended. Scheduler finished.")
                return False

        # Wait for target time
        wait_seconds = (target_datetime - now).total_seconds()
        if wait_seconds > 0:
            logger.info(f"Waiting {wait_seconds/3600:.1f} hours until execution window")
            
            # Sleep in 1-hour intervals for long waits
            while wait_seconds > 3600:
                time.sleep(3600)
                wait_seconds -= 3600
                logger.info(f"Still waiting {wait_seconds/3600:.1f} hours...")
            
            if wait_seconds > 0:
                time.sleep(wait_seconds)

        return True
    
    def cleanup_processes(self):
        """Clean up bot and browser processes"""
        # Kill bot process
        if self.bot_process and self.bot_process.poll() is None:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
            except (subprocess.TimeoutExpired, Exception):
                try:
                    self.bot_process.kill()
                except:
                    pass
        
        # Kill browser processes
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and any(browser in proc.info['name'].lower() 
                                           for browser in ['chrome', 'chromium', 'chromedriver']):
                    try:
                        proc.terminate()
                        proc.wait(timeout=3)
                    except:
                        pass
        except:
            pass
        
        self.bot_process = None
        self.start_time = None
    
    def run_bot(self):
        """Execute the smart play bot"""
        try:
            self.start_time = time.time()
            
            # Prepare command
            if os.name == 'nt':  # Windows
                cmd = ["venv/Scripts/python.exe", "-u", "smart_play_bot.py"]
            else:  # Unix/Linux/macOS
                cmd = ["venv/bin/python", "-u", "smart_play_bot.py"]
            
            # Prepare environment
            env = os.environ.copy()
            env.pop('VIRTUAL_ENV', None)
            env.pop('PYTHONHOME', None)
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # Set PYTHONPATH
            if os.name == 'nt':
                site_packages = os.path.join(self.bot_dir, "venv", "Lib", "site-packages")
            else:
                import glob
                python_dirs = glob.glob(os.path.join(self.bot_dir, "venv", "lib", "python*"))
                site_packages = os.path.join(python_dirs[0], "site-packages") if python_dirs else ""
            
            env['PYTHONPATH'] = os.path.abspath(site_packages)
            
            self.bot_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combine stderr into stdout
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=self.bot_dir,
                env=env
            )
            
            logger.info(f"Bot started (PID: {self.bot_process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False
    
    def monitor_bot(self):
        """Monitor bot execution"""
        output_lines = []
        
        while True:
            if not self.bot_process:
                break
                
            # Check if process finished
            if self.bot_process.poll() is not None:
                # Get remaining output
                remaining_output, _ = self.bot_process.communicate()
                if remaining_output:
                    output_lines.extend(remaining_output.strip().split('\n'))
                
                # Analyze result
                return_code = self.bot_process.returncode
                
                if return_code == 0:
                    # Exit code 0: Payment successful - terminate scheduler
                    logger.info("[SUCCESS] Bot completed successfully with payment")
                    return "SUCCESS"
                elif return_code == 1:
                    # Exit code 1: Payment failed but bot ran normally - continue polling
                    logger.warning("[INCOMPLETE] Bot completed but payment failed, will retry")
                    return "INCOMPLETE"
                else:
                    # Other exit codes: Bot crashed or unexpected error - continue polling
                    logger.error(f"[FAILED] Bot failed with exit code {return_code}, will retry")
                    # Show last few lines of output for debugging
                    last_lines = output_lines[-3:] if len(output_lines) >= 3 else output_lines
                    for line in last_lines:
                        if line.strip():
                            logger.error(f"Bot output: {line.strip()}")
                    return "FAILED"
            
            # Read output line by line
            try:
                line = self.bot_process.stdout.readline()
                if line:
                    line = line.strip()
                    if line:  # Only log non-empty lines
                        output_lines.append(line)
                        # Only print important messages to console
                        if any(keyword in line.lower() for keyword in 
                               ['login', 'error', 'payment', 'booking', 'success', 'failed']):
                            print(f"[BOT] {line}")
            except:
                pass
            
            time.sleep(0.1)
        
        return "UNKNOWN"
    
    def run_scheduler(self):
        """Main scheduler loop"""
        logger.info("[START] Smart Play Bot Scheduler started")
        
        # Wait until execution window
        if not self.wait_until_execution_time():
            return
        
        while True:
            try:
                # Check execution window
                if not self.is_time_to_run():
                    now = datetime.now().time()
                    if now > self.window_end_time:
                        if self.has_executed_in_window:
                            logger.info("Execution window ended. Scheduler finished.")
                            break
                        else:
                            if not self.wait_until_execution_time():
                                break
                            continue
                    else:
                        if not self.wait_until_execution_time():
                            break
                        continue
                
                # Clean up and start bot
                self.cleanup_processes()
                
                if self.run_bot():
                    self.has_executed_in_window = True
                    result = self.monitor_bot()
                    
                    if result == "SUCCESS":
                        logger.info("[SUCCESS] Scheduler completed successfully!")
                        break
                    elif result in ["INCOMPLETE", "FAILED"]:
                        logger.info("[RETRY] Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        time.sleep(5)
                else:
                    logger.error("Failed to start bot, retrying in 5 seconds...")
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                logger.info("[STOP] Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(30)
        
        self.cleanup_processes()
        logger.info("[END] Scheduler finished")

def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown"""
    logger.info(f"Received signal {signum}, shutting down gracefully")
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check prerequisites
    bot_script = Path("../Smart_Play_Bot/smart_play_bot.py")
    venv_path = Path("../Smart_Play_Bot/venv")
    
    if not bot_script.exists():
        logger.error("[ERROR] smart_play_bot.py not found")
        sys.exit(1)
    
    if not venv_path.exists():
        logger.error("[ERROR] Virtual environment not found")
        sys.exit(1)
    
    # Run scheduler
    scheduler = BotScheduler()
    scheduler.run_scheduler()