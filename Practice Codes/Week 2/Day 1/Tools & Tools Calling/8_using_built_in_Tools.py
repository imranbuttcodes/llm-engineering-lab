# from langchain_community.tools import DuckDuckGoSearchRun, ShellTool


# # search_tool = DuckDuckGoSearchRun()

# # result = search_tool.invoke(
# #     'what today trending news about pakistan'
# # )

# # print(result)




# shell_tool = ShellTool()

# result = shell_tool.invoke('ls')

# print(result)


# from langchain_tavily import TavilySearch


# search_tool = TavilySearch()

# result = search_tool.invoke('Trending News on AI')

# print(search_tool.args_schema)
# print(search_tool.name)
# print(result)


from langchain_experimental.tools import PythonREPLTool

python = PythonREPLTool()

print(python.invoke("print(5 * 9)"))