package com.prum.chatverse.entity;
import java.time.LocalDateTime;
import java.util.List;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.*;
import lombok.Setter;

import com.prum.chatverse.entity.User;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String content;
    
    private LocalDateTime createdAt;

    private int likes = 0;

    private int dislikes = 0;

    private int commentsCount = 0;
    // Relation with its comments
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments;

    // Relation with the author
    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @PrePersist
    private void onCreate() {
        this.createdAt = LocalDateTime.now();

    }
}