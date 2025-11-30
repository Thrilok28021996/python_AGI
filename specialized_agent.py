"""
Specialized Agent System
Creates different types of agents with specific roles and capabilities
Each agent can use different Ollama models
"""

from typing import List, Optional
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


class SpecializedAgent:
    """
    A specialized agent with a specific role in the company

    Attributes:
        role: The agent's role (e.g., "CEO", "Developer", "Tester")
        name: The agent's name
        system_message: The system message defining agent behavior
        model: The ChatOllama model instance
        expertise: List of areas this agent specializes in
        stored_messages: Conversation history
    """

    def __init__(
        self,
        role: str,
        name: str,
        expertise: List[str],
        model_name: str = "llama3.2",
        temperature: float = 0.7,
    ) -> None:
        self.role = role
        self.name = name
        self.expertise = expertise
        self.model_name = model_name

        # Create system message based on role
        self.system_message = self._create_system_message()

        # Initialize the model
        self.model = ChatOllama(
            model=model_name,
            temperature=temperature
        )

        self.init_messages()

    def _create_system_message(self) -> SystemMessage:
        """Create a system message based on the agent's role"""

        expertise_str = ", ".join(self.expertise)

        content = f"""You are {self.name}, a {self.role} in a software development company.

Your expertise includes: {expertise_str}

Your responsibilities as {self.role}:
{self._get_role_responsibilities()}

Communication style:
- Be professional and focused
- Provide specific, actionable feedback
- Use your expertise to guide decisions
- Collaborate effectively with other team members
- Always structure your responses clearly

When responding, use this format:

Role: {self.role}
Response:
[Your main response]

Analysis:
[Your analysis of the situation]

Recommendation:
[Your specific recommendations or next steps]

Questions/Concerns:
[Any questions or concerns you have]
"""
        return SystemMessage(content=content)

    def _get_role_responsibilities(self) -> str:
        """Get specific responsibilities based on role"""

        responsibilities = {
            "CEO": """- Define project vision and goals
- Make high-level decisions
- Approve major changes
- Ensure project stays on track
- Resolve conflicts between team members""",

            "Product Manager": """- Define product requirements
- Prioritize features
- Create user stories
- Ensure product meets user needs
- Coordinate between technical and business teams""",

            "Lead Developer": """- Design system architecture
- Write high-quality code
- Review code from other developers
- Make technical decisions
- Ensure code quality and best practices""",

            "Backend Developer": """- Implement server-side logic
- Design and manage databases
- Create APIs
- Ensure backend performance and security
- Write backend tests""",

            "Frontend Developer": """- Implement user interfaces
- Ensure responsive design
- Optimize frontend performance
- Integrate with backend APIs
- Write frontend tests""",

            "QA Tester": """- Write test cases
- Perform manual and automated testing
- Find and report bugs
- Verify bug fixes
- Ensure product quality""",

            "DevOps Engineer": """- Set up CI/CD pipelines
- Manage infrastructure
- Ensure deployment processes
- Monitor system performance
- Handle security and scalability""",

            "UI/UX Designer": """- Design user interfaces
- Create wireframes and mockups
- Ensure good user experience
- Design system components
- Provide design feedback""",

            "Security Expert": """- Identify security vulnerabilities
- Implement security best practices
- Review code for security issues
- Ensure data protection
- Conduct security audits""",

            "Technical Writer": """- Write documentation
- Create API documentation
- Write user guides
- Ensure documentation clarity
- Keep documentation up-to-date"""
        }

        return responsibilities.get(self.role, "- Perform assigned tasks\n- Collaborate with team")

    def reset(self) -> None:
        """Reset agent conversation history"""
        self.init_messages()

    def init_messages(self) -> None:
        """Initialize message history with system message"""
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        """Add a message to conversation history"""
        self.stored_messages.append(message)
        return self.stored_messages

    def step(self, input_message: HumanMessage) -> AIMessage:
        """
        Process an input message and generate a response

        Args:
            input_message: The input message from another agent or user

        Returns:
            The agent's response as an AIMessage
        """
        messages = self.update_messages(input_message)

        try:
            output_message = self.model.invoke(messages)
        except Exception as e:
            raise RuntimeError(f"LLM invocation failed for {self.name}: {str(e)}") from e

        self.update_messages(output_message)

        return output_message

    def get_context_summary(self) -> str:
        """Get a summary of the agent's conversation context"""
        return f"{self.name} ({self.role}): {len(self.stored_messages)} messages in history"


