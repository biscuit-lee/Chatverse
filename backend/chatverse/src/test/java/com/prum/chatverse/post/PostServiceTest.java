package com.prum.chatverse.post;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.prum.chatverse.dto.CreatePostRequest;
import com.prum.chatverse.dto.PostResponse;
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

    }
    
    
}
