package com.prum.chatverse.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.prum.chatverse.dto.LoginRequest;
import com.prum.chatverse.dto.LoginResponse;
import com.prum.chatverse.dto.RegisterRequest;
import com.prum.chatverse.dto.RegisterResponse;
import com.prum.chatverse.entity.User;
import com.prum.chatverse.repository.UserRepository;

@ExtendWith(MockitoExtension.class)
public class AuthServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtService jwtService;

    @InjectMocks
    private AuthService authService;

    @Test
    void whenSignUp_shouldSaveAndReturnUser(){

        String fakeUsername = "bob";
        String fakePassword = "password123";
        RegisterRequest request = new RegisterRequest(fakeUsername, fakePassword);
        
        User fakeSavedUser = new User();
        fakeSavedUser.setId(1L);
        fakeSavedUser.setUsername(fakeUsername);
        fakeSavedUser.setPassword("encodedPassword");

        when(userRepository.existsByUsername(fakeUsername)).thenReturn(false);
        when(passwordEncoder.encode(fakePassword)).thenReturn("encodedPassword");
        when(userRepository.save(any(User.class))).thenReturn(fakeSavedUser);

        RegisterResponse response = authService.signUp(request);

        assertNotNull(response);
        assertEquals(fakeSavedUser.getId(), response.id());
        assertEquals(fakeSavedUser.getUsername(), response.username());
        
        verify(userRepository).existsByUsername(fakeUsername);
        verify(passwordEncoder).encode(fakePassword);
        verify(userRepository).save(any(User.class));
    }    

    @Test
    void whenSignUpAndUsernameTaken_shouldThrowError(){

        String fakeUsername = "bob";
        String fakePassword = "password123";
        RegisterRequest request = new RegisterRequest(fakeUsername, fakePassword);

        when(userRepository.existsByUsername(fakeUsername)).thenReturn(true);

        assertThrows(RuntimeException.class, () -> authService.signUp(request));
        
        verify(userRepository).existsByUsername(fakeUsername);
    }    


    @Test
    void whenLogin_shouldSaveAndReturnUserAndToken(){

        String fakeUsername = "bob";
        String fakePassword = "password123";
        String fakeToken = "supersecrettoken";
        LoginRequest request = new LoginRequest(fakeUsername, fakePassword);
        
        User fakeSavedUser = new User();
        fakeSavedUser.setId(1L);
        fakeSavedUser.setUsername(fakeUsername);
        fakeSavedUser.setPassword("encodedPassword");

        when(userRepository.existsByUsername(fakeUsername)).thenReturn(true);
        when(userRepository.findByUsername(fakeUsername)).thenReturn(Optional.of(fakeSavedUser));
        when(passwordEncoder.matches(fakePassword,fakeSavedUser.getPassword())).thenReturn(true);
        when(jwtService.generateToken(fakeUsername)).thenReturn(fakeToken);
        
        LoginResponse response = authService.login(request);

        assertNotNull(response);
        assertEquals(fakeSavedUser.getId(), response.id());
        assertEquals(fakeSavedUser.getUsername(), response.username());
        assertEquals(fakeToken, response.token());
        
        verify(userRepository).existsByUsername(fakeUsername);
        verify(userRepository).findByUsername(fakeUsername);
        verify(passwordEncoder).matches(fakePassword, fakeSavedUser.getPassword());
        verify(jwtService).generateToken(fakeUsername);
    }    
    
    @Test
    void whenLoginAndUserNotExist_shouldThrowError(){
        String fakeUsername = "bob";
        String fakePassword = "password123";
        LoginRequest request = new LoginRequest(fakeUsername, fakePassword);

        when(userRepository.existsByUsername(fakeUsername)).thenReturn(false);

        assertThrows(RuntimeException.class, () -> authService.login(request));
        
        verify(userRepository).existsByUsername(fakeUsername);
    
    }

    @Test
    void whenLoginAndPasswordNotMatch_shouldThrowError(){
        
        String fakeUsername = "bob";
        String fakePassword = "password123";
        LoginRequest request = new LoginRequest(fakeUsername, fakePassword);
        
        User fakeSavedUser = new User();
        fakeSavedUser.setId(1L);
        fakeSavedUser.setUsername(fakeUsername);
        fakeSavedUser.setPassword("encodedPassword");

        when(userRepository.existsByUsername(fakeUsername)).thenReturn(true);
        when(userRepository.findByUsername(fakeUsername)).thenReturn(Optional.of(fakeSavedUser));
        when(passwordEncoder.matches(fakePassword,fakeSavedUser.getPassword())).thenReturn(false);
        
        assertThrows(RuntimeException.class, () -> authService.login(request));  

        verify(userRepository).existsByUsername(fakeUsername);
        verify(userRepository).findByUsername(fakeUsername);
        verify(passwordEncoder).matches(fakePassword, fakeSavedUser.getPassword());
    }
    

}
