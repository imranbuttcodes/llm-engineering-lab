import asyncio
import json

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    client = MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    r"D:\Summer-2026",
                ],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    print(f"\nDiscovered {len(tools)} tool(s)\n")

    print(tools[0])

    result = await tools[0].ainvoke(
        {
            'path': 'TestFolder/hello.txt'
        }
    )

    print(result[0]['text'])

    # for index, tool in enumerate(tools, start=1):

    #     print("=" * 90)
    #     print(f"{index}. {tool.name}")
    #     print("=" * 90)

    #     print(f"\nDescription:\n{tool.description or 'No description'}")

    #     # -------------------------------------------------------
    #     # Handle both Pydantic models and plain dictionaries
    #     # -------------------------------------------------------
    #     if isinstance(tool.args_schema, dict):
    #         schema = tool.args_schema
    #     elif hasattr(tool.args_schema, "model_json_schema"):
    #         schema = tool.args_schema.model_json_schema()
    #     else:
    #         schema = {}

    #     properties = schema.get("properties", {})
    #     required = schema.get("required", [])

    #     print("\nParameters:")

    #     if not properties:
    #         print("  None")
    #     else:
    #         for name, info in properties.items():

    #             print(f"\n• {name}")

    #             print(f"    Type        : {info.get('type', 'Unknown')}")
    #             print(
    #                 f"    Required    : {'Yes' if name in required else 'No'}"
    #             )

    #             if info.get("description"):
    #                 print(f"    Description : {info['description']}")

    #             if "default" in info:
    #                 print(f"    Default     : {info['default']}")

    #     print("\nRaw Schema:")
    #     print(json.dumps(schema, indent=4))

    #     print("\n")


if __name__ == "__main__":
    asyncio.run(main())