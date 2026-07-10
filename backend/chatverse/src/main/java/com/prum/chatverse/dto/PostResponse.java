package com.prum.chatverse.dto;

import java.time.LocalDateTime;

public record PostResponse(
    Long id,
    String content,
    LocalDateTime createdAt,
    String authorName,
    int likeCount,
    int dislikeCount,
    int commentCount)
{}
