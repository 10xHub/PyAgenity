import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client
from mcp import Tool


load_dotenv()


print(os.getenv("GITHUB_TOKEN"))

config = {
    "mcpServers": {
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable-http",
        },
        # "github": {
        #     "url": "https://api.githubcopilot.com/mcp/",
        #     "headers": {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        #     "transport": "streamable-http",
        # },
    }
}


client_http = Client(config)


async def call_tools():
    async with client_http:
        tools: list[Tool] = await client_http.list_tools()
        for i in tools:
            print(i.model_dump())


async def invoke():
    async with client_http:
        result = await client_http.call_tool(
            "get_weather",
            {"location": "New York", "tool_call_id": "12345", "config": {"units": "metric"}},
        )
        print(result)


async def main():
    await call_tools()
    await invoke()


if __name__ == "__main__":
    asyncio.run(main())


# CallToolResult(content=[TextContent(type='text', text='The weather in New York is sunny.', annotations=None, meta=None)], structured_content={'result': 'The weather in New York is sunny.'}, data='The weather in New York is sunny.', is_error=False)
# CallToolResult(content=[TextContent(type='text', text='{"location":"New York","temperature":"22°C","description":"Sunny"}', annotations=None, meta=None)], structured_content={'location': 'New York', 'temperature': '22°C', 'description': 'Sunny'}, data={'location': 'New York', 'temperature': '22°C', 'description': 'Sunny'}, is_error=False)
