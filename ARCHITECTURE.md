# Multi-Agent System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER APPLICATION                            │
│  (example_sequential.py, example_collaborative.py, etc.)            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ creates
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           AgentTeam                                 │
│                                                                     │
│  Responsibilities:                                                  │
│  - Manage multiple specialized agents                              │
│  - Coordinate workflows (Sequential, Collaborative, Hierarchical)  │
│  - Track conversation history                                      │
│  - Handle agent communication                                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ manages
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SpecializedAgent (x N)                         │
│                                                                     │
│  Each agent has:                                                    │
│  - Role (CEO, Developer, QA, etc.)                                 │
│  - Name (custom identifier)                                        │
│  - Expertise (list of skills)                                      │
│  - Ollama Model (can be different per agent)                       │
│  - Temperature (controls creativity)                               │
│  - Conversation History                                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ uses
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         ChatOllama                                  │
│                    (LangChain Integration)                          │
│                                                                     │
│  - Interfaces with Ollama                                          │
│  - Handles message formatting                                      │
│  - Manages model invocation                                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ calls
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Ollama Server                                 │
│                    (Running Locally)                                │
│                                                                     │
│  Models:                                                            │
│  - llama3.2                                                         │
│  - codellama (optional)                                            │
│  - mixtral (optional)                                              │
│  - phi (optional)                                                  │
│  - others...                                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. AgentTeam (`agent_team.py`)

**Purpose:** Orchestrates multiple agents working together

**Key Methods:**
- `sequential_workflow()` - Agents work in sequence
- `collaborative_workflow()` - Agents discuss together
- `hierarchical_workflow()` - Manager directs team
- `get_agent()` - Access individual agents
- `reset_all()` - Clear all conversation histories

**Example:**
```python
team = AgentTeam({
    "Alice": "ceo",
    "Bob": "backend_developer"
})
```

### 2. SpecializedAgent (`specialized_agent.py`)

**Purpose:** Individual agent with specific role and expertise

**Key Methods:**
- `step()` - Process a message and generate response
- `reset()` - Clear conversation history
- `update_messages()` - Add to conversation
- `get_context_summary()` - Get conversation stats

**Example:**
```python
agent = SpecializedAgent(
    role="Backend Developer",
    name="Bob",
    expertise=["Python", "FastAPI"],
    model_name="llama3.2",
    temperature=0.4
)
```

### 3. Model Configuration (`multi_model_config.py`)

**Purpose:** Manage which Ollama models are used by which roles

**Key Features:**
- Pre-configured model assignments
- Temperature settings per role
- Easy model switching
- Alternative model recommendations

## Workflow Patterns

### Sequential Workflow

```
Agent 1          Agent 2          Agent 3
   │                │                │
   ▼                │                │
Process Task        │                │
   │                │                │
   └─────Result────►│                │
                    ▼                │
                 Process Task        │
                    │                │
                    └─────Result────►│
                                     ▼
                                  Process Task
                                     │
                                     ▼
                                   DONE
```

**Use Case:** Linear tasks with dependencies (Design → Implement → Test)

### Collaborative Workflow

```
        Task
         │
    ┌────┼────┬────┐
    ▼    ▼    ▼    ▼
  Agent1 Agent2 Agent3 Agent4
    │    │    │    │
    └────┼────┴────┘
         │
    All Discuss
         │
    ┌────┼────┬────┐
    ▼    ▼    ▼    ▼
  Agent1 Agent2 Agent3 Agent4
    │    │    │    │
    └────┼────┴────┘
         │
    Reach Consensus
```

**Use Case:** Need multiple perspectives (Architecture decisions, Design reviews)

### Hierarchical Workflow

```
        Manager
           │
      Plans Task
           │
    ┌──────┼──────┬──────┐
    ▼      ▼      ▼      ▼
 Team1  Team2  Team3  Team4
    │      │      │      │
 Execute Execute Execute Execute
    │      │      │      │
    └──────┼──────┴──────┘
           │
      Manager Reviews
           │
     Next Iteration?
```

**Use Case:** Complex projects needing coordination (Product development)

## Data Flow

### Message Flow in Sequential Workflow

```
1. User defines task
2. AgentTeam creates HumanMessage(task)
3. Agent1.step(message)
   ├─> Updates conversation history
   ├─> Invokes ChatOllama
   │   └─> Calls Ollama server
   └─> Returns AIMessage
4. AgentTeam formats response as context for Agent2
5. Agent2.step(context + response)
   └─> Repeat step 3 process
6. Continue until all agents complete
7. Return results to user
```

