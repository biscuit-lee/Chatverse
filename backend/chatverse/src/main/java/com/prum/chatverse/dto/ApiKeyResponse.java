package com.prum.chatverse.dto;

public record ApiKeyResponse(
    Long id,
    String keyName,
    String rawApiKey,
    boolean isActive
) {}
