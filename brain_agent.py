
import logging
import sys
import time
import os
import shutil
from pathlib import Path
from src.agents.main_agent import MainAgent

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('brain.log')
    ]
)
logger = logging.getLogger("BrainAgent")

class BrainAgent:
    """
    The 'Muscle' / Brain of the Digital FTE.
    Watches /Needs_Action for .md files and executes them.
    Implements the 'Ralph Wiggum' loop concept (keep processing until Done).
    """
    def __init__(self):
        self.vault_path = Path("data/vault")
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.main_agent = MainAgent()
        
        # Ensure dirs
        self.done.mkdir(parents=True, exist_ok=True)
        
    def initialize(self):
        self.main_agent.initialize()
        logger.info("Brain: Initialized and ready to process Tasks.")

    def process_file(self, file_path: Path):
        """Read .md file, decide action, and execute"""
        try:
            content = file_path.read_text(encoding="utf-8")
            logger.info(f"Brain: Processing {file_path.name}...")
            
            # Simple metadata parsing (yaml-like header)
            # In a real Claude Code setup, Claude reads this naturally.
            # Here we parse it manually to trigger specific agents.
            
            source_type = "unknown"
            if "type: whatsapp" in content: source_type = "whatsapp"
            elif "type: email" in content: source_type = "email"
            
            # Extract basic info (mock AI reading)
            # We call the 'process_trigger' hook we added earlier!
            # Since we have the raw data in the MD (under ## Context usually), we can try to re-parse or just pass generic.
            
            # Trigger Action
            self.main_agent.process_trigger(
                source=source_type, 
                event_data={"filename": file_path.name, "content": content[:200]}
            )
            
            # Ralph Wiggum Loop: "Are we done?"
            # For this MVP, we assume success after trigger.
            # Move to Done
            shutil.move(str(file_path), str(self.done / file_path.name))
            logger.info(f"Brain: Task {file_path.name} moved to Done.")
            
        except Exception as e:
            logger.error(f"Brain: Error processing {file_path.name}: {e}")

    def run_loop(self):
        self.initialize()
        logger.info(f"Brain: Watching {self.needs_action}...")
        
        while True:
            # Check for .md files
            files = list(self.needs_action.glob("*.md"))
            for file in files:
                self.process_file(file)
            
            time.sleep(5) # Ralph Wiggum pauses to think

if __name__ == "__main__":
    brain = BrainAgent()
    try:
        brain.run_loop()
    except KeyboardInterrupt:
        pass
