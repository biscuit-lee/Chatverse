package com.prum.chatverse.service;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import com.prum.chatverse.repository.*;
import com.prum.chatverse.dto.*;
import com.prum.chatverse.entity.*;

@Service
public class PostService {
    private final PostRepository postRepository;
    private final UserRepository userRepository;
    private final LikeRepository likeRepository;
    private final DislikeRepository dislikeRepository;
    public PostService(PostRepository postRepository, UserRepository userRepository, LikeRepository likeRepository, DislikeRepository dislikeRepository) {
        this.postRepository = postRepository;
        this.userRepository = userRepository;
        this.likeRepository = likeRepository;
        this.dislikeRepository = dislikeRepository;
    }

    public PostResponse createPost(CreatePostRequest createPostRequest, String username){
        Post newPost = new Post();
        //Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        //String username = authentication.getName();
        User author = userRepository.findByUsername(username).orElseThrow();
        
        newPost.setContent(createPostRequest.content());
        newPost.setAuthor(author);
        Post savedPost = this.postRepository.save(newPost);

        return new PostResponse(
            savedPost.getId(),
            savedPost.getContent(),
            savedPost.getCreatedAt(),
            savedPost.getAuthor().getUsername(),
            savedPost.getAuthor().getId(),
            savedPost.getLikes(), 
            savedPost.getDislikes(), 
            savedPost.getCommentsCount(),
            savedPost.getAuthor().getProfilePictureUrl()
        );


    }

    public Post likePost(Long id, String username){
        User liker = userRepository.findByUsername(username).orElseThrow();
        Post targetPost = postRepository.findById(id).orElseThrow();

        // Check if already liked the post 
        if (likeRepository.existsByLikerAndPost(liker, targetPost)){
            throw new IllegalStateException("You already liked the post");
        }

        
        Like likeObj = new Like();
        likeObj.setLiker(liker);
        likeObj.setPost(targetPost);


        targetPost.setLikes(targetPost.getLikes() + 1);

        likeRepository.save(likeObj);

        return targetPost;
    }

    public Post dislikePost(Long id, String username){
    User disliker = userRepository.findByUsername(username).orElseThrow();
    Post targetPost = postRepository.findById(id).orElseThrow();

    // Check if already liked the post 
    if (likeRepository.existsByLikerAndPost(disliker, targetPost)){
        throw new IllegalStateException("You already liked the post");
    }

    
    Dislike dislikeObj = new Dislike();
    dislikeObj.setDisliker(disliker);
    dislikeObj.setPost(targetPost);


    targetPost.setDislikes(targetPost.getDislikes() + 1);

    dislikeRepository.save(dislikeObj);

    return targetPost;
}

    
}
