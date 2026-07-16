package com.prum.chatverse.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.prum.chatverse.entity.Dislike;

import com.prum.chatverse.entity.User;
import com.prum.chatverse.entity.Post;

public interface DislikeRepository extends JpaRepository<Dislike,Long>{
    boolean existsByDislikerAndPost(User disliker, Post post);
    
} 
