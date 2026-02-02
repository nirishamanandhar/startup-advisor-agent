# ☘️ Ireland Startup Support Chatbot 
### Conversational Chatbot Interface for Irish Founder Support

This project implements a **stateful, streaming chatbot interface** designed to help Irish founders navigate the local ecosystem (Enterprise Ireland, LEOs, NDRC, etc.) to help scale their business. 
It leverages a **decoupled architecture** to separate LLM communication from state management.

---

## 🏗️ System Design & Architecture

The primary goal was to ensure **Stateless-to-Stateful Mapping**.  
Since LLM APIs are inherently stateless, this system implements a **Sliding Window Memory Buffer** to maintain conversational context without exceeding token limits.

### High-Level Architecture

- **User Interface Layer**  
  A CLI-based loop handles standard input/output and signal interrupts.

- **Logic Layer (`LLMService`)**  
  An abstraction over the OpenAI SDK, allowing for *swapping* models based on availability and compatibility (e.g., Gemini, Groq, or local Llama) by modifying the `base_url` and `api_key`.

- **Persistence Layer (`ConversationManager`)**  
  A volatile memory store that injects the `system_prompt` and prunes history based on a pre-defined `max_history` parameter to prevent context window overflow.

### Sequential Logic Flow

The data follows a **circular pipeline** to ensure that the AI “remembers” previous runs across the conversation lifecycle.

---

## 🛠️ Developer Documentation

### 🧩 Core Components

#### 1. `LLMService` (The Connector)

This class encapsulates all API-calling logic.

- **Decoupling**  
  By passing `api_key` and `base_url` during initialization, the service can connect to any OpenAI-compatible provider.

- **Streaming**  
  Configured to return a generator object, enabling real-time text rendering for a low-latency experience.

- **Robustness**  
  Implements `try–except` blocks to handle network timeouts.

---

#### 2. `ConversationManager` (Memory Engine)

This is the “brain” that manages the context window.

- **Sliding Window Memory**  
  To keep costs low, it only remembers the last `N` messages (`max_history`).

- **System Integrity**  
  Ensures the **System Prompt** is always stored at index `0` and saved in the memory, preventing purpose drift during long conversations.

---

#### 3. `main.py` (The Orchestrator)

The entry point that ties all services together.

- **Accumulator Pattern**  
  Since `stream=True` is used, `main.py` is responsible for capturing streamed chunks and reassembling the `full_reply` before saving it back into the `ConversationManager`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Dependencies:
  ```bash
  pip install openai python-dotenv

### Configuration

Create a .env file in your root directory:
```bash
# Example for different API keys
groq_key=gsk_your_key_here
# Example for Gemini
# google_key=your_key_here
```

### Running the Bot
```bash
python main.py
```

🛠️ Maintenance & Troubleshooting

 - Connection Errors
 - Verify your base_url.

Groq typically uses .../v1

Gemini uses .../v1beta/openai/

### Response Cutoff
max_tokens is set to 200 for token usage reductions.
For longer responses, consider increasing this to 512 or 1024.
