package com.prum.chatverse.dto;

public record LikeResponse(
    boolean liked,
    int likeCount
) {}
