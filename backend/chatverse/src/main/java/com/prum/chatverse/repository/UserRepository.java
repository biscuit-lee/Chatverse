package com.prum.chatverse.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import com.prum.chatverse.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    boolean existsByUsername(String username);
}
