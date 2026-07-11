package com.prum.chatverse.dto;
import jakarta.validation.constraints.NotBlank;

public record CreateCommentRequest(
    @NotBlank
    String content
) {}