# Predefined agent configurations
# OPTIMIZED FOR YOUR DOWNLOADED OLLAMA MODELS
AGENT_CONFIGS = {
    "ceo": {
        "role": "CEO",
        "expertise": ["Strategic Planning", "Decision Making", "Leadership"],
        "model": "mistral:latest",  # Best for strategic thinking
        "temperature": 0.7
    },
    "product_manager": {
        "role": "Product Manager",
        "expertise": ["Product Strategy", "Requirements Gathering", "User Stories"],
        "model": "mistral:latest",  # Good reasoning for planning
        "temperature": 0.7
    },
    "lead_developer": {
        "role": "Lead Developer",
        "expertise": ["System Architecture", "Code Review", "Technical Leadership"],
        "model": "qwen2.5-coder:14b",  # Advanced code model
        "temperature": 0.4
    },
    "backend_developer": {
        "role": "Backend Developer",
        "expertise": ["Python", "APIs", "Databases", "Server-side Logic"],
        "model": "qwen2.5-coder:latest",  # Code specialist
        "temperature": 0.3
    },
    "frontend_developer": {
        "role": "Frontend Developer",
        "expertise": ["React", "JavaScript", "CSS", "UI Implementation"],
        "model": "qwen2.5-coder:latest",  # Code specialist
        "temperature": 0.4
    },
    "qa_tester": {
        "role": "QA Tester",
        "expertise": ["Test Cases", "Bug Finding", "Quality Assurance"],
        "model": "phi3:latest",  # Fast and efficient
        "temperature": 0.5
    },
    "devops": {
        "role": "DevOps Engineer",
        "expertise": ["CI/CD", "Docker", "Cloud Infrastructure", "Deployment"],
        "model": "qwen2.5-coder:latest",  # Good for scripts and configs
        "temperature": 0.4
    },
    "designer": {
        "role": "UI/UX Designer",
        "expertise": ["UI Design", "UX Research", "Wireframing", "Prototyping"],
        "model": "gemma3n:latest",  # Creative tasks
        "temperature": 0.8
    },
    "security": {
        "role": "Security Expert",
        "expertise": ["Security Audits", "Vulnerability Assessment", "Best Practices"],
        "model": "deepseek-r1:latest",  # Deep analysis
        "temperature": 0.2
    },
    "tech_writer": {
        "role": "Technical Writer",
        "expertise": ["Documentation", "API Docs", "User Guides"],
        "model": "phi3:latest",  # Fast and clear
        "temperature": 0.6
    }
}


def create_agent(agent_type: str, name: Optional[str] = None) -> SpecializedAgent:
    """
    Factory function to create a specialized agent

    Args:
        agent_type: Type of agent (key from AGENT_CONFIGS)
        name: Optional custom name for the agent

    Returns:
        A configured SpecializedAgent instance
    """
    if agent_type not in AGENT_CONFIGS:
        raise ValueError(f"Unknown agent type: {agent_type}. Available: {list(AGENT_CONFIGS.keys())}")

    config = AGENT_CONFIGS[agent_type]
    agent_name = name or f"{config['role']} Agent"

    return SpecializedAgent(
        role=config["role"],
        name=agent_name,
        expertise=config["expertise"],
        model_name=config["model"],
        temperature=config["temperature"]
    )
