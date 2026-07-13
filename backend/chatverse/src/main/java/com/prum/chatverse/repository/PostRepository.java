package com.prum.chatverse.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import com.prum.chatverse.entity.Post;


public interface PostRepository extends JpaRepository<Post, Long> {
    Page<Post> findByAuthorId(Long id, Pageable pageable);
}
