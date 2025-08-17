#!/bin/bash
# Expert Document Writer Agent Launcher
# =====================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Expert Document Writer Agent Launcher${NC}"
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Install dependencies if needed
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
if ! python3 -c "import git" 2>/dev/null; then
    echo -e "${YELLOW}Installing required dependencies...${NC}"
    pip3 install -r requirements-agent.txt
fi

# Function to show usage
show_usage() {
    echo ""
    echo -e "${BLUE}Usage Options:${NC}"
    echo "  ${GREEN}./launch-docs-agent.sh status${NC}     - Show current status"
    echo "  ${GREEN}./launch-docs-agent.sh once${NC}       - Run documentation update once"
    echo "  ${GREEN}./launch-docs-agent.sh monitor${NC}    - Start continuous monitoring"
    echo "  ${GREEN}./launch-docs-agent.sh help${NC}       - Show this help message"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  ${GREEN}./launch-docs-agent.sh status${NC}     # Check if docs are up to date"
    echo "  ${GREEN}./launch-docs-agent.sh once${NC}       # Update docs now if needed"
    echo "  ${GREEN}./launch-docs-agent.sh monitor${NC}    # Start hourly monitoring"
    echo ""
}

# Function to run the agent
run_agent() {
    local mode="$1"
    echo -e "${GREEN}✅ Starting Expert Document Writer Agent in ${mode} mode...${NC}"
    echo ""
    
    case "$mode" in
        "status")
            python3 expert-doc-writer.py --status
            ;;
        "once")
            python3 expert-doc-writer.py --once
            ;;
        "monitor")
            echo -e "${YELLOW}🔄 Starting continuous monitoring (press Ctrl+C to stop)...${NC}"
            echo ""
            python3 expert-doc-writer.py
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

# Main logic
case "${1:-help}" in
    "status"|"once"|"monitor")
        run_agent "$1"
        ;;
    "help"|*)
        show_usage
        ;;
esac
