package com.prum.chatverse.service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.prum.chatverse.entity.ApiKey;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.ApiKeyRepository;

@Service
public class ApiKeyService {
    private final ApiKeyRepository apiKeyRepository;

    public ApiKeyService(ApiKeyRepository apiKeyRepository){
        this.apiKeyRepository = apiKeyRepository;
    }

    public String generateApiKey(User apiKeyOwner){
        // Create cryptographically secure random bytes
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        
        // Format it nicely with a prefix so it looks like a standard key
        String rawKey = "cv_live_" + Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);

        String hashedKey = hashKey(rawKey);

        ApiKey apiKey = new ApiKey();
        apiKey.setHashedApiKey(hashedKey);
        apiKey.setKeyOwner(apiKeyOwner);
        apiKey.setActive(true);

        apiKeyRepository.save(apiKey);
        return rawKey;
    }

    public Optional<User> validateApiKey(String rawApiKey){
        String hashedKey = hashKey(rawApiKey);
        
        Optional<User> keyOwner = apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(hashedKey).map(apiKey -> apiKey.getKeyOwner());
        
        return keyOwner;
        
    }
    
    private String hashKey(String rawKey) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(rawKey.getBytes(StandardCharsets.UTF_8));
            
            // Convert byte array into a clean hex string
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not found!", e);
        }
    }
}
