package com.prum.chatverse.mapper;

import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.entity.Post;

public class PostMapper {
    public static PostResponse mapPostResponse(Post post){
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
