from agent_framework.tools.socials.post import PostTool
from unittest.mock import MagicMock

def test_create_post(mock_client):
    post_tool = PostTool(client=mock_client)
    arguments = {"content": "Hello from my agent"}
    response = post_tool.execute(arguments)

    mock_client.post.assert_called_once_with(
        path="api/posts",
        json={"content": "Hello from my agent"}
    )

def test_create_post_error():
    bad_client = MagicMock()
    bad_client.post.side_effect = Exception("connection refused")
    tool = PostTool(client=bad_client)
    result = tool.execute({"content": "hello"})
    assert "error" in result

def test_argument_schema():
    tool = PostTool(client=MagicMock())
    schema = tool.argument_schema()
    assert "content" in schema["properties"]
    assert "content" in schema["required"]