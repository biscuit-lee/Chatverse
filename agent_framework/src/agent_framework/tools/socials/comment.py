from agent_framework.tools.base_tool import BaseTool
from agent_framework.tools.chatverse_service.client import client as deafult_client
class PostCommentTool(BaseTool):
    """Tool for working with comments."""

    def __init__(self, client=deafult_client):
        super().__init__(name="comment_tool", description="Tool for making a comment on a post.")
        self.client = client

    def argument_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "post_id": {"type": "string", "description": "The ID of the post to comment on."},
                "content": {"type": "string", "description": "The text of the comment."},
            },
            "required": ["post_id", "content"]
        }

    def execute(self, arguments: dict):
        post_id = arguments["post_id"]
        comment_text = arguments["content"]

        payload = {
            "content": comment_text,
        }

        try:
            response = self.client.post(path=f"api/posts/{post_id}/comment", json=payload)
            return response
        except Exception as e:
            return {"error": str(e)}
