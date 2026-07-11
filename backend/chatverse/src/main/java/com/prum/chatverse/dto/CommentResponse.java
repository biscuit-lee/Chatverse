package com.prum.chatverse.dto;

import java.time.LocalDateTime;

public record CommentResponse(
    Long id,
    String content,
    Long authorId,
    String authorName,
    LocalDateTime createdAt,
    int likeCount,
    int dislikeCount
) {}
