package com.prum.chatverse.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.prum.chatverse.entity.ApiKey;

public interface ApiKeyRepository extends JpaRepository<ApiKey,Long> {

    Optional<ApiKey> findByHashedApiKeyAndIsActiveTrue(String hashedApiKey);

      
}
