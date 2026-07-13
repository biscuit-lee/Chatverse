package com.prum.chatverse.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.LoginRequest;
import com.prum.chatverse.dto.LoginResponse;
import com.prum.chatverse.dto.RegisterRequest;
import com.prum.chatverse.dto.RegisterResponse;
import com.prum.chatverse.dto.UserInfoResponse;
import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.PostRepository;
import com.prum.chatverse.repository.UserRepository;

@Service
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final PostRepository postRepository;
    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService, PostRepository postRepository){
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
        this.postRepository = postRepository;
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
    
    public UserInfoResponse getUserInfo(Long userId){
        User user = userRepository.findById(userId).orElseThrow();
        return new UserInfoResponse(
            user.getId(),
            user.getUsername(),
            user.getBio(),
            user.getFollowers(),
            user.getFollowing(),
            user.getProfilePictureUrl()
        );
    }

    public Page<PostResponse> getPostbyUserId(Long userId, Pageable pageable){
        return postRepository.findByAuthorId(userId, pageable).map(this::mapPostResponse);
    }

    private PostResponse mapPostResponse(Post post){
        return new PostResponse(
            post.getId(),
            post.getContent(),
            post.getCreatedAt(),
            post.getAuthor().getUsername(),
            post.getAuthor().getId(),
            post.getLikes(),
            post.getDislikes(),
            post.getCommentsCount(),
            post.getAuthor().getProfilePictureUrl()
        );
    }
}