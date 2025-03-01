# Cursor Learn - FastAPI Name Processing Service

A simple FastAPI application that processes names and counts letter occurrences.

## Features

- RESTful API endpoints for name processing
- Letter frequency analysis
- Input validation using Pydantic models
- Comprehensive test coverage

## API Flow Diagram

```mermaid
graph TD
    A[Client] -->|GET /| B[Root Endpoint]
    A -->|POST /name| C[Name Endpoint]
    C -->|Input| D[Name Payload Validation]
    D -->|Valid| E[Letter Counter Utility]
    E -->|Process| F[Generate Response]
    F -->|JSON Response| A
    D -->|Invalid| G[422 Validation Error]
    G -->|Error Response| A
    
    style B fill:#90EE90
    style C fill:#90EE90
    style D fill:#FFB6C1
    style E fill:#ADD8E6
    style F fill:#DDA0DD
    style G fill:#FF6B6B
```

## Installation

1. Ensure Python 3.13+ is installed
2. Install dependencies:





