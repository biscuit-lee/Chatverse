from agent_framework.tools.socials.comment import PostCommentTool
from unittest.mock import MagicMock

def test_create_comment(mock_client):
    comment_tool = PostCommentTool(client=mock_client)
    arguments = {"post_id": 123, "content": "This is a comment"}
    response = comment_tool.execute(arguments)

    mock_client.post.assert_called_once_with(
        path="api/posts/123/comment",
        json={"content": "This is a comment"}
    )


def test_create_comment_error():
    bad_client = MagicMock()
    bad_client.post.side_effect = Exception("connection refused")
    tool = PostCommentTool(client=bad_client)
    result = tool.execute({"post_id": 123, "content": "This is a comment"})
    assert "error" in result