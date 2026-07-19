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
import com.prum.chatverse.mapper.PostMapper;
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

    public User getUserByUsername(String username){
        return userRepository.findByUsername(username).orElseThrow();
    }

    public Page<PostResponse> getPostbyUserId(Long userId, Pageable pageable){
        return postRepository.findByAuthorId(userId, pageable).map(PostMapper::mapPostResponse);
    }

}