# Task: Find Player Deletion Endpoint on AdminWebAPI

**Ticket:** CT-752
**Context:** QA testing blocked - need to delete test player registered via Google

## Problem
- Registered a player via Google OAuth on QA
- This automatically created a linked social account
- Cannot test social linking scenarios with clean state
- Need to delete this test player to continue testing

## Goal
Find if AdminWebAPI has an endpoint to delete/remove players by:
1. Player ID
2. Client ID
3. Email

## Scope
- Check AdminWebAPI Swagger/OpenAPI docs
- Look for endpoints like:
  - `DELETE /api/players/{id}`
  - `DELETE /api/clients/{clientId}`
  - Any admin-level player management endpoints
  - Social account unlinking endpoints

## Environment
- Base URL: `https://qa-adminwebapi.minebit.com` (check exact URL)
- Need admin-level access

## Expected Output
1. List of relevant endpoints found
2. Required parameters (player ID, client ID, etc.)
3. Authentication requirements
4. Example curl request if endpoint exists

## Alternative Approaches
If no delete endpoint exists:
- Check for "unlink social account" endpoint
- Check for player status change (disable/suspend)
- Document that player cleanup requires DB access

## Context Files
- Test data scripts: `/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/test-data-scripts/`
- Project docs: Check for AdminWebAPI documentation
