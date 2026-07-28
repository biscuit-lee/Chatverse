package com.prum.chatverse.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.ApiKeyResponse;
import com.prum.chatverse.dto.BotSignUpRequest;
import com.prum.chatverse.dto.BotSignUpResponse;
import com.prum.chatverse.dto.LoginRequest;
import com.prum.chatverse.dto.LoginResponse;
import com.prum.chatverse.dto.RegisterRequest;
import com.prum.chatverse.dto.RegisterResponse;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.entity.UserType;
import com.prum.chatverse.repository.UserRepository;

@Service
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final ApiKeyService apiKeyService;

    public AuthService(ApiKeyService apiKeyService,UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService){
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
        this.apiKeyService = apiKeyService;
    }

    public RegisterResponse signUp(RegisterRequest registerRequest){
        // Check if username is taken
        if (userRepository.existsByUsername(registerRequest.username())){
            throw new RuntimeException("Username Taken");
        }

        User newUser = new User();
        newUser.setUsername(registerRequest.username());
        newUser.setPassword(passwordEncoder.encode(registerRequest.password()));
        newUser.setUserType(UserType.HUMAN);
        
        User savedUser = userRepository.save(newUser);

        return new RegisterResponse(
            savedUser.getId(),
            savedUser.getUsername()
        );
    }
    
    public LoginResponse login(LoginRequest loginRequest){
        // If user does not exists
        if (!userRepository.existsByUsername(loginRequest.username())){
            throw new RuntimeException("Invalid credentials");
        }
        
        User user = userRepository.findByUsername(loginRequest.username())
        .orElseThrow(() -> new RuntimeException("Invalid Credentials"));
        

        if (user.getUserType() == UserType.BOT){
            throw new RuntimeException("Bots cannot sign in");
        }        

        boolean passwordMatch = passwordEncoder.matches(loginRequest.password(), user.getPassword());
        
        if (!passwordMatch){
            throw new RuntimeException("Invalid credentials");
        }
        
        String token = jwtService.generateToken(loginRequest.username());

        return new LoginResponse(token,user.getUsername(),user.getId());

    }

    public BotSignUpResponse botSignUp(BotSignUpRequest botSignUpRequest){
        // Check if username is taken
        if (userRepository.existsByUsername(botSignUpRequest.username())){
            throw new RuntimeException("Username Taken");
        }

        User newUser = new User();
        newUser.setUsername(botSignUpRequest.username());
        newUser.setPassword(null);
        newUser.setBio(botSignUpRequest.bio());
        newUser.setProfilePictureUrl(botSignUpRequest.profilePictureUrl());

        User savedUser = userRepository.save(newUser);
        
        ApiKeyResponse apiKey = apiKeyService.generateApiKey(savedUser, "bot-api-key");

        return new BotSignUpResponse(
            savedUser.getId(),
            savedUser.getUsername(),
            apiKey.rawApiKey()

        );
    }
}
