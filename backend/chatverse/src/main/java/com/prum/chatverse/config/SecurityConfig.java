package com.prum.chatverse.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import com.prum.chatverse.security.ApiKeyFilter;
import com.prum.chatverse.security.JwtAuthFilter;

@Configuration
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;
    private final ApiKeyFilter apiKeyFilter;
    public SecurityConfig(JwtAuthFilter jwtAuthFilter, ApiKeyFilter apiKeyFilter){
        this.jwtAuthFilter = jwtAuthFilter;
        this.apiKeyFilter = apiKeyFilter;
    }


    @Bean
    public PasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception{
        http.csrf(csrf -> csrf.disable())
            .formLogin(form -> form.disable())
            .httpBasic(httpBasic -> httpBasic.disable())
        // Whitelist the login and register endpoints
        .authorizeHttpRequests(auth -> auth.requestMatchers(
            "/api/users/login",
            "/api/users/register"
        ).permitAll().anyRequest().authenticated()
    ).addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
    .addFilterAfter(apiKeyFilter, JwtAuthFilter.class);

    return http.build();
    }
}
