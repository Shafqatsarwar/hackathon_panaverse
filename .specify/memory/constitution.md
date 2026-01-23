# Panversity Student Assistant Constitution

## Core Principles

### I. Skills-First Architecture
**Every capability starts as a reusable skill**
- Skills are self-contained, independently testable modules
- Each skill has a single, well-defined responsibility
- Skills must include `SKILL.md` documentation with usage examples
- Skills have no dependencies on agents or tasks
- Skills expose clear interfaces for agent consumption

**Current Skills:**
- `gmail_monitoring`: Gmail API integration for inbox monitoring
- `email_filtering`: Email categorization, keyword matching, priority detection
- `email_notifications`: SMTP-based email notification delivery

### II. Agent Autonomy & Orchestration
**Agents compose skills to perform autonomous actions**
- Agents use one or more skills to accomplish specific goals
- Each agent maintains its own state and provides status reporting
- Agents handle errors gracefully with retry logic and fallback mechanisms
- Agents must implement `get_status()` for observability
- Agents are coordinated by higher-level orchestrator agents

**Current Agents:**
- `EmailAgent`: Monitors Gmail using gmail_monitoring + email_filtering skills
- `NotificationAgent`: Sends alerts using email_notifications skill
- `MainAgent`: Orchestrates EmailAgent + NotificationAgent for complete workflows
- `ChatAgent`: Conversational AI using Google Gemini for user interactions

### III. Chatbot Assistant (User Interface)
**A helpful chatbot interface for all autonomous tasks**
- ChatAgent provides natural language interface to all system capabilities
- Users can query email status, task progress, and system information via chat
- Chatbot uses Google Gemini AI for intelligent, context-aware responses
- Web search integration for answering questions beyond training data
- Real-time streaming responses for better user experience
- Chat history maintained for context and auditability

**Chatbot Capabilities:**
- **Email Management**: "Check my emails", "Any important messages?", "Show quiz deadlines"
- **Task Assistance**: "What tasks are running?", "When is the next email check?"
- **Information Queries**: "What is Panversity?", "Search for Python tutorials"
- **System Status**: "Show agent status", "Is email monitoring active?"
- **Skill Integration**: Access to all skills through conversational interface

**Technical Implementation:**
- Google AI SDK (@google/generative-ai) for Gemini integration
- Next.js 15 + React frontend for modern UI/UX
- WebSocket/streaming for real-time responses
- DuckDuckGo integration for web search
- Glassmorphism design for premium user experience

### IV. Task-Driven Execution
**Tasks define what needs to be done and coordinate agents**
- Tasks are declarative JSON definitions in `tasks/` directory
- Each task specifies: name, agents, skills_required, schedule, success_criteria
- Tasks define clear success criteria and error handling policies
- Tasks can be scheduled (cron-like) or triggered on-demand
- Task execution is logged to chat history for auditability

**Task Definition Standard:**
```json
{
  "name": "task_name",
  "description": "Clear description of task purpose",
  "agents": ["Agent1", "Agent2"],
  "skills_required": ["skill1", "skill2"],
  "schedule": "every N minutes | on_demand",
  "success_criteria": { "key": "expected_value" },
  "error_handling": { "retry_on_failure": true, "max_retries": 3 }
}
```

### V. Observability & Audit Trail (NON-NEGOTIABLE)
**Complete chat history logging is mandatory**
- All agent activities are logged to `chat_history/` as daily JSON files
- Log format: `chat_history/YYYY-MM-DD.json`
- Each log entry includes: timestamp, task, agent, action, status, data
- Logs enable debugging, analytics, and compliance auditing
- Chat history is queryable and machine-readable

**Log Entry Standard:**
```json
{
  "timestamp": "ISO-8601 format",
  "task": "task_name",
  "agent": "agent_name",
  "action": "action_performed",
  "status": "success | failure | in_progress",
  "data": { "relevant": "context" }
}
```