### Conversation History Structure

```python
agent.stored_messages = [
    SystemMessage(content="You are a Backend Developer..."),  # Role definition
    HumanMessage(content="Build an API..."),                  # Task
    AIMessage(content="Here's the implementation..."),        # Agent response
    HumanMessage(content="Review this code..."),             # Next task
    AIMessage(content="Code looks good but..."),             # Agent response
    # ... continues
]
```

## Model Assignment Strategy

```
Role Type          Temperature    Model Choice      Reasoning
─────────────────────────────────────────────────────────────────
Strategic          0.6-0.8        llama3.2         Needs creativity
(CEO, PM)                         or mixtral       for planning

Technical          0.3-0.5        codellama        Needs precision
(Developers)                      or llama3.2      for code

Creative           0.7-0.9        llama3.2         Needs imagination
(Designer)                        or neural-chat   for design

Analytical         0.3-0.5        llama3.2         Needs accuracy
(QA, Security)                    or mixtral       for analysis
```

## File Organization

```
python_AGI/
│
├── Core Agent System
│   ├── specialized_agent.py      # Individual agent implementation
│   ├── agent_team.py              # Team coordination
│   └── multi_model_config.py     # Model assignments
│
├── Original CAMEL System
│   ├── camel.py                   # Main CAMEL implementation
│   ├── camelagent.py              # CAMEL agent class
│   ├── utils.py                   # Helper functions
│   ├── user_prompt.py             # User agent prompt
│   └── assistant_prompt.py        # Assistant agent prompt
│
├── Examples
│   ├── quick_start_multi_agent.py     # Quick start
│   ├── example_sequential.py          # Sequential workflow
│   ├── example_collaborative.py       # Collaborative workflow
│   ├── example_hierarchical.py        # Hierarchical workflow
│   └── example_custom_workflow.py     # Custom workflows
│
├── Documentation
│   ├── README.md                  # Main documentation
│   ├── MULTI_AGENT_GUIDE.md      # Detailed guide
│   └── ARCHITECTURE.md            # This file
│
└── Configuration
    ├── requirements.txt           # Python dependencies
    ├── example.env                # Environment template
    └── .gitignore                 # Git ignore rules
```

## Extension Points

### Adding New Agent Roles

1. Update `AGENT_CONFIGS` in `specialized_agent.py`:
```python
AGENT_CONFIGS["data_scientist"] = {
    "role": "Data Scientist",
    "expertise": ["ML", "Statistics", "Python"],
    "model": "llama3.2",
    "temperature": 0.5
}
```

2. Add role responsibilities in `_get_role_responsibilities()` method

### Adding New Workflows

Create a new method in `AgentTeam`:
```python
def custom_workflow(self, task, **kwargs):
    # Your custom logic here
    # Mix sequential, collaborative, and hierarchical patterns
    pass
```

### Using Different Models

```python
# Option 1: Update global config
from multi_model_config import update_model_assignment
update_model_assignment("backend_developer", "codellama")

# Option 2: Create agent with specific model
agent = SpecializedAgent(
    role="Developer",
    name="Bob",
    expertise=["Python"],
    model_name="codellama",  # Specific model
    temperature=0.3
)
```

## Performance Considerations

### Memory Management
- Each agent stores full conversation history
- For long workflows, consider implementing message pruning
- Reset agents between unrelated tasks

### Concurrency
- Current implementation is synchronous
- For independent agents, use `ThreadPoolExecutor` for parallel execution
- Be mindful of Ollama's concurrent request limits

### Model Selection
- Larger models (mixtral) → Better quality, slower
- Smaller models (phi) → Faster, good for simple tasks
- Specialized models (codellama) → Best for specific domains

## Security Considerations

- All processing happens locally via Ollama
- No API keys required
- No data sent to external services
- Conversation history stored in memory only
- Clear sensitive data with `agent.reset()`

## Future Enhancements

Potential additions:
1. **Persistent storage** - Save conversation histories
2. **Web interface** - GUI for managing agents
3. **Agent learning** - Agents improve from feedback
4. **Tool integration** - Agents can use external tools (search, databases)
5. **Async workflows** - Non-blocking agent operations
6. **Agent marketplace** - Share and download agent configurations
