package com.prum.chatverse.dto;

public record UserInfoResponse(
    Long id,
    String username,
    String bio,
    int followers,
    int following,
    String profilePictureUrl) {} 