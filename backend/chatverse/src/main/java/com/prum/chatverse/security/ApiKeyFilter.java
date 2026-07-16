package com.prum.chatverse.security;

import java.io.IOException;
import java.util.List;
import java.util.Optional;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.prum.chatverse.entity.User;
import com.prum.chatverse.service.ApiKeyService;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component
public class ApiKeyFilter extends OncePerRequestFilter {
    private final ApiKeyService apiKeyService;        

    public ApiKeyFilter(ApiKeyService apiKeyService){
        this.apiKeyService = apiKeyService;
    }

    @Override
    protected void doFilterInternal(
        HttpServletRequest request,
        HttpServletResponse response,
        FilterChain filterChain
    ) throws ServletException, IOException
    {
        
        String apiKey = request.getHeader("X-API-KEY");

        if (apiKey == null || apiKey.isBlank()){
            filterChain.doFilter(request, response);
            return;
        }

        Optional<User> apiKeyOwnerOption = apiKeyService.validateApiKey(apiKey);

        if (apiKeyOwnerOption.isPresent()) {
            User apiKeyOwner = apiKeyOwnerOption.get();
            
            UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(apiKeyOwner.getUsername(),null,List.of());
            
            SecurityContextHolder.getContext().setAuthentication(auth);

        }

        filterChain.doFilter(request, response);
    }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        return "OPTIONS".equalsIgnoreCase(request.getMethod());
    }
}
