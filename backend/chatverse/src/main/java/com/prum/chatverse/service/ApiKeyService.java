package com.prum.chatverse.service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.prum.chatverse.dto.ApiKeyResponse;
import com.prum.chatverse.entity.ApiKey;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.mapper.ApiKeyMapper;
import com.prum.chatverse.repository.ApiKeyRepository;

@Service
public class ApiKeyService {
    private final ApiKeyRepository apiKeyRepository;

    public ApiKeyService(ApiKeyRepository apiKeyRepository){
        this.apiKeyRepository = apiKeyRepository;
    }

    public String generateRawApiKey() {
        SecureRandom random = new SecureRandom();

        byte[] bytes = new byte[32];
        random.nextBytes(bytes);

        return "cv_live_" +
            Base64.getUrlEncoder()
            .withoutPadding()
            .encodeToString(bytes);
    }

    public Optional<User> validateApiKey(String rawApiKey){
        String hashedKey = hashKey(rawApiKey);
        
        Optional<User> keyOwner = apiKeyRepository.findByHashedApiKeyAndIsActiveTrueWithOwner(hashedKey).map(apiKey -> apiKey.getKeyOwner());
        
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

        public ApiKeyResponse generateApiKey(User user, String keyName) {

        String rawKey = generateRawApiKey();

        ApiKey apiKey = new ApiKey();
        apiKey.setKeyOwner(user);
        apiKey.setKeyName(keyName);
        apiKey.setHashedApiKey(hashKey(rawKey));
        apiKey.setActive(true);

        ApiKey savedKey = apiKeyRepository.save(apiKey);

        return new ApiKeyResponse(
            savedKey.getId(),
            savedKey.getKeyName(),
            rawKey,
            savedKey.isActive()
        );
    }

}
