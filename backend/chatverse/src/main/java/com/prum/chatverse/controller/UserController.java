package com.prum.chatverse.controller;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import com.prum.chatverse.dto.*;
import com.prum.chatverse.service.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    private final AuthService authService;

    public UserController(UserService userService, AuthService authService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.authService = authService;
    }
    
    @GetMapping("/{postId}")
    public UserInfoResponse getUserById(@PathVariable Long postId){
        return userService.getUserInfo(postId);
    }

    @GetMapping("/{userId}/posts")
    public Page<PostResponse> getPostsByUserId(@PathVariable Long userId, Pageable pageable){
        return userService.getPostbyUserId(userId, pageable);
    }

    @PostMapping("/register")
    public RegisterResponse signUp(@RequestBody RegisterRequest registerRequest){
        return authService.signUp(registerRequest);
    }

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest loginRequest){
        return authService.login(loginRequest);
    }
}
