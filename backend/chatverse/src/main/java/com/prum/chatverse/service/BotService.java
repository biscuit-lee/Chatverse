package com.prum.chatverse.service;

import org.springframework.stereotype.Service;

@Service
public class BotService {
    private final UserService userService;

    public BotService(UserService userService){
        this.userService = userService;
    }
    
}
