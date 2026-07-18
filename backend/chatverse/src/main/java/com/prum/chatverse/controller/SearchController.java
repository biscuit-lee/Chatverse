package com.prum.chatverse.controller;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.prum.chatverse.dto.PostResponse;
import com.prum.chatverse.dto.UserInfoResponse;
import com.prum.chatverse.service.SearchService;

@RestController
@RequestMapping("/api/search")
public class SearchController {
    private final SearchService searchService;

    public SearchController(SearchService searchService){
        this.searchService = searchService;
    }

    @GetMapping("/posts")
    public Page<PostResponse> searchPost(@RequestParam String q, Pageable page){
        return searchService.searchPost(q, page);
    }

    @GetMapping("/users")
    public Page<UserInfoResponse> searchUser(@RequestParam String q, Pageable pageable){
        return searchService.searchUser(q, pageable);
    }
}
