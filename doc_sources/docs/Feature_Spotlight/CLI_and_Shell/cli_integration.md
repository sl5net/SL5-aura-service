# Feature Spotlight: Command Line Interface (CLI) Integration

**Dedicated to my very important friend, Lub.**

The new FastAPI-based Command Line Interface (CLI) provides a clean, synchronous way to interact with our running core text processing service from any local or remote shell. This is a robust solution designed to integrate the core logic into shell environments.

---

## 1. Architecture and Synchronous CLI Concept

The service is powered by the **Uvicorn/FastAPI** server and uses a custom endpoint (`/process_cli`) to deliver a synchronous (blocking) result from an inherently asynchronous, file-based background process.

### Wait-and-Read Polling Strategy

1.  **Unique Output Override:** The API creates a unique temporary directory for each request.
2.  **Process Start:** It calls `process_text_in_background` to run the core logic in a non-blocking thread, writing the result to a `tts_output_*.txt` file within that unique folder.
3.  **Synchronous Wait:** The API function then **blocks** and polls the unique folder until the output file is created or a timeout is reached.
4.  **Result Delivery:** The API reads the content of the file, performs necessary cleanup (deleting the file and the temporary directory), and returns the final processed text in the JSON response's `result_text` field.

This ensures the CLI client only receives a response *after* the text processing is complete, guaranteeing a reliable shell experience.

## 2. Remote Access and Network Port Mapping

To allow access from remote clients like Lub's terminal, the following network configuration was required, addressing the common constraint of limited external port availability:

### Solution: External Port Mapping

Since the service runs internally on **Port 8000** and our network environment limits external access to a specific port range (e.g., `88__-8831`), we implemented **Port Mapping** on the router (Fritz!Box).

| Endpoint | Protocol | Port | Description |
| :--- | :--- | :--- | :--- |
| **External/Public** | TCP | `88__` (Example) | The port the client (Lub) must use. |
| **Internal/Local** | TCP | `8000` | The port the FastAPI service actually listens on (`--port 8000`). |

The router translates any incoming connection on the external port (`88__`) to the internal port (`8000`) of the host machine, making the service globally accessible without changing the core server configuration.

## 3. CLI Client Usage

The client must be configured with the public IP address, the external port, and the correct API-Key.

### Final Command Syntax

```bash
# Note the use of the external port 88__ for remote access
python3 cli_client.py "Was ist ein Haus" --lang "de-DE"
