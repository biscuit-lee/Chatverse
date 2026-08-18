package com.prum.chatverse.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.prum.chatverse.dto.*;
import com.prum.chatverse.service.*;

@RestController
public class AuthController {
    
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }
    @PostMapping("/register")
    public RegisterResponse signUp(@RequestBody RegisterRequest registerRequest){
        return authService.signUp(registerRequest);
    }

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest loginRequest){
        return authService.login(loginRequest);
    }

    @PostMapping("/api/auth/bot-signup")
    public BotSignUpResponse botSignUp(@RequestBody BotSignUpRequest botSignUpRequest){
        return authService.botSignUp(botSignUpRequest);
    }
}
