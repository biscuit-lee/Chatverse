package com.prum.chatverse.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.dto.UserInfoResponse;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.PostRepository;
import com.prum.chatverse.repository.UserRepository;

@Service
public class SearchService {
    private final PostRepository postRepository;
    private final UserRepository userRepository;
    public SearchService(PostRepository postRepository, UserRepository userRepository){
        this.postRepository = postRepository;
        this.userRepository = userRepository;
    }

    public Page<PostResponse> searchPost(String query, Pageable pageable){
        return postRepository.search(query, pageable).map(this::mapPostResponse);
    }


    public Page<UserInfoResponse> searchUser(String query, Pageable pageable){
        return userRepository.findByUsernameContainingIgnoreCase(query, pageable).map(this::mapUserInfoResponse);
    }


    private UserInfoResponse mapUserInfoResponse(User user){
        return new UserInfoResponse(
            user.getId(),
            user.getUsername(),
            user.getBio(),
            user.getFollowers(),
            user.getFollowing(),
            user.getProfilePictureUrl()
        );
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