### VI. MCP Server Integration
**Model Context Protocol servers extend agent capabilities**
- MCP servers provide standardized interfaces for external services
- Each MCP server exposes tools, resources, and prompts
- MCP servers are located in `src/mcp_servers/`
- Agents can leverage MCP tools for enhanced functionality
- MCP servers follow the official MCP specification

**Current MCP Servers:**
- `gmail_server.py`: Gmail API operations (read, search, send)
- `github_server.py`: GitHub repository and issue management
- `playwright_server.py`: Web automation and browser interactions

### VII. Modularity & Reusability
**Design for composition and extension**
- Skills can be used by multiple agents
- Agents can be composed into higher-level workflows
- Tasks can be combined and scheduled independently
- Clear separation of concerns: Skills → Agents → Tasks → Chat History
- New capabilities added through new skills/agents, not modifications

### VIII. Configuration-Driven Behavior
**Environment-based configuration without code changes**
- All credentials and secrets in `.env` (never committed)
- Configuration loaded via `src/utils/config.py`
- Feature flags for enabling/disabling capabilities (WHATSAPP_ENABLED, LINKEDIN_ENABLED)
- Configurable intervals, keywords, and thresholds
- Validation of required configuration on startup

## Architecture Standards

### Skills Layer Standards
**Location:** `skills/skill_name/`

**Required Files:**
- `SKILL.md`: Documentation with purpose, usage, examples
- `skill_name.py`: Implementation with clear public interface

**Implementation Requirements:**
- Single responsibility principle
- No dependencies on agents or tasks
- Independent testability
- Error handling with descriptive exceptions
- Type hints for all public methods

**Documentation Requirements:**
- Purpose and use cases
- Installation/setup instructions
- Code examples
- API reference
- Known limitations

### Agents Layer Standards
**Location:** `src/agents/agent_name.py`

**Required Methods:**
- `__init__()`: Initialize with required skills/dependencies
- `get_status()`: Return current agent status and metrics
- Core action methods specific to agent purpose

**Implementation Requirements:**
- Import and compose skills (never duplicate skill logic)
- Maintain internal state as needed
- Implement graceful error handling
- Log all significant actions
- Provide status reporting for observability

**Error Handling:**
- Catch and log all exceptions
- Retry transient failures (network, API rate limits)
- Fail gracefully with informative error messages
- Report errors to MainAgent for coordination

### Tasks Layer Standards
**Location:** `tasks/task_name.json`

**Required Fields:**
- `name`: Unique task identifier
- `description`: Human-readable purpose
- `agents`: Array of agent names required
- `skills_required`: Array of skill names required
- `schedule`: Execution schedule or "on_demand"
- `success_criteria`: Object defining success conditions
- `error_handling`: Retry and logging policies

**Execution Requirements:**
- Tasks executed by MainAgent
- All task runs logged to chat_history
- Success/failure status recorded
- Errors trigger retry logic per task definition

### Chat History Standards
**Location:** `chat_history/YYYY-MM-DD.json`

**Format:** JSON array of log entries

**Required Fields per Entry:**
- `timestamp`: ISO-8601 formatted datetime
- `task`: Task name or "manual" for ad-hoc actions
- `agent`: Agent that performed the action (optional)
- `action`: Description of action taken
- `status`: "success", "failure", "in_progress"
- `data`: Object with relevant context/results

**Retention Policy:**
- Daily files for easy querying and archival
- Retain indefinitely for audit trail
- Files are append-only during the day

### MCP Server Standards
**Location:** `src/mcp_servers/server_name.py`

**Implementation Requirements:**
- Follow official MCP specification
- Expose tools, resources, and/or prompts
- Handle authentication and credentials securely
- Implement error handling and retries
- Provide clear tool descriptions for AI agents

**Integration Requirements:**
- Agents can import and use MCP server tools
- MCP servers are stateless where possible
- Configuration via environment variables
- Logging of all MCP tool invocations

