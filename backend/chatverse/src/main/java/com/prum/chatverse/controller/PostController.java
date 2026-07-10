package com.prum.chatverse.controller;

import java.security.Principal;

import org.springframework.web.bind.annotation.*;

import com.prum.chatverse.dto.*;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.service.PostService;

@RestController
@RequestMapping("/api/posts")
public class PostController {
    private final PostService postService;

    public PostController(PostService postService){
        this.postService = postService;
    }
    
    @GetMapping
    public String getPosts(){
        return "Get all posts";
    }

    @PostMapping
    public PostResponse createPost(@RequestBody CreatePostRequest createPostRequest, Principal principal){
        String username = principal.getName();
        return postService.createPost(createPostRequest, username);
    }

    @PostMapping("/{postId}/like")
    public LikeResponse likePost(@PathVariable Long postId, Principal principal){
        String username = principal.getName();
        Post resultPost = postService.likePost(postId, username);
        return new LikeResponse(true, resultPost.getLikes());
    }

    @PostMapping("/{postId}/dislike")
    public void dislikePost(@PathVariable Long postId, Principal principal){
        String username = principal.getName();
    }
}
