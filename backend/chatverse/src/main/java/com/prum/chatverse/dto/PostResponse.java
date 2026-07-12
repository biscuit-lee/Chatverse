package com.prum.chatverse.dto;

import java.time.LocalDateTime;

public record PostResponse(
    Long id,
    String text,
    LocalDateTime createdAt,
    String username,
    Long authorId,
    int likes,
    int dislikes,
    int commentCount,
    String profilePictureUrl)
{}
