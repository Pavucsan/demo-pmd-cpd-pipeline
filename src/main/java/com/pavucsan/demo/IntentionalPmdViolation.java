package com.pavucsan.demo;

public final class IntentionalPmdViolation {
    private void neverCalled() {
        System.out.println("PMD should report this unused private method");
    }
}

