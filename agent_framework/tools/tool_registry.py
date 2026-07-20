from base_tool import BaseTool

class ToolRegistry:
    """
    Tool registry class
    
    """
    
    def __init__(self):
        self.tools: dict[str,BaseTool] = {}

    def register(self,tool: BaseTool):
        if tool.name in self.tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")

        self.tools[tool.name] = tool

    def get(self,tool_name: str) -> BaseTool:
        return self.tools.get(tool_name)