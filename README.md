# 🤖 AI Invoice Agent

An intelligent invoice management assistant powered by local LLM models (Ollama) and Phidata framework. Query invoices, check statuses, and download PDFs using natural language - all running locally with zero API costs!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Phidata](https://img.shields.io/badge/phidata-2.4+-orange.svg)
![Ollama](https://img.shields.io/badge/ollama-powered-purple.svg)

## ✨ Features

- 🧠 **Local LLM** - Runs completely offline using Ollama (Llama 3.1, Mistral, etc.)
- 💰 **Zero API Costs** - No OpenAI charges, unlimited queries
- 🎨 **Beautiful Web UI** - Modern Streamlit interface with real-time chat
- 💾 **Conversation Memory** - SQLite-based persistent storage
- 🔒 **Data Privacy** - All data stays on your machine
- 🛠️ **Three Core Functions**:
  - Get invoice details
  - Check invoice status
  - Download invoice PDFs
- 🎯 **Context-Aware** - Remembers previous queries in conversation
- ⚡ **Smart Suggestions** - Recommends actions based on invoice status

## 📸 Screenshots

### Web Interface
```
┌─────────────────────────────────────────────────────────┐
│  📄 Invoice AI Assistant                                │
│  Your intelligent invoice management companion          │
├─────────────────────────────────────────────────────────┤
│  You: Give me details for invoice 3479                  │
│                                                          │
│  🔧 Tool: get_invoice_details                           │
│  📊 Result: Successfully retrieved...                    │
│                                                          │
│  Assistant: I've retrieved the details for invoice...   │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed
- 8GB+ RAM (for 7-8B models) or 16GB+ (for larger models)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-invoice-agent.git
cd ai-invoice-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install and start Ollama**
```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai for Windows

# Start Ollama server
ollama serve

# Pull the model (in another terminal)
ollama pull llama3.1:8b
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**

**Option A: Streamlit Web UI (Recommended)**
```bash
streamlit run streamlit_app.py
```
Open http://localhost:8501 in your browser

**Option B: Command Line**
```bash
python invoice_agent.py
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# Local LLM Configuration
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama3.1:8b

# Invoice API Configuration
INVOICE_API_BASE_URL=http://localhost:8000/invoices
INVOICE_API_KEY=your-api-key-here

# Database Configuration (SQLite - default)
DB_FILE=invoice_agent.db
```

## 🧪 Testing with Mock API

We provide a complete mock API server for testing:

1. **Start the mock server**
```bash
python mock_api_server.py
```

2. **Update .env**
```env
INVOICE_API_BASE_URL=http://localhost:5000/invoices
INVOICE_API_KEY=test-key
```

3. **Test with sample invoices**
- Invoice 3479 - Paid ($15,000)
- Invoice 3481 - Overdue (£22,000)
- Invoice 3485 - Very overdue ($7,500)
- And 7 more test invoices

## 📚 Usage Examples

### Web Interface

1. Start the Streamlit app
2. Type natural language queries:

```
"Give me details for invoice 3479"
"What's the status of invoice 3481?"
"Download invoice 3483 PDF"
"Show me all overdue invoices"
```

### Command Line

```python
from invoice_agent import create_invoice_agent

agent = create_invoice_agent("session_123")
response = agent.run("Get details for invoice 3479")
print(response.content)
```

### Context-Aware Conversations

```
You: "Show me invoice 3479"
Agent: [Displays invoice details]

You: "What's its status?"
Agent: [Remembers 3479, checks status]

You: "Download it"
Agent: [Downloads PDF for invoice 3479]
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit UI                       │
│            (Beautiful Web Interface)                │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│              Phidata Agent Framework                │
│  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Ollama LLM   │  │  SQLite     │  │  Tools    │ │
│  │ (Local)      │  │  Storage    │  │ Functions │ │
│  └──────────────┘  └─────────────┘  └───────────┘ │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│              Your Invoice API                       │
│  • GET /invoices/{id}         (Details)            │
│  • GET /invoices/{id}/status  (Status)             │
│  • GET /invoices/{id}/pdf     (Download)           │
└─────────────────────────────────────────────────────┘
```

## 🔧 API Integration

### FastAPI Implementation

The project includes a complete FastAPI implementation for serving invoice PDFs:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
INVOICES_DIR = Path("./invoices")

@app.get("/invoices/{invoice_no}/pdf")
async def download_invoice_pdf(invoice_no: str):
    file_path = INVOICES_DIR / f"invoice_{invoice_no}.pdf"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"invoice_{invoice_no}.pdf"
    )
```

Run your FastAPI server:
```bash
uvicorn main:app --reload
```

## 🎯 Supported Models

Choose based on your hardware:

| Model | RAM Required | Speed | Quality | Best For |
|-------|--------------|-------|---------|----------|
| llama3.1:8b | 8GB | ⚡⚡⚡ | ⭐⭐⭐ | General use (recommended) |
| mistral:7b | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Speed priority |
| qwen2.5:14b | 16GB | ⚡⚡ | ⭐⭐⭐⭐ | Best balance |
| llama3.1:70b | 32GB+ | ⚡ | ⭐⭐⭐⭐⭐ | Maximum quality |

Change model in `.env`:
```env
MODEL_NAME=qwen2.5:14b
```

## 📦 Project Structure

```
ai-invoice-agent/
├── invoice_agent.py          # CLI version
├── streamlit_app.py          # Web UI version
├── mock_api_server.py        # Test API server
├── fastapi_implementation.py # FastAPI PDF endpoint
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── README.md                # This file
├── test_data/
│   └── invoices.json        # Sample invoice data
└── invoices/                # PDF storage directory
```

## 🛠️ Development

### Running Tests

```bash
# Test Ollama connection
python -c "from invoice_agent import check_ollama_status; check_ollama_status()"

# Test with mock data
python mock_api_server.py  # In one terminal
python invoice_agent.py     # In another terminal
```

### Adding New Tools

```python
def your_custom_function(param: str) -> dict:
    """Your function description"""
    # Implementation
    return {"result": "success"}

# Add to agent
agent = Agent(
    tools=[
        Function.from_callable(your_custom_function),
        # ... other tools
    ]
)
```

## 🔒 Security Features

- ✅ Input validation for invoice numbers
- ✅ Directory traversal prevention
- ✅ API key authentication support
- ✅ Local data processing (no cloud)
- ✅ Configurable CORS policies
- ✅ Rate limiting ready

## 💡 Use Cases

- **Accounting Teams** - Quick invoice lookups without navigating complex systems
- **Customer Support** - Instant invoice status for customer queries
- **Finance Departments** - Bulk invoice status checks
- **Small Businesses** - Affordable invoice management
- **Developers** - API testing and integration

## 🚧 Roadmap

- [ ] Multi-language support
- [ ] Bulk operations (process multiple invoices)
- [ ] Email notifications for overdue invoices
- [ ] Invoice analytics and reporting
- [ ] Integration with accounting software (QuickBooks, Xero)
- [ ] Mobile app support
- [ ] Voice interface
- [ ] Advanced search and filtering

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Phidata](https://phidata.com) - Agent framework
- [Ollama](https://ollama.ai) - Local LLM runtime
- [Streamlit](https://streamlit.io) - Web UI framework
- [FastAPI](https://fastapi.tiangolo.com) - API framework

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by Vinay Gandhi**

*Powered by Local LLMs - No API costs, Full privacy*
