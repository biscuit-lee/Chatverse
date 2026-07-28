package com.prum.chatverse.dto;

public record BotSignUpRequest(
    String username,
    String bio,
    String profilePictureUrl
) {
    
}
