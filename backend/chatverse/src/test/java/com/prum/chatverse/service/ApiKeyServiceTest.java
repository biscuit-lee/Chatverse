package com.prum.chatverse.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.prum.chatverse.dto.ApiKeyResponse;
import com.prum.chatverse.entity.ApiKey;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.ApiKeyRepository;

@ExtendWith(MockitoExtension.class)
class ApiKeyServiceTest {

    @Mock
    private ApiKeyRepository apiKeyRepository;

    @InjectMocks
    private ApiKeyService apiKeyService;

    private String sha256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }


    @Test
    void generateRawApiKey_returnsKeyWithCorrectPrefix() {
        User user = new User();
        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(new ApiKey());

        String rawKey = apiKeyService.generateRawApiKey(user, "test-key");

        assertTrue(rawKey.startsWith("cv_live_"));
    }

    @Test
    void generateRawApiKey_savesEntityOnce() {
        User user = new User();
        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(new ApiKey());

        apiKeyService.generateRawApiKey(user, "test-key");

        verify(apiKeyRepository, times(1)).save(any(ApiKey.class));
    }

    @Test
    void generateRawApiKey_savesWithHashedKey() {
        User user = new User();
        ArgumentCaptor<ApiKey> captor = ArgumentCaptor.forClass(ApiKey.class);
        when(apiKeyRepository.save(captor.capture())).thenReturn(new ApiKey());

        String rawKey = apiKeyService.generateRawApiKey(user, "test-key");

        ApiKey saved = captor.getValue();
        assertEquals(sha256(rawKey), saved.getHashedApiKey());
    }

    @Test
    void generateRawApiKey_savesWithActiveTrue() {
        User user = new User();
        ArgumentCaptor<ApiKey> captor = ArgumentCaptor.forClass(ApiKey.class);
        when(apiKeyRepository.save(captor.capture())).thenReturn(new ApiKey());

        apiKeyService.generateRawApiKey(user, "test-key");

        assertTrue(captor.getValue().isActive());
    }

    @Test
    void generateRawApiKey_setsKeyOwner() {
        User user = new User();
        user.setUsername("bob");
        ArgumentCaptor<ApiKey> captor = ArgumentCaptor.forClass(ApiKey.class);
        when(apiKeyRepository.save(captor.capture())).thenReturn(new ApiKey());

        apiKeyService.generateRawApiKey(user, "test-key");

        assertSame(user, captor.getValue().getKeyOwner());
    }

    @Test
    void generateRawApiKey_setsKeyName() {
        User user = new User();
        ArgumentCaptor<ApiKey> captor = ArgumentCaptor.forClass(ApiKey.class);
        when(apiKeyRepository.save(captor.capture())).thenReturn(new ApiKey());

        apiKeyService.generateRawApiKey(user, "my-api-key");

        assertEquals("my-api-key", captor.getValue().getKeyName());
    }

    @Test
    void generateRawApiKey_generatesDifferentKeysEachCall() {
        User user = new User();
        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(new ApiKey());

        String key1 = apiKeyService.generateRawApiKey(user, "key-1");
        String key2 = apiKeyService.generateRawApiKey(user, "key-2");

        assertNotEquals(key1, key2);
    }

    @Test
    void generateRawApiKey_generatedKeyFormatIsCorrect() {
        User user = new User();
        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(new ApiKey());

        String rawKey = apiKeyService.generateRawApiKey(user, "test-key");

        String prefix = "cv_live_";
        assertTrue(rawKey.startsWith(prefix));
        String encodedPart = rawKey.substring(prefix.length());
        assertEquals(43, encodedPart.length());
        assertTrue(encodedPart.matches("^[A-Za-z0-9_-]+$"));
    }


    @Test
    void validateApiKey_withValidKey_returnsOwner() {
        User owner = new User();
        owner.setId(1L);
        owner.setUsername("bob");
        ApiKey apiKey = new ApiKey();
        apiKey.setKeyOwner(owner);

        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(anyString()))
                .thenReturn(Optional.of(apiKey));

        Optional<User> result = apiKeyService.validateApiKey("cv_live_someValidKey");

        assertTrue(result.isPresent());
        assertSame(owner, result.get());
    }

    @Test
    void validateApiKey_withInvalidKey_returnsEmpty() {
        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(anyString()))
                .thenReturn(Optional.empty());

        Optional<User> result = apiKeyService.validateApiKey("cv_live_invalidKey");

        assertFalse(result.isPresent());
    }

    @Test
    void validateApiKey_hashesTheInputBeforeLookup() {
        String rawKey = "cv_live_testInputKey";
        String expectedHash = sha256(rawKey);

        ArgumentCaptor<String> captor = ArgumentCaptor.forClass(String.class);
        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(captor.capture()))
                .thenReturn(Optional.empty());

        apiKeyService.validateApiKey(rawKey);

        assertEquals(expectedHash, captor.getValue());
    }

    @Test
    void validateApiKey_inactiveKey_returnsEmpty() {
        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(anyString()))
                .thenReturn(Optional.empty());

        Optional<User> result = apiKeyService.validateApiKey("cv_live_inactiveKey");

        assertFalse(result.isPresent());
    }

    @Test
    void generateApiKey_returnsApiKeyResponse() {
        User user = new User();
        user.setId(1L);
        user.setUsername("bob");

        ApiKey savedApiKey = new ApiKey();
        savedApiKey.setId(42L);
        savedApiKey.setKeyName("my-key");
        savedApiKey.setActive(true);

        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(savedApiKey);
        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(anyString()))
                .thenReturn(Optional.of(savedApiKey));

        ApiKeyResponse response = apiKeyService.generateApiKey(user, "my-key");

        assertNotNull(response);
        assertEquals(42L, response.id());
        assertEquals("my-key", response.keyName());
        assertTrue(response.isActive());
    }

    @Test
    void generateApiKey_responseContainsRawKey() {
        User user = new User();

        ApiKey savedApiKey = new ApiKey();
        savedApiKey.setId(1L);
        savedApiKey.setKeyName("my-key");
        savedApiKey.setActive(true);

        when(apiKeyRepository.save(any(ApiKey.class))).thenReturn(savedApiKey);
        when(apiKeyRepository.findByHashedApiKeyAndIsActiveTrue(anyString()))
                .thenReturn(Optional.of(savedApiKey));

        ApiKeyResponse response = apiKeyService.generateApiKey(user, "my-key");

        assertNotNull(response.rawApiKey());
        assertTrue(response.rawApiKey().startsWith("cv_live_"));
    }
}
