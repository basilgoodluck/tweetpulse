#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python -m venv venv
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

echo -e "${GREEN}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo -e "${GREEN}Installing dependencies from requirements.txt...${NC}"
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo -e "${RED}No .env file found!${NC}"
    echo -e "${GREEN}Copying .env.example to .env...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env with your DISCORD_WEBHOOK_URL and TWITTER_NAMES.${NC}"
    exit 1
fi

echo -e "${GREEN}Starting the scheduler (runs every 10 minutes)...${NC}"
python src/scheduler.py