## Development Workflow

### Adding a New Skill
1. Create `skills/skill_name/` directory
2. Write `SKILL.md` documentation (purpose, usage, examples)
3. Implement `skill_name.py` with clear interface
4. Test skill independently
5. Update `skills/README.md` with skill description
6. Submit for review with test results

### Adding a New Agent
1. Create `src/agents/agent_name.py`
2. Import required skills (never duplicate skill logic)
3. Implement `__init__()` and `get_status()` methods
4. Implement core agent action methods
5. Add error handling and logging
6. Update `MainAgent` to coordinate new agent if needed
7. Test agent with real skills
8. Document agent in `ARCHITECTURE.md`

### Adding a New Task
1. Create `tasks/task_name.json` with complete definition
2. Ensure all required agents and skills exist
3. Define clear success criteria
4. Configure error handling and retry logic
5. Add task execution method to `MainAgent` if needed
6. Test task execution end-to-end
7. Verify chat_history logging
8. Update `tasks/README.md`

### Adding a New MCP Server
1. Create `src/mcp_servers/server_name.py`
2. Implement MCP specification (tools/resources/prompts)
3. Add authentication and configuration
4. Document available tools and usage
5. Test MCP server independently
6. Integrate with relevant agents
7. Update documentation

## Quality Gates

### Documentation Requirements
- **Skills**: Must have `SKILL.md` with examples
- **Agents**: Must be documented in `ARCHITECTURE.md`
- **Tasks**: Must have clear description in JSON
- **MCP Servers**: Must document available tools
- **Code**: Docstrings for all public methods

### Testing Requirements
- **Skills**: Independently testable with unit tests
- **Agents**: Integration tests with real skills
- **Tasks**: End-to-end tests with chat_history verification
- **MCP Servers**: Tool invocation tests

### Code Quality Requirements
- Type hints for all public methods
- Error handling for all external calls (API, file I/O, network)
- Logging for all significant actions
- No hardcoded credentials or secrets
- Configuration via environment variables

### Observability Requirements
- All agent actions logged to chat_history
- Status reporting via `get_status()` methods
- Error logging with stack traces
- Performance metrics where relevant

## Technology Stack

### Core Technologies
- **Language**: Python 3.8+
- **Architecture**: Skills → Agents → Tasks
- **Logging**: JSON-based chat_history
- **Configuration**: python-dotenv
- **MCP**: Model Context Protocol servers

### External Integrations
- **Gmail API**: Email monitoring via gmail_monitoring skill
- **SMTP**: Email notifications via email_notifications skill
- **GitHub API**: Repository management via github_server MCP
- **Playwright**: Web automation via playwright_server MCP

### Future Integrations (Feature Flags)
- **WhatsApp**: Enabled via `WHATSAPP_ENABLED=true`
- **LinkedIn**: Enabled via `LINKEDIN_ENABLED=true`

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- All code reviews must verify compliance with constitution
- Violations must be justified and documented
- Constitution is the source of truth for architecture decisions

### Amendment Process
1. Propose amendment with rationale
2. Document impact on existing code
3. Obtain approval from project maintainers
4. Update constitution with version increment
5. Create migration plan for existing code
6. Update `Last Amended` date

### Compliance Verification
- All pull requests reviewed for constitution compliance
- Skills must have `SKILL.md` documentation
- Agents must implement `get_status()`
- Tasks must log to chat_history
- No hardcoded credentials allowed
- Configuration must be environment-based

### Complexity Justification
- Simple solutions preferred (YAGNI principle)
- Complexity must be justified in code comments
- Premature optimization avoided
- Refactoring preferred over rewriting

### Runtime Guidance
- Use `ARCHITECTURE.md` for development guidance
- Follow existing patterns in codebase
- Consult `skills/README.md` for skill guidelines
- Reference task definitions in `tasks/` for examples

**Version**: 1.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23
