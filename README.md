# Cursor Learn - FastAPI Name Processing Service

A simple FastAPI application that processes names and counts letter occurrences.

## Features

- RESTful API endpoints for name processing
- Letter frequency analysis
- Input validation using Pydantic models
- Comprehensive test coverage

## API Flow Diagram

```mermaid
flowchart TD
    A[Client]
    B[Root Endpoint\n GET /]
    C[Name Endpoint\n POST /name]
    D[Pydantic Validator]
    E[Letter Counter]
    F[Response Generator]
    G[Error Handler]

    A --> |Request| B
    A --> |Request| C
    C --> |Validate| D
    D --> |Valid| E
    E --> |Process| F
    F --> |Response| A
    D --> |Invalid| G
    G --> |Error| A

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#000;
    classDef client fill:#FFD700,stroke:#333,stroke-width:2px,color:#000;
    classDef endpoint fill:#98FB98,stroke:#333,stroke-width:2px,color:#000;
    classDef process fill:#87CEEB,stroke:#333,stroke-width:2px,color:#000;
    classDef error fill:#FFB6C1,stroke:#333,stroke-width:2px,color:#000;

    class A client;
    class B,C endpoint;
    class D,E,F process;
    class G error;
```

## Installation

1. Ensure Python 3.13+ is installed
2. Install dependencies:





