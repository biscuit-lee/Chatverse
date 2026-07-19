package com.prum.chatverse.controller;

import java.security.Principal;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.prum.chatverse.entity.User;
import com.prum.chatverse.service.ApiKeyService;
import com.prum.chatverse.service.UserService;

@RestController
@RequestMapping("/api/apikeys")
public class ApikeyController {
    private final ApiKeyService apiKeyService;
    private final UserService userService;
    public ApikeyController(ApiKeyService apiKeyService, UserService userService) {
        this.apiKeyService = apiKeyService;
        this.userService = userService;
    }

    @PostMapping("/generate")
    public String generateApiKey(Principal principal) {
        User user = userService.getUserByUsername(principal.getName());
        return apiKeyService.generateApiKey(user);
    }

    
    
}
