from phi.agent import Agent
#from phi.memory.db.postgres import PgAgentStorage
from phi.storage.agent.postgres import PgAgentStorage
from phi.model.ollama import Ollama
from phi.tools.function import Function
from tools import get_invoice_details, get_invoice_status, download_invoice_pdf

def invoice_agent(session_id: str)->Agent:

    storage = PgAgentStorage(
        table_name="agent_sessions",
        db_url="postgresql+psycopg2://postgres:Root!0019@localhost:5432/deeplearning"
    )

    agent = Agent(
        name="Invoice Assistant",
        model=Ollama(id="mistral:latest",host="http://localhost:11434"),
        storage=storage,
        session_id=session_id,
        tools=[
            Function.from_callable(get_invoice_details),
            Function.from_callable(get_invoice_status),
            Function.from_callable(download_invoice_pdf)
        ],
        instructions=[
            "You are a helpful invoice management assistant.",
            "You can retrieve invoice details, check invoice status, and download invoice PDFs.",
            "Always extract the invoice number from the user's query.",
            "When suggesting further actions, consider the user's conversation history.",
            "Be concise and professional in your responses.",
            "If an invoice is overdue, suggest contacting the customer.",
            "If an invoice is paid, congratulate and ask if they need anything else.",
            "When you need to call a function, do so immediately without asking for permission."
        ],
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=False
    )

    return agent
   

