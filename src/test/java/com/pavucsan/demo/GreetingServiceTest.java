package com.pavucsan.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class GreetingServiceTest {

    private final GreetingService service = new GreetingService();

    @Test
    void greetsAName() {
        assertEquals("Hello, Ada!", service.greet(" Ada "));
    }

    @Test
    void usesFallbackForBlankInput() {
        assertEquals("Hello, world!", service.greet(" "));
    }
}

