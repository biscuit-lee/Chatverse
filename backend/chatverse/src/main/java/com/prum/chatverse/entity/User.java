package com.prum.chatverse.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;
    
    @Column(nullable = true) // Allow null for bots
    private String password;

    private LocalDateTime createdAt;

    private String profilePictureUrl;
    
    String bio;

    int followers = 0;

    int following = 0;
    @OneToMany(mappedBy = "author")
    private List<Post> posts;

    @OneToMany(mappedBy = "author")
    private List<Comment> comments;

    @Enumerated(EnumType.STRING)
    private UserType userType;

    @PrePersist
    private void onCreate(){
        this.createdAt = LocalDateTime.now();
    }
}
