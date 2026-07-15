# Burp MCP Setup for Claude CLI

## Prerequisites

- [Burp Suite](https://portswigger.net/burp) (Community or Professional)
- [Claude CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Java runtime (bundled with Burp Suite)

## Step 1: Install the MCP Server Extension in Burp Suite

1. Open Burp Suite
2. Go to **Extensions** > **BApp Store**
3. Search for **MCP Server**
4. Click **Install**
5. Verify the extension is loaded under the **Extensions** > **Installed** tab

The extension starts an SSE server on `http://127.0.0.1:9876` by default.

## Step 2: Configure Claude CLI

Create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "burp-mcp": {
      "type": "sse",
      "url": "http://127.0.0.1:9876/"
    }
  }
}
```

> **Note:** The SSE endpoint is at `/`

## Step 3: Connect

1. Start Claude CLI in your project dir
2. Run `/mcp` to connect (or restart the session)
3. You should see: `Reconnected to burp

## Available Tools

Once connected, Claude has access to 25

| Category | Tools |
|----------|-------|
| **Proxy** | Get HTTP/WebSocket histor
| **Scanner** | Get scanner issues |
| **Repeater** | Create repeater tabs (
| **Intruder** | Send requests to intruder |
| **Collaborator** | Generate payloads,
| **HTTP Requests** | Send HTTP/1 and HTTP/2 requests directly |
| **Encoding** | Base64 and URL encode/
| **Config** | Get/set project and user options |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `HTTP 404 at .../sse` | Change the URL to `http://127.0.0.1:9876/` (root path, not `/sse`) |
| `-32000` error | Ensure Burp Suite isr extension is loaded |
| Empty proxy history | Confirm your browser is proxying through Burp (default `127.0.0.1:8080`) |
| Connection timeout | Check that port irewall |
