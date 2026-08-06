import asyncio

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

    # Discover all tools
    tools = await client.get_tools()

    # Convert list -> dictionary for easy access
    tools = {tool.name: tool for tool in tools}

    print("\nAvailable Tools:")
    for name in tools:
        print("-", name)

    print("\n" + "=" * 50)

    # ----------------------------------------------------
    # List Directory
    # ----------------------------------------------------
    print("\n1. Listing Directory")
    result = await tools["list_directory"].ainvoke({"path": "."})
    print(result)

    # ----------------------------------------------------
    # Create Directory
    # ----------------------------------------------------
    print("\n2. Creating Directory")
    result = await tools["create_directory"].ainvoke(
        {
            "path": "TestFolder"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Write File
    # ----------------------------------------------------
    print("\n3. Writing File")
    result = await tools["write_file"].ainvoke(
        {
            "path": "TestFolder/hello.txt",
            "content": "Hello from MCP!"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Read File
    # ----------------------------------------------------
    print("\n4. Reading File")
    result = await tools["read_file"].ainvoke(
        {
            "path": "TestFolder/hello.txt"
        }
    )
    print(result)

    # ----------------------------------------------------
    # File Info
    # ----------------------------------------------------
    print("\n5. File Info")
    result = await tools["get_file_info"].ainvoke(
        {
            "path": "TestFolder/hello.txt"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Search Files
    # ----------------------------------------------------
    print("\n6. Search Files")
    result = await tools["search_files"].ainvoke(
        {
            "path": ".",
            "pattern": "hello"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Copy File
    # ----------------------------------------------------
    print("\n7. Copy File")
    result = await tools["copy_file"].ainvoke(
        {
            "source": "TestFolder/hello.txt",
            "destination": "TestFolder/hello_copy.txt"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Move File
    # ----------------------------------------------------
    print("\n8. Move File")
    result = await tools["move_file"].ainvoke(
        {
            "source": "TestFolder/hello_copy.txt",
            "destination": "TestFolder/moved.txt"
        }
    )
    print(result)

    # ----------------------------------------------------
    # Delete File
    # ----------------------------------------------------
    print("\n9. Delete File")
    result = await tools["delete_file"].ainvoke(
        {
            "path": "TestFolder/moved.txt"
        }
    )
    print(result)

    print("\nFinished!")


if __name__ == "__main__":
    asyncio.run(main())