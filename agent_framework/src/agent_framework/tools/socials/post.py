from agent_framework.tools.base_tool import BaseTool
from agent_framework.tools.chatverse_service.client import client
class PostTool(BaseTool):
    def __init__(self, client):
        super().__init__(name="create_post", description="Tool for posting content to the social media platform.")
        self.post_url = "api/posts"
        self.client = client
    
    def argument_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The content of the post."},
            },
            "required": ["content"]
        }
    
    def execute(self, arguments: dict):
        payload = {
            "content": arguments["content"],
        }
        
        try:
            return self.client.post(path=self.post_url, json=payload)

        except Exception as e:
            return {"error": str(e)}
