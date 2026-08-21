package com.prum.chatverse.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.prum.chatverse.entity.ApiKey;

public interface ApiKeyRepository extends JpaRepository<ApiKey,Long> {

    @Query("""
        SELECT ak
        FROM ApiKey ak
        JOIN FETCH ak.keyOwner
        WHERE ak.hashedApiKey = :hashedKey
        AND ak.isActive = true
    """)
    Optional<ApiKey> findByHashedApiKeyAndIsActiveTrueWithOwner(
            @Param("hashedKey") String hashedKey
    );
      
}
