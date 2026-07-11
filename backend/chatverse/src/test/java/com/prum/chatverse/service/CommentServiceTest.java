package com.prum.chatverse.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.NoSuchElementException;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.prum.chatverse.dto.CommentResponse;
import com.prum.chatverse.dto.CreateCommentRequest;
import com.prum.chatverse.entity.Comment;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.CommentRepository;
import com.prum.chatverse.repository.PostRepository;
import com.prum.chatverse.repository.UserRepository;

@ExtendWith(MockitoExtension.class)
public class CommentServiceTest {
    @Mock
    private CommentRepository commentRepository;
    
    @Mock
    private UserRepository userRepository;

    @Mock
    private PostRepository postRepository;

    @InjectMocks
    private CommentService commentService;

    @Test
    void whenCreateComment_shouldSaveAndReturnComment(){
        String fakeName = "bob";
        Long fakePostId = 1L;
        String commentContent = "Hey, greg";
        CreateCommentRequest newRequest = new CreateCommentRequest(commentContent);

        Post fakePost = new Post();
        fakePost.setId(fakePostId);

        User fakeUser =new User();
        fakeUser.setUsername(fakeName);

        Comment savedComment = new Comment();
        savedComment.setContent(commentContent);
        savedComment.setPost(fakePost);
        savedComment.setAuthor(fakeUser);
        savedComment.setLikes(0);
        savedComment.setDislikes(0);

        when(postRepository.findById(fakePostId)).thenReturn(Optional.of(fakePost));
        when(userRepository.findByUsername(fakeName)).thenReturn(Optional.of(fakeUser));
        when(commentRepository.save(any(Comment.class))).thenReturn(savedComment);
        CommentResponse result = commentService.createComment(fakeName, fakePostId, newRequest);

        assertEquals(result.content(),commentContent);

        verify(commentRepository).save(any(Comment.class));
    }

    @Test
    void whenCommentIsBlank_shouldThrowError(){
        String fakeName = "bob";
        Long fakePostId = 1L;
        String commentContent = "";
        CreateCommentRequest newRequest = new CreateCommentRequest(commentContent);

        Post fakePost = new Post();
        fakePost.setId(fakePostId);

        User fakeUser = new User();
        fakeUser.setUsername(fakeName);

        Comment savedComment = new Comment();
        savedComment.setContent(commentContent);
        savedComment.setPost(fakePost);
        savedComment.setAuthor(fakeUser);
        savedComment.setLikes(0);
        savedComment.setDislikes(0);

        when(postRepository.findById(fakePostId)).thenReturn(Optional.of(fakePost));
        when(userRepository.findByUsername(fakeName)).thenReturn(Optional.of(fakeUser));
        
        assertThrows(IllegalArgumentException.class, () -> {
            commentService.createComment(fakeName, fakePostId, newRequest);
        });
        verify(commentRepository,never()).save(any(Comment.class));

    }


    @Test
    void whenCommentUserNotExist_shouldThrowError(){
        String fakeName = "bob";
        Long fakePostId = 1L;
        String commentContent = "";
        CreateCommentRequest newRequest = new CreateCommentRequest(commentContent);

        Post fakePost = new Post();
        fakePost.setId(fakePostId);

        User fakeUser =new User();
        fakeUser.setUsername(fakeName);

        Comment savedComment = new Comment();
        savedComment.setContent(commentContent);
        savedComment.setPost(fakePost);
        savedComment.setAuthor(fakeUser);
        savedComment.setLikes(0);
        savedComment.setDislikes(0);
        
        when(postRepository.findById(fakePostId)).thenReturn(Optional.of(fakePost));
        when(userRepository.findByUsername(fakeName)).thenReturn(Optional.empty());
        
        assertThrows(NoSuchElementException.class, () -> {
            commentService.createComment(fakeName, fakePostId, newRequest);
        });
        verify(commentRepository,never()).save(any(Comment.class));

    }

    @Test
    void whenCommentPostNotExist_shouldThrowError(){
        String fakeName = "bob";
        Long fakePostId = 1L;
        String commentContent = "";
        CreateCommentRequest newRequest = new CreateCommentRequest(commentContent);

        Post fakePost = new Post();
        fakePost.setId(fakePostId);

        User fakeUser =new User();
        fakeUser.setUsername(fakeName);

        Comment savedComment = new Comment();
        savedComment.setContent(commentContent);
        savedComment.setPost(fakePost);
        savedComment.setAuthor(fakeUser);
        savedComment.setLikes(0);
        savedComment.setDislikes(0);
        
        when(postRepository.findById(fakePostId)).thenReturn(Optional.empty());
        
        assertThrows(NoSuchElementException.class, () -> {
            commentService.createComment(fakeName, fakePostId, newRequest);
        });
        verify(commentRepository,never()).save(any(Comment.class));

    }

}
