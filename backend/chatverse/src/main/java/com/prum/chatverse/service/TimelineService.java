package com.prum.chatverse.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.entity.Post;
import com.prum.chatverse.repository.DislikeRepository;
import com.prum.chatverse.repository.FollowRepository;
import com.prum.chatverse.repository.LikeRepository;
import com.prum.chatverse.repository.PostRepository;

@Service
public class TimelineService {
    private final FollowRepository followRepository;
    private final LikeRepository likeRepository;
    private final DislikeRepository dislikeRepository;
    private final PostRepository postRepository;

    public TimelineService(FollowRepository followRepository, LikeRepository likeRepository, DislikeRepository dislikeRepository, PostRepository postRepository){
        this.dislikeRepository = dislikeRepository;
        this.likeRepository = likeRepository;
        this.followRepository = followRepository;
        this.postRepository = postRepository;
    }

    public Page<PostResponse> getFeed(String sortType, Pageable pageable){
        switch (sortType) {
            // order by like-dislike ratio
            case "hot":
                return postRepository.findAllByScoreDesc(pageable).map(this::mapPostResponse);
            
            case "new":
                return postRepository.findAllByOrderByCreatedAtDesc(pageable).map(this::mapPostResponse);

            default:
                return postRepository.findAllByOrderByCreatedAtDesc(pageable).map(this::mapPostResponse);

        }
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
