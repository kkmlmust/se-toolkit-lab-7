# Bot Development Plan

## Overview
This bot provides LMS data access through Telegram with natural language interface. Users can check scores, view lab statistics, and ask questions in natural language.

## Architecture
- **Handlers**: Separate from Telegram transport for testability
- **Services**: API client for LMS backend, LLM client for intent routing
- **Config**: Pydantic settings with .env file support
- **Entry Point**: Single bot.py with --test flag

## Task 1: Scaffolding (Current)
Create project structure with test mode support:
- bot/pyproject.toml with dependencies
- bot/bot.py with --test flag
- bot/handlers/ with placeholder commands
- bot/config.py for configuration

## Task 2: Backend Integration
Implement real API calls:
- Fetch labs, items, scores from LMS API
- Handle async requests properly
- Add error handling and timeouts
- Implement data formatting for Telegram messages

## Task 3: LLM Intent Routing
Add natural language understanding:
- Route user questions to appropriate handlers
- Use Qwen API to interpret queries
- Fallback to command parsing
- Handle edge cases and unknown intents

## Task 4: Deployment
Deploy bot on VM:
- Run as background process
- Monitor logs
- Ensure auto-recovery on failures

## Testing Strategy
- --test mode for offline verification
- Manual testing in Telegram
- Autochecker will validate deployment

## Timeline
- Task 1: 2 hours
- Task 2: 3 hours
- Task 3: 4 hours
- Task 4: 1 hour
