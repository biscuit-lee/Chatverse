package com.prum.chatverse.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.prum.chatverse.entity.Follow;

public interface FollowRepository extends JpaRepository<Follow,Long>{
    
} 
