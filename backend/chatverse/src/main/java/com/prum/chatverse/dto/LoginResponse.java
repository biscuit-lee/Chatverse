package com.prum.chatverse.dto;

public record LoginResponse(
    String token,
    String username,
    Long id
)
{}
