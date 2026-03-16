# Task: Find Player Deletion Endpoint on AdminWebAPI

## Context
Testing CT-752 (Social Account Linking) requires clean test data. A player created via Google registration is blocking further testing because the same Google account cannot be linked to another player.

## Objective
Find if there's an endpoint on AdminWebAPI to delete a player or unlink a social account from a player.

## Player to Delete/Clean
- Email: `pandasen@echoprx.cc`
- Player ID: `3563473`
- Linked via: Google registration

## What to Check
1. Check AdminWebAPI Swagger/OpenAPI documentation for:
   - Player deletion endpoints (DELETE /players/{id} or similar)
   - Social account unlinking endpoints
   - Any admin endpoints for player management

2. Check available endpoints in:
   - `https://minebit-casino.qa.sofon.one/adminwebapi/swagger` (or similar)
   - Existing API documentation

3. If found, provide:
   - Endpoint URL
   - Required parameters
   - Example request
   - Required authentication/headers

## Environment
- QA environment: `minebit-casino.qa.sofon.one`

## Output
Report findings in this file with:
- Available endpoints for player management
- Whether deletion is possible
- Example curl command if available
