package com.prum.chatverse.controller;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.prum.chatverse.dto.*;
import com.prum.chatverse.service.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;

    public UserController(UserService userService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public UserInfoResponse getUserById(@PathVariable Long postId){
        return userService.getUserInfo(postId);
    }

    @PostMapping("/register")
    public RegisterResponse signUp(@RequestBody RegisterRequest registerRequest){
        return userService.signUp(registerRequest);
    }

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest loginRequest){
        return userService.login(loginRequest);
    }
}
