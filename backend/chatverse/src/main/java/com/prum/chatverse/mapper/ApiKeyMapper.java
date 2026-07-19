package com.prum.chatverse.mapper;

import com.prum.chatverse.dto.ApiKeyResponse;
import com.prum.chatverse.entity.ApiKey;

public class ApiKeyMapper {
    
    public static ApiKeyResponse mapApiKeyResponse(ApiKey apikey, String rawApiKey){
        return new ApiKeyResponse(apikey.getId(), apikey.getKeyName(),rawApiKey , apikey.isActive());
    }
}
