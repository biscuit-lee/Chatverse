package com.prum.chatverse.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
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

import com.prum.chatverse.dto.CreatePostRequest;
import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.entity.Like;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.*;
import com.prum.chatverse.service.PostService;

@ExtendWith(MockitoExtension.class)

public class PostServiceTest {
    @Mock
    private PostRepository postRepository;
    
    @Mock
    private UserRepository userRepository;
    @Mock
    private LikeRepository likeRepository;

    @InjectMocks
    private PostService postService;

    @Test
    void whenCreatePost_shouldSaveAndReturnPost(){
        // Create fake user
        String fakeUsername = "bob";
        User fakeUser = new User();
        fakeUser.setUsername(fakeUsername);
        
        // Create fake post request
        String postString = "Hello fake Twitter!";
        CreatePostRequest request = new CreatePostRequest(postString);
        
        // Create fake post result 
        Post fakeSavedPost = new Post();
        fakeSavedPost.setId(1L);
        fakeSavedPost.setContent(postString);
        fakeSavedPost.setAuthor(fakeUser);

        // Define fake behavior
        when(userRepository.findByUsername(fakeUsername)).thenReturn(Optional.of(fakeUser));

        when(postRepository.save(any(Post.class))).thenReturn(fakeSavedPost);
        
        // Simulate posting
        PostResponse result = postService.createPost(request,fakeUsername);
        
        // Asserts

        assertNotNull(result);
        assertEquals(result.content(), postString);

        verify(postRepository).save(any(Post.class));

    }

    @Test
    void whenLikePost_shouldIncreaseLikeCount(){
        User fakeUser = new User();
        fakeUser.setUsername("bob");

        Post fakePost = new Post();
        fakePost.setLikes(5);

        when(userRepository.findByUsername("bob")).thenReturn(Optional.of(fakeUser));

        when(postRepository.findById(1L)).thenReturn(Optional.of(fakePost));

        when(likeRepository.existsByLikerAndPost(fakeUser,fakePost)).thenReturn(false);

        Post result = postService.likePost(1L, "bob");

        assertEquals(6, result.getLikes());

        // verify if the service actually called saved
        verify(likeRepository).save(any(Like.class));
    }

    @Test
    void whenSameUserLikePost_shouldThrowException(){
        User fakeUser = new User();
        fakeUser.setUsername("bob");

        Post fakePost = new Post();
        fakePost.setLikes(5);

        when(userRepository.findByUsername("bob")).thenReturn(Optional.of(fakeUser));

        when(postRepository.findById(1L)).thenReturn(Optional.of(fakePost));

        when(likeRepository.existsByLikerAndPost(fakeUser,fakePost)).thenReturn(true);

        assertThrows(IllegalStateException.class, () -> postService.likePost(1L, "bob"));

        // Verify that it does not save
        verify(likeRepository,never()).save(any(Like.class));
    }

    @Test
    void whenLikerDoesNotExist_shuoldThrowException(){
        User fakeUser = new User();
        fakeUser.setUsername("bob");

        Post fakePost = new Post();
        fakePost.setLikes(5);

        when(userRepository.findByUsername("bob")).thenReturn(Optional.empty());

        assertThrows(NoSuchElementException.class, () -> postService.likePost(1L, "bob"));

        // Verify that it does not save
        verify(likeRepository,never()).save(any(Like.class));

    }

    @Test
    void whenLikingPostDoesNotExist_shuoldThrowException(){
        User fakeUser = new User();
        fakeUser.setUsername("bob");

        Post fakePost = new Post();
        fakePost.setLikes(5);

        when(userRepository.findByUsername("bob")).thenReturn(Optional.of(fakeUser));

        when(postRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(NoSuchElementException.class, () -> postService.likePost(1L, "bob"));

        // Verify that it does not save
        verify(likeRepository,never()).save(any(Like.class));

    }

}
