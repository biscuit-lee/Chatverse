package com.prum.chatverse.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.prum.chatverse.entity.*;

public interface LikeRepository extends JpaRepository<Like,Long>{
    
    boolean existsByLikerAndPost(User liker, Post targetPost);
} 
