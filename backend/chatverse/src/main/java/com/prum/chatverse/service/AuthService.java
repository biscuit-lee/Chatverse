package com.prum.chatverse.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.LoginRequest;
import com.prum.chatverse.dto.LoginResponse;
import com.prum.chatverse.dto.RegisterRequest;
import com.prum.chatverse.dto.RegisterResponse;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.UserRepository;

@Service
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService){
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    public RegisterResponse signUp(RegisterRequest registerRequest){
        // Check if username is taken
        if (userRepository.existsByUsername(registerRequest.username())){
            throw new RuntimeException("Username Taken");
        }

        User newUser = new User();
        newUser.setUsername(registerRequest.username());
        newUser.setPassword(passwordEncoder.encode(registerRequest.password()));

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
        
        boolean passwordMatch = passwordEncoder.matches(loginRequest.password(), user.getPassword());
        
        if (!passwordMatch){
            throw new RuntimeException("Wrong password");
        }
        
        String token = jwtService.generateToken(loginRequest.username());

        return new LoginResponse(token,user.getUsername(),user.getId());

    }
}
