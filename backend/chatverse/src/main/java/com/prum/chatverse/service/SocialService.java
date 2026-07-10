package com.prum.chatverse.service;

import org.springframework.stereotype.Service;

import com.prum.chatverse.repository.DislikeRepository;
import com.prum.chatverse.repository.FollowRepository;
import com.prum.chatverse.repository.LikeRepository;

@Service
public class SocialService {
    private final FollowRepository followRepository;
    private final LikeRepository likeRepository;
    private final DislikeRepository dislikeRepository;

    public SocialService(FollowRepository followRepository, LikeRepository likeRepository, DislikeRepository dislikeRepository){
        this.dislikeRepository = dislikeRepository;
        this.likeRepository = likeRepository;
        this.followRepository = followRepository;
    }
}
