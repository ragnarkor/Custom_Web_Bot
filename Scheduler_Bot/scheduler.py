#!/usr/bin/env python3
"""
Smart Play Bot Scheduler
Executes smart_play_bot.py within a configurable daily time window with process monitoring
Automatically updates config.yml dates to current date + 6 days
"""

import os
import sys
import time
import signal
import subprocess
import psutil
import logging
import yaml
from datetime import datetime, time as dt_time, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotScheduler:
    def __init__(self):
        self.bot_process = None
        self.start_time = None
        self.max_runtime = 15 * 60  # 15 minutes in seconds
        self.bot_dir = "../Smart_Play_Bot"
        # Execution window configuration (single source of truth)
        # Update these two values to change the allowed run window
        self.window_start_time = dt_time(0, 0)  # start of window (HH:MM)
        self.window_end_time = dt_time(9, 0)     # end of window (HH:MM)
        
    def update_config_dates(self):
        """Update config.yml dates to current date + 6 days"""
        try:
            config_file = Path(self.bot_dir) / "config.yml"
            if not config_file.exists():
                logger.error(f"Config file not found: {config_file}")
                return False
            
            # Calculate target date (current date + 6 days)
            today = datetime.now()
            target_date = today + timedelta(days=6)
            target_month = str(target_date.month)
            target_day = str(target_date.day)
            
            logger.info(f"Current date: {today.strftime('%Y-%m-%d')}")
            logger.info(f"Target date (+6 days): {target_date.strftime('%Y-%m-%d')}")
            logger.info(f"Month: {target_month}, Day: {target_day}")
            
            # Read existing config
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Update dates
            config['booking_month'] = target_month
            config['booking_day'] = target_day
            
            # Write back to file
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            logger.info(f"Successfully updated config: booking_month = {target_month}, booking_day = {target_day}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update config dates: {e}")
            return False
    
    def is_time_to_run(self):
        """Check if current time is within configured execution window."""
        now = datetime.now().time()
        return self.window_start_time <= now <= self.window_end_time
    
    def wait_until_execution_time(self):
        """Wait until the configured execution window starts."""
        now = datetime.now()
        today_start = datetime.combine(now.date(), self.window_start_time)
        today_end = datetime.combine(now.date(), self.window_end_time)

        if now < today_start:
            target_datetime = today_start
        elif now <= today_end:
            # Already inside the window; no waiting needed
            logger.info(
                f"Execution time window already active "
                f"({self.window_start_time.strftime('%H:%M')} - {self.window_end_time.strftime('%H:%M')}). Proceeding."
            )
            return
        else:
            # Wait until tomorrow's window start
            target_datetime = datetime.combine(now.date() + timedelta(days=1), self.window_start_time)

        wait_seconds = (target_datetime - now).total_seconds()
        if wait_seconds > 0:
            start_label = self.window_start_time.strftime('%H:%M')
            logger.info(f"Waiting {wait_seconds:.0f} seconds until execution time window starts ({start_label})")

            # Sleep in 1-minute intervals
            while wait_seconds > 60:
                time.sleep(60)
                wait_seconds -= 60
                logger.info(f"Still waiting {wait_seconds:.0f} seconds...")

            if wait_seconds > 0:
                time.sleep(wait_seconds)

        start_label = self.window_start_time.strftime('%H:%M')
        logger.info(f"Execution time window started ({start_label})")
    
    def kill_browser_processes(self):
        """Kill all Chrome/Chromium browser processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and any(browser in proc.info['name'].lower() 
                                               for browser in ['chrome', 'chromium', 'chromedriver']):
                        logger.info(f"Killing browser process: {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.terminate()
                        proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    continue
        except Exception as e:
            logger.error(f"Error killing browser processes: {e}")
    
    def kill_bot_process(self):
        """Kill the bot process if it's running"""
        if self.bot_process and self.bot_process.poll() is None:
            try:
                logger.info("Terminating bot process")
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("Bot process didn't terminate gracefully, force killing")
                self.bot_process.kill()
            except Exception as e:
                logger.error(f"Error terminating bot process: {e}")
    
    def check_timeout(self):
        """Check if bot has been running too long"""
        if self.start_time and self.bot_process and self.bot_process.poll() is None:
            elapsed = time.time() - self.start_time
            if elapsed > self.max_runtime:
                logger.warning(f"Bot running for {elapsed:.1f}s, exceeding {self.max_runtime}s limit")
                return True
        return False
    
    def run_bot(self):
        """Execute the smart play bot"""
        try:
            logger.info("Starting Smart Play Bot")
            self.start_time = time.time()
            
            # Change to Smart_Play_Bot directory and run bot
            bot_dir = "../Smart_Play_Bot"
            if os.name == 'nt':  # Windows
                cmd = ["../venv/Scripts/python.exe", "-u", "smart_play_bot.py"]
            else:  # Unix/Linux/macOS
                cmd = ["../venv/bin/python", "-u", "smart_play_bot.py"]
            
            self.bot_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=bot_dir,  # Set working directory
                bufsize=0,    # Unbuffered
                universal_newlines=True
            )
            
            logger.info(f"Bot process started with PID: {self.bot_process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False
    
    def monitor_bot(self):
        """Monitor bot execution and handle various scenarios"""
        # Collect all output
        all_stdout = []
        all_stderr = []
        
        while True:
            if not self.bot_process:
                break
                
            # Check if process is still running
            if self.bot_process.poll() is not None:
                # Process has finished
                stdout, stderr = self.bot_process.communicate()
                return_code = self.bot_process.returncode
                
                # Add any remaining output
                if stdout:
                    all_stdout.append(stdout)
                if stderr:
                    all_stderr.append(stderr)
                
                # Check if bot actually completed the payment process
                full_stdout = "".join(all_stdout)
                full_stderr = "".join(all_stderr)
                
                if return_code == 0 and "payment" in full_stdout.lower():
                    logger.info("Bot completed successfully with payment")
                    return "SUCCESS"
                elif return_code == 0:
                    logger.warning("Bot exited with code 0 but may not have completed payment")
                    logger.info("STDOUT: " + full_stdout[-500:])  # Last 500 chars
                    logger.info("STDERR: " + full_stderr[-500:])  # Last 500 chars
                    return "INCOMPLETE"
                else:
                    logger.error(f"Bot failed with return code: {return_code}")
                    logger.error(f"STDOUT: {full_stdout[-500:]}")
                    logger.error(f"STDERR: {full_stderr[-500:]}")
                    return "FAILED"
            
            # Check for timeout
            if self.check_timeout():
                self.kill_bot_process()
                self.kill_browser_processes()
                return "TIMEOUT"
            
            # Try to read output in real-time (non-blocking)
            try:
                # Check if there's data available without blocking
                import select
                
                # Check stdout
                if select.select([self.bot_process.stdout], [], [], 0)[0]:
                    stdout_line = self.bot_process.stdout.readline()
                    if stdout_line:
                        line = stdout_line.strip()
                        print(f"[BOT] {line}")  # Print to console
                        logger.info(f"[BOT] {line}")  # Log to file
                        all_stdout.append(line + "\n")
                
                # Check stderr
                if select.select([self.bot_process.stderr], [], [], 0)[0]:
                    stderr_line = self.bot_process.stderr.readline()
                    if stderr_line:
                        line = stderr_line.strip()
                        print(f"[ERROR] {line}")  # Print to console
                        logger.error(f"[ERROR] {line}")  # Log to file
                        all_stderr.append(line + "\n")
                    
            except Exception as e:
                # If non-blocking read fails, continue
                pass
            
            time.sleep(0.1)  # Check more frequently for output
        
        return "UNKNOWN"
    
    def cleanup(self):
        """Clean up processes and resources"""
        self.kill_bot_process()
        self.kill_browser_processes()
        self.bot_process = None
        self.start_time = None
    
    def run_scheduler(self):
        """Main scheduler loop"""
        logger.info("Smart Play Bot Scheduler started")
        
        # Initialize: update config dates and generate random execution time
        logger.info("Initializing scheduler...")
        if not self.update_config_dates():
            logger.error("Failed to update config dates, exiting")
            return
        
        # Wait until the execution window starts
        self.wait_until_execution_time()
        
        while True:
            try:
                current_time = datetime.now()
                
                # Update config dates if it's a new day
                if current_time.date() != getattr(self, '_last_date', None):
                    logger.info(f"New day detected. Updating config dates...")
                    if self.update_config_dates():
                        self._last_date = current_time.date()
                
                # Check if we are within the execution window
                if not self.is_time_to_run():
                    start_label = self.window_start_time.strftime('%H:%M')
                    end_label = self.window_end_time.strftime('%H:%M')
                    logger.info(f"Outside execution time window ({start_label} - {end_label}), waiting until {start_label}")
                    self.wait_until_execution_time()
                    continue
                
                # Clean up any existing processes
                self.cleanup()
                
                # Start the bot
                if self.run_bot():
                    # Monitor the bot
                    result = self.monitor_bot()
                    
                    if result == "SUCCESS":
                        logger.info("Bot completed successfully with payment. Scheduler finished.")
                        break
                    elif result == "INCOMPLETE":
                        logger.warning("Bot exited but may not have completed payment, will retry")
                        time.sleep(5)  # Wait before retry
                    elif result == "TIMEOUT":
                        logger.warning("Bot timed out, will retry")
                        time.sleep(5)  # Wait before retry
                    elif result == "FAILED":
                        logger.error("Bot failed, will retry")
                        time.sleep(5)  # Wait before retry
                    else:
                        logger.warning("Bot ended unexpectedly, will retry")
                        time.sleep(5)  # Wait before retry
                else:
                    logger.error("Failed to start bot, waiting before retry")
                    time.sleep(10)  # Wait before retry
                    
            except KeyboardInterrupt:
                logger.info("Scheduler interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in scheduler: {e}")
                time.sleep(10)
        
        # Final cleanup
        self.cleanup()
        logger.info("Scheduler finished")

def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown"""
    logger.info(f"Received signal {signum}, shutting down gracefully")
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check if bot script exists
    if not Path("../Smart_Play_Bot/smart_play_bot.py").exists():
        logger.error("smart_play_bot.py not found in ../Smart_Play_Bot directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_path = Path("../Smart_Play_Bot/venv")
    if not venv_path.exists():
        logger.error("Virtual environment not found in ../Smart_Play_Bot directory")
        sys.exit(1)
    
    # Create and run scheduler
    scheduler = BotScheduler()
    scheduler.run_scheduler()
