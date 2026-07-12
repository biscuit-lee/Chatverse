package com.prum.chatverse.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.repository.DislikeRepository;
import com.prum.chatverse.repository.LikeRepository;
import com.prum.chatverse.repository.PostRepository;
import com.prum.chatverse.security.ApiKeyFilter;
import com.prum.chatverse.service.CommentService;
import com.prum.chatverse.service.JwtService;
import com.prum.chatverse.service.PostService;
import com.prum.chatverse.service.UserService;

@WebMvcTest(PostController.class)
@AutoConfigureMockMvc(addFilters = false) // skip the security filter chain entirely for this slice
public class PostControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    PostService postService;

    @MockitoBean
    UserService userService;

    @MockitoBean
    CommentService commentService;

    @MockitoBean
    PostRepository postRepository;

    @MockitoBean
    LikeRepository likeRepository;

    @MockitoBean
    DislikeRepository dislikeRepository;

    @MockitoBean
    JwtService jwtService;

    @MockitoBean
    ApiKeyFilter apiKeyFilter;
    @Test
    void shouldCreatePost() throws Exception {

        PostResponse postResponse = new PostResponse(
            1L,
            "Hello testers",
            LocalDateTime.now(),
            "bob",
            1L,
            0, 0, 0, null
        );

        when(postService.createPost(any(), any())).thenReturn(postResponse);

        mockMvc.perform(
            post("/api/posts")
                .principal(() -> "bob")
                .content("""
                        {"content": "Hello testers"}
                        """)
                .contentType(MediaType.APPLICATION_JSON)
        ).andExpect(status().isOk())
         .andExpect(jsonPath("$.content").value("Hello testers"));
    }
}