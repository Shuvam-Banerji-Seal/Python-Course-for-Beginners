# Ollama Architecture and System Diagrams

This document provides visual explanations of Ollama's architecture, components, and workflows using Mermaid diagrams.

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Model Management Workflow](#model-management-workflow)
3. [Request Processing Flow](#request-processing-flow)
4. [API Interaction Patterns](#api-interaction-patterns)
5. [Model Storage Structure](#model-storage-structure)
6. [Client-Server Communication](#client-server-communication)
7. [GPU Acceleration Flow](#gpu-acceleration-flow)
8. [Error Handling Flow](#error-handling-flow)

## High-Level Architecture

The following diagram shows the overall architecture of Ollama and how its components interact:

```mermaid
graph TB
    subgraph "Client Applications"
        CLI[Ollama CLI]
        API[REST API Clients]
        PY[Python Scripts]
        WEB[Web Applications]
    end
    
    subgraph "Ollama Server"
        HTTP[HTTP Server<br/>Port 11434]
        ROUTER[Request Router]
        AUTH[Authentication<br/>(Optional)]
        
        subgraph "Core Engine"
            LOAD[Model Loader]
            INFER[Inference Engine]
            CACHE[Response Cache]
            QUEUE[Request Queue]
        end
        
        subgraph "Model Management"
            REGISTRY[Model Registry]
            DOWNLOAD[Download Manager]
            STORAGE[Model Storage]
            VALIDATE[Model Validator]
        end
    end
    
    subgraph "System Resources"
        CPU[CPU Cores]
        RAM[System RAM]
        GPU[GPU Memory<br/>(Optional)]
        DISK[Disk Storage]
    end
    
    subgraph "External Services"
        HF[Hugging Face Hub]
        OLLAMA_REG[Ollama Registry]
        CUSTOM[Custom Registries]
    end
    
    CLI --> HTTP
    API --> HTTP
    PY --> HTTP
    WEB --> HTTP
    
    HTTP --> ROUTER
    ROUTER --> AUTH
    AUTH --> LOAD
    AUTH --> INFER
    AUTH --> REGISTRY
    
    LOAD --> CACHE
    INFER --> CACHE
    LOAD --> QUEUE
    INFER --> QUEUE
    
    REGISTRY --> DOWNLOAD
    DOWNLOAD --> STORAGE
    STORAGE --> VALIDATE
    
    LOAD --> CPU
    LOAD --> RAM
    INFER --> CPU
    INFER --> RAM
    INFER --> GPU
    STORAGE --> DISK
    
    DOWNLOAD --> HF
    DOWNLOAD --> OLLAMA_REG
    DOWNLOAD --> CUSTOM
```

### Architecture Components Explained

**Client Layer:**
- **Ollama CLI**: Command-line interface for direct interaction
- **REST API Clients**: Applications using HTTP API endpoints
- **Python Scripts**: Custom scripts using requests or ollama library
- **Web Applications**: Browser-based interfaces

**Server Layer:**
- **HTTP Server**: Handles incoming requests on port 11434
- **Request Router**: Routes requests to appropriate handlers
- **Authentication**: Optional security layer for access control

**Core Engine:**
- **Model Loader**: Loads models into memory for inference
- **Inference Engine**: Processes prompts and generates responses
- **Response Cache**: Caches responses for improved performance
- **Request Queue**: Manages concurrent requests

**Model Management:**
- **Model Registry**: Tracks available and installed models
- **Download Manager**: Handles model downloads with progress tracking
- **Model Storage**: Manages local model files and metadata
- **Model Validator**: Verifies model integrity and compatibility

## Model Management Workflow

This diagram illustrates how models are discovered, downloaded, and managed:

```mermaid
sequenceDiagram
    participant User
    participant CLI as Ollama CLI
    participant Server as Ollama Server
    participant Registry as Model Registry
    participant Storage as Local Storage
    participant Remote as Remote Registry
    
    User->>CLI: ollama pull llama2:7b
    CLI->>Server: POST /api/pull
    Server->>Registry: Check if model exists locally
    
    alt Model not found locally
        Registry->>Remote: Query model availability
        Remote-->>Registry: Model metadata
        Registry->>Storage: Check available space
        
        alt Sufficient space
            Server->>Remote: Download model chunks
            Remote-->>Server: Model data (streaming)
            Server->>Storage: Save model chunks
            Server-->>CLI: Progress updates
            CLI-->>User: Download progress
            
            Server->>Registry: Register model locally
            Server-->>CLI: Download complete
            CLI-->>User: Model ready
        else Insufficient space
            Server-->>CLI: Error: Not enough space
            CLI-->>User: Error message
        end
    else Model exists locally
        Server-->>CLI: Model already available
        CLI-->>User: Model ready
    end
```

### Model Management States

```mermaid
stateDiagram-v2
    [*] --> Available: Model in registry
    Available --> Downloading: User requests pull
    Downloading --> Downloaded: Download complete
    Downloading --> Failed: Download error
    Downloaded --> Loading: User runs model
    Loading --> Running: Model loaded successfully
    Loading --> Failed: Load error
    Running --> Idle: No active requests
    Idle --> Running: New request
    Running --> Unloaded: Memory pressure
    Unloaded --> Available: Model removed from memory
    Downloaded --> Removed: User deletes model
    Failed --> Available: Retry or fix issue
    Removed --> [*]
```

## Request Processing Flow

This diagram shows how requests are processed from client to response:

```mermaid
flowchart TD
    START([Client Request]) --> VALIDATE{Valid Request?}
    
    VALIDATE -->|No| ERROR_RESP[Return Error Response]
    VALIDATE -->|Yes| CHECK_MODEL{Model Available?}
    
    CHECK_MODEL -->|No| LOAD_MODEL[Load Model into Memory]
    CHECK_MODEL -->|Yes| CHECK_QUEUE{Queue Available?}
    
    LOAD_MODEL --> MODEL_READY{Model Loaded?}
    MODEL_READY -->|No| ERROR_RESP
    MODEL_READY -->|Yes| CHECK_QUEUE
    
    CHECK_QUEUE -->|No| QUEUE_REQUEST[Add to Queue]
    CHECK_QUEUE -->|Yes| PROCESS_REQUEST[Process Request]
    
    QUEUE_REQUEST --> WAIT[Wait for Queue Slot]
    WAIT --> PROCESS_REQUEST
    
    PROCESS_REQUEST --> TOKENIZE[Tokenize Input]
    TOKENIZE --> INFERENCE[Run Inference]
    INFERENCE --> GENERATE[Generate Tokens]
    
    GENERATE --> STREAM_CHECK{Streaming?}
    STREAM_CHECK -->|Yes| STREAM_TOKEN[Send Token]
    STREAM_CHECK -->|No| COLLECT_TOKENS[Collect All Tokens]
    
    STREAM_TOKEN --> MORE_TOKENS{More Tokens?}
    MORE_TOKENS -->|Yes| GENERATE
    MORE_TOKENS -->|No| COMPLETE[Mark Complete]
    
    COLLECT_TOKENS --> COMPLETE
    COMPLETE --> CLEANUP[Cleanup Resources]
    CLEANUP --> RESPONSE[Send Final Response]
    
    ERROR_RESP --> END([End])
    RESPONSE --> END
```

## API Interaction Patterns

### Synchronous Generation Pattern

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Model
    
    Client->>Server: POST /api/generate
    Note over Client,Server: {"model": "llama2:7b", "prompt": "Hello", "stream": false}
    
    Server->>Model: Load model (if needed)
    Model-->>Server: Model ready
    
    Server->>Model: Process prompt
    Model-->>Server: Generate complete response
    
    Server-->>Client: Full response
    Note over Client,Server: {"response": "Hello! How can I help?", "done": true}
```

### Streaming Generation Pattern

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Model
    
    Client->>Server: POST /api/generate
    Note over Client,Server: {"model": "llama2:7b", "prompt": "Hello", "stream": true}
    
    Server->>Model: Load model (if needed)
    Model-->>Server: Model ready
    
    Server->>Model: Start generation
    
    loop For each token
        Model-->>Server: Generate token
        Server-->>Client: Stream token chunk
        Note over Client,Server: {"response": "Hello", "done": false}
    end
    
    Model-->>Server: Generation complete
    Server-->>Client: Final chunk
    Note over Client,Server: {"response": "", "done": true}
```

### Chat Conversation Pattern

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Model
    participant Context as Context Manager
    
    Client->>Server: POST /api/chat
    Note over Client,Server: {"model": "llama2:7b", "messages": [...]}
    
    Server->>Context: Build conversation context
    Context-->>Server: Formatted prompt
    
    Server->>Model: Load model (if needed)
    Model-->>Server: Model ready
    
    Server->>Model: Process conversation
    Model-->>Server: Generate response
    
    Server->>Context: Update conversation history
    Server-->>Client: Assistant response
    Note over Client,Server: {"message": {"role": "assistant", "content": "..."}}
```

## Model Storage Structure

This diagram shows how models are organized in the local file system:

```mermaid
graph TD
    subgraph "Ollama Models Directory (~/.ollama/models)"
        MANIFESTS[manifests/]
        BLOBS[blobs/]
        
        subgraph "Manifests"
            MANIFEST1[registry.ollama.ai/library/llama2/7b]
            MANIFEST2[registry.ollama.ai/library/mistral/7b]
            MANIFEST3[custom/my-model/latest]
        end
        
        subgraph "Blobs (Content-Addressed)"
            BLOB1[sha256-abc123.../]
            BLOB2[sha256-def456.../]
            BLOB3[sha256-ghi789.../]
            
            subgraph "Blob Contents"
                MODEL_FILE[model.bin]
                TOKENIZER[tokenizer.json]
                CONFIG[config.json]
                TEMPLATE[template.txt]
            end
        end
    end
    
    MANIFEST1 --> BLOB1
    MANIFEST2 --> BLOB2
    MANIFEST3 --> BLOB3
    
    BLOB1 --> MODEL_FILE
    BLOB1 --> TOKENIZER
    BLOB1 --> CONFIG
    BLOB1 --> TEMPLATE
```

### Storage Organization Explained

**Manifests Directory:**
- Contains metadata for each model
- Organized by registry/namespace/model/tag structure
- Points to actual content blobs via SHA256 hashes

**Blobs Directory:**
- Content-addressed storage using SHA256 hashes
- Enables deduplication across models
- Contains actual model files, tokenizers, and configurations

**Benefits of this Structure:**
- **Deduplication**: Shared components between models stored once
- **Integrity**: Content-addressed storage ensures data integrity
- **Efficiency**: Only download changed components during updates
- **Organization**: Clear separation between metadata and content

## Client-Server Communication

### HTTP API Endpoints

```mermaid
graph LR
    subgraph "Client Operations"
        LIST[List Models]
        PULL[Pull Model]
        PUSH[Push Model]
        DELETE[Delete Model]
        GENERATE[Generate Text]
        CHAT[Chat]
        EMBED[Embeddings]
    end
    
    subgraph "API Endpoints"
        API_TAGS[GET /api/tags]
        API_PULL[POST /api/pull]
        API_PUSH[POST /api/push]
        API_DELETE[DELETE /api/delete]
        API_GENERATE[POST /api/generate]
        API_CHAT[POST /api/chat]
        API_EMBED[POST /api/embeddings]
    end
    
    LIST --> API_TAGS
    PULL --> API_PULL
    PUSH --> API_PUSH
    DELETE --> API_DELETE
    GENERATE --> API_GENERATE
    CHAT --> API_CHAT
    EMBED --> API_EMBED
```

### Request/Response Flow

```mermaid
flowchart LR
    subgraph "Request Processing"
        REQ[HTTP Request] --> PARSE[Parse JSON]
        PARSE --> VALIDATE[Validate Parameters]
        VALIDATE --> ROUTE[Route to Handler]
    end
    
    subgraph "Response Generation"
        PROCESS[Process Request] --> FORMAT[Format Response]
        FORMAT --> SEND[Send HTTP Response]
    end
    
    ROUTE --> PROCESS
```

## GPU Acceleration Flow

This diagram shows how GPU acceleration is utilized when available:

```mermaid
flowchart TD
    START[Model Loading Request] --> CHECK_GPU{GPU Available?}
    
    CHECK_GPU -->|No| CPU_LOAD[Load Model on CPU]
    CHECK_GPU -->|Yes| GPU_CHECK{GPU Memory Sufficient?}
    
    GPU_CHECK -->|No| CPU_LOAD
    GPU_CHECK -->|Yes| GPU_LOAD[Load Model on GPU]
    
    CPU_LOAD --> CPU_INFERENCE[CPU Inference]
    GPU_LOAD --> GPU_INFERENCE[GPU Inference]
    
    CPU_INFERENCE --> RESPONSE[Generate Response]
    GPU_INFERENCE --> RESPONSE
    
    subgraph "GPU Memory Management"
        GPU_LOAD --> ALLOCATE[Allocate GPU Memory]
        ALLOCATE --> TRANSFER[Transfer Model to GPU]
        TRANSFER --> OPTIMIZE[Optimize for GPU]
    end
    
    subgraph "Performance Monitoring"
        GPU_INFERENCE --> MONITOR[Monitor GPU Usage]
        MONITOR --> ADJUST{Adjust Parameters?}
        ADJUST -->|Yes| OPTIMIZE
        ADJUST -->|No| CONTINUE[Continue Inference]
        CONTINUE --> RESPONSE
    end
```

### GPU vs CPU Performance Comparison

```mermaid
graph LR
    subgraph "CPU Processing"
        CPU_CORES[Multiple CPU Cores]
        CPU_MEMORY[System RAM]
        CPU_SPEED[Sequential Processing]
    end
    
    subgraph "GPU Processing"
        GPU_CORES[Thousands of GPU Cores]
        GPU_MEMORY[GPU VRAM]
        GPU_SPEED[Parallel Processing]
    end
    
    subgraph "Performance Metrics"
        TOKENS_SEC[Tokens/Second]
        LATENCY[Response Latency]
        THROUGHPUT[Request Throughput]
    end
    
    CPU_CORES --> TOKENS_SEC
    CPU_MEMORY --> LATENCY
    CPU_SPEED --> THROUGHPUT
    
    GPU_CORES --> TOKENS_SEC
    GPU_MEMORY --> LATENCY
    GPU_SPEED --> THROUGHPUT
```

## Error Handling Flow

This diagram illustrates how different types of errors are handled:

```mermaid
flowchart TD
    REQUEST[Incoming Request] --> VALIDATE{Valid Format?}
    
    VALIDATE -->|No| FORMAT_ERROR[400 Bad Request]
    VALIDATE -->|Yes| AUTH_CHECK{Authorized?}
    
    AUTH_CHECK -->|No| AUTH_ERROR[401 Unauthorized]
    AUTH_CHECK -->|Yes| MODEL_CHECK{Model Exists?}
    
    MODEL_CHECK -->|No| NOT_FOUND[404 Model Not Found]
    MODEL_CHECK -->|Yes| RESOURCE_CHECK{Resources Available?}
    
    RESOURCE_CHECK -->|No| RESOURCE_ERROR[503 Service Unavailable]
    RESOURCE_CHECK -->|Yes| PROCESS[Process Request]
    
    PROCESS --> INFERENCE_CHECK{Inference Successful?}
    
    INFERENCE_CHECK -->|No| INFERENCE_ERROR[500 Internal Server Error]
    INFERENCE_CHECK -->|Yes| SUCCESS[200 OK Response]
    
    subgraph "Error Recovery"
        INFERENCE_ERROR --> RETRY{Retry Possible?}
        RETRY -->|Yes| PROCESS
        RETRY -->|No| LOG_ERROR[Log Error Details]
        LOG_ERROR --> CLEANUP[Cleanup Resources]
    end
    
    subgraph "Error Responses"
        FORMAT_ERROR --> ERROR_RESPONSE[JSON Error Response]
        AUTH_ERROR --> ERROR_RESPONSE
        NOT_FOUND --> ERROR_RESPONSE
        RESOURCE_ERROR --> ERROR_RESPONSE
        CLEANUP --> ERROR_RESPONSE
    end
```

### Error Types and Handling

```mermaid
graph TD
    subgraph "Client Errors (4xx)"
        BAD_REQUEST[400 Bad Request<br/>Invalid JSON/Parameters]
        UNAUTHORIZED[401 Unauthorized<br/>Missing/Invalid Auth]
        NOT_FOUND[404 Not Found<br/>Model/Endpoint Missing]
        RATE_LIMIT[429 Too Many Requests<br/>Rate Limiting]
    end
    
    subgraph "Server Errors (5xx)"
        INTERNAL[500 Internal Server Error<br/>Inference Failure]
        NOT_IMPLEMENTED[501 Not Implemented<br/>Unsupported Feature]
        UNAVAILABLE[503 Service Unavailable<br/>Resource Exhaustion]
        TIMEOUT[504 Gateway Timeout<br/>Request Timeout]
    end
    
    subgraph "Recovery Strategies"
        RETRY[Automatic Retry]
        FALLBACK[Fallback Model]
        QUEUE[Request Queuing]
        SCALE[Resource Scaling]
    end
    
    BAD_REQUEST --> VALIDATE_INPUT[Input Validation]
    NOT_FOUND --> FALLBACK
    RATE_LIMIT --> QUEUE
    INTERNAL --> RETRY
    UNAVAILABLE --> SCALE
    TIMEOUT --> RETRY
```

## System Integration Patterns

### Microservices Integration

```mermaid
graph TB
    subgraph "Application Layer"
        WEB_APP[Web Application]
        MOBILE[Mobile App]
        CLI_TOOL[CLI Tool]
    end
    
    subgraph "API Gateway"
        GATEWAY[Load Balancer/Gateway]
        AUTH_SERVICE[Authentication Service]
        RATE_LIMITER[Rate Limiter]
    end
    
    subgraph "Ollama Cluster"
        OLLAMA1[Ollama Instance 1]
        OLLAMA2[Ollama Instance 2]
        OLLAMA3[Ollama Instance 3]
    end
    
    subgraph "Shared Storage"
        MODEL_STORE[Model Storage]
        CONFIG_STORE[Configuration Store]
        LOG_STORE[Log Storage]
    end
    
    WEB_APP --> GATEWAY
    MOBILE --> GATEWAY
    CLI_TOOL --> GATEWAY
    
    GATEWAY --> AUTH_SERVICE
    GATEWAY --> RATE_LIMITER
    GATEWAY --> OLLAMA1
    GATEWAY --> OLLAMA2
    GATEWAY --> OLLAMA3
    
    OLLAMA1 --> MODEL_STORE
    OLLAMA2 --> MODEL_STORE
    OLLAMA3 --> MODEL_STORE
    
    OLLAMA1 --> CONFIG_STORE
    OLLAMA2 --> CONFIG_STORE
    OLLAMA3 --> CONFIG_STORE
```

## Conclusion

These diagrams provide a comprehensive view of Ollama's architecture and operational patterns. Understanding these flows helps in:

1. **Troubleshooting**: Identifying where issues might occur in the system
2. **Optimization**: Understanding bottlenecks and performance characteristics
3. **Integration**: Planning how to integrate Ollama into larger systems
4. **Development**: Building applications that effectively use Ollama's capabilities

For hands-on experience with these concepts, refer to:
- `api_examples.py` - Practical API usage examples
- `model_management.py` - Model management operations
- `ollama_features.py` - Feature demonstrations
- `installation_guide.md` - Setup and configuration details