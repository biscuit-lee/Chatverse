package com.prum.chatverse.service;

import java.security.Key;
import java.util.Date;

import org.springframework.stereotype.Service;

import io.jsonwebtoken.Jwt;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

@Service
public class JwtService {
    private final Key secretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);
    private final long expirationMs = 1000 * 60 * 60;  //1h

    public String generateToken(String username){
        return Jwts.builder()
        .setSubject(username)   
        .setIssuedAt(new Date()) 
        .setExpiration(new Date(System.currentTimeMillis() + expirationMs))
        .signWith(secretKey)
        .compact(); // Build final key
    }

    public String extractUsername(String token){
        return Jwts.parserBuilder()
                .setSigningKey(secretKey)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    public boolean isTokenValid(String token){
        try{Jwts.parserBuilder()
                .setSigningKey(secretKey)
                .build()
                .parseClaimsJws(token);
                
            return true;
        }catch (JwtException e){
            return false;
        }
        
    }
}
