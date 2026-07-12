package com.prum.chatverse.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.prum.chatverse.entity.Comment;

public interface CommentRepository extends JpaRepository<Comment,Long>{
    List<Comment> findByPostId(Long id);
} 

