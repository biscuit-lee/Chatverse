package com.prum.chatverse.dto;

import java.time.LocalDateTime;

public record CommentResponse(
    Long id,
    String text,
    Long authorId,
    String username,
    LocalDateTime createdAt,
    int likes,
    int dislikes,
    String profilePictureUrl
) {}
