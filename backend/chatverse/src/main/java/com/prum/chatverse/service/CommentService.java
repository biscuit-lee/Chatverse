package com.prum.chatverse.service;

import java.util.List;

import com.prum.chatverse.dto.CommentResponse;
import com.prum.chatverse.dto.CreateCommentRequest;
import com.prum.chatverse.entity.Comment;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.CommentRepository;
import com.prum.chatverse.repository.PostRepository;
import com.prum.chatverse.repository.UserRepository;

import jakarta.validation.Valid;

public class CommentService {
    private final CommentRepository commentRepository;
    private final UserRepository userRepository;
    private final PostRepository postRepository;
    public CommentService(CommentRepository commentRepository, UserRepository userRepository, PostRepository postRepository){
        this.commentRepository = commentRepository;
        this.postRepository = postRepository;
        this.userRepository = userRepository;
    } 

    public CommentResponse createComment(String username, Long postId, @Valid CreateCommentRequest createCommentRequest){
        Post targetPost = postRepository.findById(postId).orElseThrow();
        User commenter = userRepository.findByUsername(username).orElseThrow();
        String commentContent = createCommentRequest.content();

        if (commentContent == null || commentContent.isBlank()){
            throw new IllegalArgumentException("Comment cannot be blank");
        }
        
        Comment newComment = new Comment();
        newComment.setContent(commentContent);
        newComment.setAuthor(commenter);
        newComment.setPost(targetPost);

        Comment saved = commentRepository.save(newComment);

        return mapToResponse(saved);
    }

    public List<CommentResponse> getCommentsByPostId(Long postId){
        return commentRepository.findByPostId(postId)
        .stream().map(this::mapToResponse).toList();
    }

    private CommentResponse mapToResponse(Comment comment){

        return new CommentResponse(
            comment.getId(),
            comment.getContent(),
            comment.getAuthor().getId(),
            comment.getAuthor().getUsername(),
            comment.getCreatedAt(),
            comment.getLikes(),
            comment.getDislikes(),
            comment.getAuthor().getProfilePictureUrl()
        );
    }
}
