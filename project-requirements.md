i have a code test i need to work on 


AI‑Powered Recipe Chatbot Assessment (Backend + Next.js Frontend)
Role: AI / Applied AI Engineer (Full‑Stack)
Timebox: 3 hours. It’s fine to leave pieces unfinished—show solid architecture, reasoning, and trade‑offs—we want to understand your prioritization as well as technical capabilities.
Overview
You are tasked with building an LLM-powered cooking & recipe Q&A application. The core of the system still centers on the AI-Powered Recipe Chatbot (LLM + LangGraph + LangChain), but the assessment also requires a Next.js frontend to demonstrate full‑stack capability and monorepo best practices.
Key backend constraint: Do not use model-specific SDKs directly; route all LLM calls through LangChain.
Your solution should:
Decide when and how to research (web search or other tools).
Classify queries as in-scope or out-of-scope.
Validate whether the user can actually cook a suggested dish with the available cookware list.
Expose a minimal FastAPI API.
Provide a simple chat UI in Next.js that talks to your backend.
Be structured as a monorepo, with clear documentation and Docker support.
Ensure that once you start, you push an initial commit to the repository. We will use the timestamp of that commit to check the amount of time you spent
High-Level Functional Requirements (Backend)
Queries to Handle
General cooking questions.
Recipe requests for specific dishes.
"What can I cook with these ingredients?" queries.
Query Relevance Classification
Decide if a query is relevant to cooking/recipes.
Refuse irrelevant queries briefly and politely.
LLM-Driven Research & Tool Usage
Let the LLM decide when to invoke tools (e.g., web search).
Implement at least one external info tool (SERP, Requests wrapper, etc.).
"Can the user cook this?" Check
Use this hardcoded cookware list (assume it’s what the user has):
[
  "Spatula",
  "Frying Pan",
  "Little Pot",
  "Stovetop",
  "Whisk",
  "Knife",
  "Ladle",
  "Spoon"
]
Verify required tools for any suggested recipe and respond accordingly.
LangGraph Flow
Implement a node-based or agent-based flow using LangGraph (with or without extra LangChain abstractions).
Include deterministic and conditional transitions where appropriate.
Result Output
For cooking queries: return a detailed response (steps, tips, references).
For non-cooking queries: brief refusal message.
FastAPI Endpoint(s)
Provide at least one endpoint (e.g.,  or ).
Accepts a user message; returns JSON with either a refusal or a full answer.
Ensure that the response streams back to the frontend. You can use any extra libraries (such as AG-UI, CopilotKit) to handle this as needed.
Logging & Debugging
Add logging around tool calls and node transitions.
Provide a simple way to view the reasoning chain/plan (e.g., include in response under a debug flag or log it).
Interaction Examples
Include example curl requests in the README.
Document Unhandled Edge Cases
List edge cases or failure modes you noticed but didn’t resolve; add notes on future fixes.
Frontend Requirements (Next.js + TypeScript)
Framework & Stack
Use Next.js (15+ / App Router) with TypeScript.
Style with Tailwind CSS and use shadcn/ui for common components (buttons, inputs, cards/chat bubbles).
UI / UX
Build a minimal chat interface:
Text input box for the user message.
Scrollable conversation history showing both user and assistant messages.
Basic loading indicator and error state handling.
Optional but nice: message "types" (e.g., recipe with steps rendered nicely), copy-to-clipboard buttons, or streaming responses.
API Integration
Call your FastAPI backend endpoint(s) to send user messages.
If you use LangGraph’s JS SDK () or AG-UI/Copilotkit for orchestration, document how you wired it up.
Best Practices
Logical file organization (components, hooks, lib/api clients, etc.).
Strong typing for request/response schemas (consider  or generated types from OpenAPI).
No need for global state libraries unless you want to; React hooks/state is fine for the 3‑hour limit.
Dev Experience
Support  (or ) for local dev.
Frontend should run in Docker as part of .
Project & Code Requirements
1. Monorepo Structure
Organize a single repo like:
.
├── backend/
│   ├── main.py                   # FastAPI entry point
│   ├── graphs/                   # LangGraph graphs / nodes
│   ├── tools/                    # Tool definitions (SERP, cookware checker, etc.)
│   ├── models/ or schemas/       # Pydantic models for requests/responses
│   ├── Dockerfile
│   └── ...
├── frontend/
│   ├── app/                      # Next.js routes
│   ├── components/               # UI components (chat bubbles, input)
│   ├── lib/                      # API helpers / types
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
├── README.md                     # Root README covering both apps
└── .editorconfig / .prettierrc / etc.
2. Containerization & Env
Provide Dockerfiles for both backend and frontend.
 (optional but encouraged) to run everything with one command.
