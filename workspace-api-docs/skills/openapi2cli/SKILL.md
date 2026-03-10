---
name: openapi2cli
description: Generate strict, executable CLI tools from OpenAPI specifications. Built for API agents to bypass manual curl writing.
version: 1.0.0
---

# OpenAPI to CLI Generator Skill

This skill allows you to instantly generate a strongly-typed CLI client from any Swagger or OpenAPI specification. You should use this whenever you need to interact with a complex REST API directly (like `AdminWebApi` or `Wallet Service`) to avoid making typos in `curl` commands.

## Requirements
- `npx` (Node Package Runner) installed on the system.
- Access to an OpenAPI/Swagger URL.

## How it works

Behind the scenes, this skill leverages the official OpenAPI Generator CLI (`@openapitools/openapi-generator-cli`), but is streamlined for agent use. 

### Step 1: Generate the CLI tool

When you need to interact with an API whose Swagger is at `$SWAGGER_URL`, first generate the CLI client in a temporary or local directory (e.g., your `scripts/` folder):

```bash
npx @openapitools/openapi-generator-cli generate \
  -i <SWAGGER_URL_OR_FILE> \
  -g bash \
  -o ./generated-api-cli
```
*Note: We use the `bash` generator, which outputs a ready-to-use Bash script wrapper around curl with strict parameter flags based on the OpenAPI Spec.*

### Step 2: Make it executable

Navigate to the generated folder and ensure the main script is executable:

```bash
cd ./generated-api-cli
chmod +x ./<APP_NAME>
```

### Step 3: Use the CLI

Now, instead of manually writing curl requests, you can use the generated CLI! 

First, get the help documentation to see available endpoints and parameters:
```bash
./<APP_NAME> --help
```

Then, run a specific command (example):
```bash
./<APP_NAME> addBonus \
  --client-id 59107 \
  --amount 100 \
  --header "Authorization: Bearer <TOKEN>"
```

## When to use this skill
- **Complex Payloads:** When a POST/PUT request has a massive JSON schema, and you don't want to risk formatting errors.
- **Exploratory Testing:** When Nexus asks you to quickly verify if an endpoint is alive or modify a balance, use the generated CLI for immediate feedback.
- **Regression Checks:** If you need to repeatedly call an endpoint, the CLI acts as a solid alias.

## Limitations & Best Practices
- **GraphQL APIs:** This tool works **only** for REST (OpenAPI/Swagger). Do NOT use this for the Website Web API if it's strictly GraphQL. 
- Try to cache the generated CLI in your `scripts/` folder so you don't have to regenerate it for every request.
