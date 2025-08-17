#!/usr/bin/env python3
"""
Expert Document Writer Agent
============================

This agent monitors the codebase for changes and automatically updates documentation
using the master documentation automation prompt. It provides full visibility into
all operations and maintains comprehensive logs.
"""

import os
import sys
import time
import json
import logging
import subprocess
import git
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class ExpertDocWriter:
    """Expert Document Writer Agent for automated documentation management."""
    
    def __init__(self, repo_path: str = ".", log_level: str = "INFO"):
        self.repo_path = Path(repo_path).resolve()
        self.last_update_file = self.repo_path / ".last_docs_update"
        self.docs_dir = self.repo_path / "docs"
        self.log_file = self.repo_path / "docs-agent.log"
        
        # Setup logging
        self.setup_logging(log_level)
        self.logger.info(f"Expert Doc Writer Agent initialized at {self.repo_path}")
        
        # Initialize git repository
        try:
            self.repo = git.Repo(self.repo_path)
            self.logger.info(f"Git repository initialized: {self.repo.working_dir}")
        except git.InvalidGitRepositoryError:
            self.logger.error("Not a git repository!")
            sys.exit(1)
        
        # Load master prompt
        self.master_prompt = self.load_master_prompt()
        
        # Configuration
        self.config = {
            "monitor_interval_hours": 1,
            "check_extensions": [".py", ".js", ".ts", ".java", ".cpp", ".h", ".hpp"],
            "exclude_patterns": ["tests/", "docs/", "*.md", "*.txt", ".git/"],
            "auto_commit": True,
            "auto_push": True,
            "build_timeout_minutes": 30
        }
        
        self.logger.info("Configuration loaded successfully")
    
    def setup_logging(self, log_level: str):
        """Setup comprehensive logging with file and console output."""
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Setup logger
        self.logger = logging.getLogger('ExpertDocWriter')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logging setup complete. Log file: {self.log_file}")
    
    def load_master_prompt(self) -> str:
        """Load the master documentation automation prompt."""
        prompt_file = self.repo_path / "prompts" / "documentation_automation_master.md"
        
        if not prompt_file.exists():
            self.logger.error(f"Master prompt not found: {prompt_file}")
            return ""
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info("Master prompt loaded successfully")
            return content
        except Exception as e:
            self.logger.error(f"Failed to load master prompt: {e}")
            return ""
    
    def get_last_processed_commit(self) -> Optional[str]:
        """Get the last processed commit hash."""
        if self.last_update_file.exists():
            try:
                with open(self.last_update_file, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                self.logger.warning(f"Failed to read last update file: {e}")
        return None
    
    def save_last_processed_commit(self, commit_hash: str):
        """Save the last processed commit hash."""
        try:
            with open(self.last_update_file, 'w') as f:
                f.write(commit_hash)
            self.logger.info(f"Saved last processed commit: {commit_hash[:8]}")
        except Exception as e:
            self.logger.error(f"Failed to save last processed commit: {e}")
    
    def detect_code_changes(self, since_commit: Optional[str] = None) -> Tuple[bool, List[str]]:
        """Detect if there are code changes since the last update."""
        self.logger.info("Detecting code changes...")
        
        try:
            if since_commit:
                # Get diff since specific commit
                diff = self.repo.git.diff('--name-only', since_commit, 'HEAD')
                changed_files = diff.strip().split('\n') if diff.strip() else []
            else:
                # Get changes from last 24 hours
                since_time = datetime.now() - timedelta(hours=24)
                changed_files = []
                for commit in self.repo.iter_commits(since=since_time.strftime('%Y-%m-%d %H:%M:%S')):
                    for parent in commit.parents:
                        diff = self.repo.git.diff('--name-only', parent.hexsha, commit.hexsha)
                        if diff.strip():
                            changed_files.extend(diff.strip().split('\n'))
                changed_files = list(set(changed_files))  # Remove duplicates
            
            # Filter for code files only
            code_changes = []
            for file_path in changed_files:
                if file_path and any(file_path.endswith(ext) for ext in self.config["check_extensions"]):
                    # Check if file is excluded
                    if not any(pattern in file_path for pattern in self.config["exclude_patterns"]):
                        code_changes.append(file_path)
            
            self.logger.info(f"Detected {len(code_changes)} code file changes")
            if code_changes:
                self.logger.info(f"Changed files: {', '.join(code_changes[:5])}{'...' if len(code_changes) > 5 else ''}")
            
            return len(code_changes) > 0, code_changes
            
        except Exception as e:
            self.logger.error(f"Error detecting code changes: {e}")
            return False, []
    
    def build_documentation(self) -> bool:
        """Build the documentation using Sphinx."""
        self.logger.info("Building documentation...")
        
        if not self.docs_dir.exists():
            self.logger.error(f"Documentation directory not found: {self.docs_dir}")
            return False
        
        try:
            # Change to docs directory
            original_dir = os.getcwd()
            os.chdir(self.docs_dir)
            
            # Clean previous build
            self.logger.info("Cleaning previous build...")
            result = subprocess.run(['make', 'clean'], capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                self.logger.warning(f"Clean command output: {result.stderr}")
            
            # Build HTML documentation
            self.logger.info("Building HTML documentation...")
            result = subprocess.run(['make', 'html'], capture_output=True, text=True, timeout=1800)  # 30 minutes
            
            # Return to original directory
            os.chdir(original_dir)
            
            if result.returncode == 0:
                self.logger.info("Documentation built successfully!")
                return True
            else:
                self.logger.error(f"Documentation build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Documentation build timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error building documentation: {e}")
            return False
    
    def commit_documentation_updates(self, commit_message: str) -> bool:
        """Commit documentation updates to git."""
        if not self.config["auto_commit"]:
            self.logger.info("Auto-commit disabled, skipping commit")
            return True
        
        self.logger.info("Committing documentation updates...")
        
        try:
            # Add all changes in docs directory
            self.repo.index.add('docs/')
            
            # Check if there are changes to commit
            if not self.repo.index.diff('HEAD'):
                self.logger.info("No documentation changes to commit")
                return True
            
            # Commit changes
            commit = self.repo.index.commit(commit_message)
            self.logger.info(f"Committed documentation updates: {commit.hexsha[:8]}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to commit documentation updates: {e}")
            return False
    
    def push_documentation_updates(self) -> bool:
        """Push documentation updates to remote repository."""
        if not self.config["auto_push"]:
            self.logger.info("Auto-push disabled, skipping push")
            return True
        
        self.logger.info("Pushing documentation updates...")
        
        try:
            origin = self.repo.remotes.origin
            origin.push()
            self.logger.info("Documentation updates pushed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to push documentation updates: {e}")
            return False
    
    def update_documentation(self) -> bool:
        """Main method to update documentation if needed."""
        self.logger.info("=" * 60)
        self.logger.info("Starting documentation update check")
        self.logger.info("=" * 60)
        
        # Get current commit
        current_commit = self.repo.head.commit.hexsha
        self.logger.info(f"Current commit: {current_commit[:8]}")
        
        # Get last processed commit
        last_processed = self.get_last_processed_commit()
        if last_processed:
            self.logger.info(f"Last processed commit: {last_processed[:8]}")
        else:
            self.logger.info("No previous documentation update found")
        
        # Check if we need to update
        if last_processed == current_commit:
            self.logger.info("Documentation is up to date, no changes needed")
            return True
        
        # Detect code changes
        has_changes, changed_files = self.detect_code_changes(last_processed)
        
        if not has_changes:
            self.logger.info("No code changes detected, updating last processed commit")
            self.save_last_processed_commit(current_commit)
            return True
        
        # Code changes detected, update documentation
        self.logger.info("Code changes detected, updating documentation...")
        
        # Build documentation
        if not self.build_documentation():
            self.logger.error("Documentation build failed, aborting update")
            return False
        
        # Commit updates
        commit_message = f"Auto-update docs for code changes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if not self.commit_documentation_updates(commit_message):
            self.logger.error("Failed to commit documentation updates")
            return False
        
        # Push updates
        if not self.push_documentation_updates():
            self.logger.error("Failed to push documentation updates")
            return False
        
        # Update last processed commit
        self.save_last_processed_commit(current_commit)
        
        self.logger.info("Documentation update completed successfully!")
        return True
    
    def run_monitoring_loop(self):
        """Run the continuous monitoring loop."""
        self.logger.info("Starting continuous monitoring loop...")
        self.logger.info(f"Monitoring interval: {self.config['monitor_interval_hours']} hour(s)")
        
        try:
            while True:
                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"Monitoring cycle started at {datetime.now()}")
                self.logger.info(f"{'='*60}")
                
                # Update documentation if needed
                success = self.update_documentation()
                
                if success:
                    self.logger.info("Monitoring cycle completed successfully")
                else:
                    self.logger.error("Monitoring cycle failed")
                
                # Wait for next cycle
                wait_time = self.config['monitor_interval_hours'] * 3600  # Convert to seconds
                self.logger.info(f"Waiting {self.config['monitor_interval_hours']} hour(s) until next cycle...")
                time.sleep(wait_time)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring loop interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in monitoring loop: {e}")
    
    def show_status(self):
        """Show current status of the documentation system."""
        self.logger.info("=" * 60)
        self.logger.info("DOCUMENTATION SYSTEM STATUS")
        self.logger.info("=" * 60)
        
        # Repository status
        self.logger.info(f"Repository: {self.repo.working_dir}")
        self.logger.info(f"Current branch: {self.repo.active_branch.name}")
        self.logger.info(f"Current commit: {self.repo.head.commit.hexsha[:8]}")
        
        # Last update status
        last_processed = self.get_last_processed_commit()
        if last_processed:
            self.logger.info(f"Last docs update: {last_processed[:8]}")
            if last_processed != self.repo.head.commit.hexsha:
                self.logger.info("⚠️  Documentation may be out of date")
            else:
                self.logger.info("✅ Documentation is up to date")
        else:
            self.logger.info("❌ No documentation updates recorded")
        
        # Configuration
        self.logger.info(f"Monitor interval: {self.config['monitor_interval_hours']} hour(s)")
        self.logger.info(f"Auto-commit: {'✅' if self.config['auto_commit'] else '❌'}")
        self.logger.info(f"Auto-push: {'✅' if self.config['auto_push'] else '❌'}")
        
        # Check for uncommitted changes
        if self.repo.is_dirty():
            self.logger.info("⚠️  Repository has uncommitted changes")
        else:
            self.logger.info("✅ Repository is clean")
        
        self.logger.info("=" * 60)

def main():
    """Main entry point for the Expert Document Writer Agent."""
    parser = argparse.ArgumentParser(description="Expert Document Writer Agent")
    parser.add_argument("--repo-path", default=".", help="Path to git repository")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Logging level")
    parser.add_argument("--once", action="store_true", help="Run once instead of continuous monitoring")
    parser.add_argument("--status", action="store_true", help="Show current status and exit")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ExpertDocWriter(args.repo_path, args.log_level)
    
    # Load custom configuration if provided
    if args.config:
        try:
            with open(args.config, 'r') as f:
                custom_config = json.load(f)
                agent.config.update(custom_config)
                agent.logger.info(f"Loaded custom configuration from {args.config}")
        except Exception as e:
            agent.logger.error(f"Failed to load custom configuration: {e}")
    
    # Show status if requested
    if args.status:
        agent.show_status()
        return
    
    # Run agent
    if args.once:
        agent.logger.info("Running documentation update once...")
        success = agent.update_documentation()
        sys.exit(0 if success else 1)
    else:
        agent.logger.info("Starting continuous monitoring...")
        agent.run_monitoring_loop()

if __name__ == "__main__":
    main()
