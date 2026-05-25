package com.example.springvuebackend.api;

import java.time.OffsetDateTime;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public HelloResponse hello() {
        return new HelloResponse("Spring Boot 2.7 API is running.", OffsetDateTime.now());
    }

    public record HelloResponse(String message, OffsetDateTime serverTime) {
    }
}

