package com.prum.chatverse.dto;

public record DislikeResponse(
    boolean disliked,
    int dislikeCount
) {}
