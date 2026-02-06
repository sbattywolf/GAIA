#!/bin/bash
# GAIA Quick Start Script
# Automated setup for local development with GitHub Copilot

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  GAIA Quick Start Setup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version || { echo "Python 3 not found. Please install Python 3.10+"; exit 1; }

# Run automated setup
echo -e "\n${BLUE}Running automated setup...${NC}"
python3 scripts/setup_dev_env.py

# Check result
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Setup completed successfully!${NC}"
else
    echo -e "\n${YELLOW}⚠ Setup completed with warnings. Review output above.${NC}"
fi

# Provide next steps
echo -e "\n${BLUE}================================${NC}"
echo -e "${BLUE}  Next Steps${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "1. Activate virtual environment:"
echo -e "   ${GREEN}source .venv/bin/activate${NC}"
echo ""
echo "2. Load project context:"
echo -e "   ${GREEN}python scripts/load_context.py${NC}"
echo ""
echo "3. Start coding with Copilot:"
echo -e "   ${GREEN}See: doc/01_onboarding/copilot-local-setup.md${NC}"
echo ""
