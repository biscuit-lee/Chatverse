package com.prum.chatverse.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.prum.chatverse.entity.Post;


public interface PostRepository extends JpaRepository<Post, Long> {
    Page<Post> findByAuthorId(Long id, Pageable pageable);
    Page<Post> findAllByOrderByCreatedAtDesc(Pageable pageable);

    @Query("""
            SELECT p from Post p ORDER BY (p.likes - p.dislikes) DESC
            """)
    Page<Post> findAllByScoreDesc(Pageable pageable);
    
    // plainto_tsquery turns search query (Ex. "funny cat ") to postgres query (eg. "funny"&"cat") 
    // then "@@" compares that to the tsvector (the document we stored which is search_vector (eg. "funny" "cat" "video"))

    @Query
    (value = """
    SELECT * FROM post 
    WHERE search_vector @@ plainto_tsquery('english', :query)             
    ORDER BY ts_rank(search_vector, plainto_tsquery('english', :query)) DESC         
    """,
    countQuery = """
            SELECT COUNT(*) from post where search_vector @@ plainto_tsquery('english', :query)
            """,
    nativeQuery = true
    )
    Page<Post> search(@Param("query") String query, Pageable pageable);
}
