package com.prum.chatverse.controller;

import java.security.Principal;
import java.util.List;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import com.prum.chatverse.dto.*;
import com.prum.chatverse.entity.Dislike;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.service.CommentService;
import com.prum.chatverse.service.PostService;

@RestController
@RequestMapping("/api/posts")
public class PostController {
    private final PostService postService;
    private final CommentService commentService;

    public PostController(PostService postService, CommentService commentService){
        this.postService = postService;
        this.commentService = commentService;
    }
    
    @GetMapping
    public String getPosts(){
        return "hi";
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
    public DislikeResponse dislikePost(@PathVariable Long postId, Principal principal){
        String username = principal.getName();
        Post resultPost = postService.dislikePost(postId, username);
        return new DislikeResponse(true, resultPost.getDislikes());
    }

    @PostMapping("/{postId}/comment")
    public CommentResponse commnetOnPost(@PathVariable Long postId, 
        @RequestBody CreateCommentRequest commentRequest,
        Principal principal)
    {
        return commentService.createComment(principal.getName(), postId, commentRequest);
        
    }

    @GetMapping("/{postId}/comments")
    public List<CommentResponse> getCommentsByPostId(@PathVariable Long postId){
        return commentService.getCommentsByPostId(postId);
    }
}
