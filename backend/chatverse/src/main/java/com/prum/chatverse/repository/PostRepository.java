package com.prum.chatverse.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.prum.chatverse.entity.Post;


public interface PostRepository extends JpaRepository<Post, Long> {
    Page<Post> findByAuthorId(Long id, Pageable pageable);
    Page<Post> findAllByOrderByCreatedAtDesc(Pageable pageable);

    @Query("""
            SELECT p from Post p ORDER BY (p.likes - p.dislikes) DESC
            """)
    Page<Post> findAllByScoreDesc(Pageable pageable);
}
