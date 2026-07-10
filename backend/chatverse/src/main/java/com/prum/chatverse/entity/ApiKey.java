package com.prum.chatverse.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Setter
@Getter
@NoArgsConstructor
public class ApiKey {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String hashedApiKey;

    @ManyToOne(fetch = FetchType.LAZY)
    private User keyOwner;

    private LocalDateTime createdAt;

    private boolean isActive = true;
    @PrePersist
    private void onCreate(){
        this.createdAt = LocalDateTime.now();
    }

}