Document environment variables (e.g., , LLM keys) in the README. Use .
3. Code Quality
Python: Follow PEP 8, use Ruff formatter.
TypeScript: strict mode on. Clean, modular code.
Comments/docstrings where useful.
4. Deployment (AWS) — Documentation Only
In the README, describe how you would deploy:
Compute choice (ECS/EKS/Lambda/EC2) and why.
Secret management (SSM Parameter Store, Secrets Manager).
Observability (CloudWatch, OpenTelemetry, structured logs).
Scaling & networking (ALB, autoscaling, VPC, etc.).
5. Auth & Security — Documentation Only
Describe how you would secure the endpoints:
API keys, JWT, OAuth2, or a reverse proxy with auth.
CORS, rate limiting, input validation, prompt injection mitigation.
Safeguarding LLM and SERP keys.
6. ELT Integration — Documentation Only
Describe how you would setup an ELT system to intake the recipes that users are deciding on making with their tools to convert it to metrics and statistics so that the stakeholders know what people are cooking.
Deliverables
GitHub Repo with the full monorepo.
Backend: FastAPI app, LangGraph flow, tools.
Frontend: Next.js chat UI calling the backend.
Dockerfile(s) and (optionally) docker-compose.yml.
README.md containing:
Local setup (dev & Docker).
Usage examples (curl, screenshots/GIFs of UI are great).
AWS deployment plan.
Auth & security plan.
Design decisions & AI tooling used.
Timeboxing notes / trade-offs & next steps.
Edge Case Notes in README (or separate doc) for unhandled scenarios and proposed fixes.
Evaluation Criteria
Correctness & Features
Does the system classify queries and refuse irrelevant ones?
Does the LLM control tool usage via LangGraph, not hard-coded sequences?
Are recipes validated against available cookware?
Frontend Functionality & UX
Does the chat interface work end-to-end?
Is the UI reasonably clean and responsive?
Architecture & Code Quality
Clear monorepo organization.
Modular, readable Python & TypeScript.
Sensible LangGraph design (state, nodes, branching).
Documentation
Can we run it on our machines quickly?
Are deployment/auth plans coherent?
Are design choices and trade-offs explained?
Time Management & Senior Thinking
Smart prioritization under 3 hours.
Clear notes on what’s missing and why.
Optional Nice-to-Haves (Bonus Points)
Streaming responses (SSE/Fetch streaming) to the frontend.
Unit tests for key graph nodes/tools.
OpenAPI schema export and generated TS types for the frontend.
CI pipeline (lint/test/build) in GitHub Actions.
Prompt/template versioning and evaluation notes.
Edge Cases & Future Work (Examples)
Include a brief list like:
Multi-step recipes requiring unavailable cookware (suggest substitutions?).
Ambiguous ingredient names (“tomato sauce” vs “strained tomatoes”).
Non-English queries or metric/imperial conversions.
Long conversations and context window limits (strategies: memory pruning, vector store, summaries).
Tool failures (SERP outages, rate limits) and retries/circuit breakers.
Submission Tips
Start by scaffolding the monorepo and Docker.
Implement the LangGraph backbone early, then basic tools.
Get one E2E path working (query → backend → LLM/tool → answer → frontend) before polishing.
Document unfinished parts clearly—this is part of the assessment.
Your submission will either need to be a public GitHub repository or shared with @elmdecoste and @bgreal5 on GitHub
Good luck! We’re excited to see your approach.

