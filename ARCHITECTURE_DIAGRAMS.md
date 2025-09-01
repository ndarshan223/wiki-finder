# 🏗️ SDLC Chatbot Architecture Diagrams

This document provides visual representations of the system architecture, data flow, and component relationships to help developers understand the codebase from scratch.

## 📊 Entity Relationship Diagram

```mermaid
erDiagram
    AppConfig ||--|| SearchConfig : contains
    AppConfig ||--|| DataConfig : contains
    AppConfig ||--|| UIConfig : contains
    
    ChatbotService ||--|| DataLoader : uses
    ChatbotService ||--|| SearchEngine : uses
    ChatbotService ||--|| ResultFormatter : uses
    
    DataLoader ||--o{ DataFile : loads
    DataFile {
        string tool
        string action
        string summary
        string confluence_link
    }
    
    SearchEngine ||--|| SearchStrategy : implements
    SearchEngine ||--|| SentenceTransformer : uses
    
    SearchStrategy ||--|| CosineSimilarityStrategy : concrete
    SearchStrategy ||--|| WeightedSimilarityStrategy : concrete
    
    ChatInterface ||--|| ChatbotService : depends_on
    ChatInterface ||--|| GradioComponents : creates
```

## 🔄 Code Property Graph - Component Dependencies

```mermaid
graph TD
    A[main.py] --> B[AppConfig]
    A --> C[ChatbotService]
    A --> D[ChatInterface]
    
    B --> E[SearchConfig]
    B --> F[DataConfig]
    B --> G[UIConfig]
    
    C --> H[DataLoader]
    C --> I[SearchEngine]
    C --> J[ResultFormatter]
    C --> K[ComponentFactory]
    
    H --> F
    I --> E
    I --> L[SearchStrategy]
    J --> M[SearchResult]
    
    L --> N[CosineSimilarityStrategy]
    L --> O[WeightedSimilarityStrategy]
    
    D --> G
    D --> P[GradioInterface]
    
    K --> Q[StrategyFactory]
    K --> R[EngineFactory]
    
    style A fill:#ff9999
    style C fill:#99ccff
    style D fill:#99ff99
    style B fill:#ffcc99
```

## 🚀 Application Bootup Flow

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Config as AppConfig
    participant Service as ChatbotService
    participant Loader as DataLoader
    participant Engine as SearchEngine
    participant UI as ChatInterface
    participant Gradio as GradioApp
    
    Main->>Config: Load configuration
    Config-->>Main: Return config object
    
    Main->>Service: Initialize ChatbotService(config)
    Service->>Loader: Create DataLoader
    Service->>Engine: Create SearchEngine
    Service->>Engine: Load sentence transformer model
    Engine-->>Service: Model loaded
    
    Service->>Loader: Load data files
    Loader->>Loader: Scan data/ folder
    Loader->>Loader: Read Excel/CSV files
    Loader->>Loader: Validate data structure
    Loader-->>Service: Return processed data
    
    Service->>Engine: Generate embeddings
    Engine->>Engine: Create text embeddings
    Engine-->>Service: Embeddings ready
    
    Main->>UI: Create ChatInterface(service, ui_config)
    UI->>UI: Setup Gradio components
    UI-->>Main: Return demo object
    
    Main->>Gradio: Launch demo
    Gradio-->>Main: Server started
```

## 🔍 Search Operation Flow

```mermaid
flowchart TD
    A[User Query] --> B[ChatInterface]
    B --> C[ChatbotService.search]
    C --> D[SearchEngine.search]
    D --> E[Encode Query]
    E --> F[Calculate Similarities]
    F --> G[Apply Threshold Filter]
    G --> H[Rank Results]
    H --> I[Format Results]
    I --> J[Return to UI]
    J --> K[Display Results]
    
    subgraph "Search Strategy"
        F --> L[CosineSimilarity]
        F --> M[WeightedSimilarity]
    end
    
    subgraph "Data Processing"
        N[Excel/CSV Files] --> O[DataLoader]
        O --> P[Validate Structure]
        P --> Q[Clean Data]
        Q --> R[Generate Embeddings]
        R --> S[Store in Memory]
    end
    
    style A fill:#ffeb3b
    style K fill:#4caf50
    style F fill:#2196f3
```

## 🏭 Factory Pattern Implementation

```mermaid
classDiagram
    class ComponentFactory {
        +create_data_loader(config) DataLoader
        +create_search_engine(config, strategy) SearchEngine
        +create_formatter() ResultFormatter
    }
    
    class SearchStrategyFactory {
        +create_strategy(type, params) SearchStrategy
    }
    
    class SearchStrategy {
        <<abstract>>
        +search(query, embeddings, data, k, threshold)*
    }
    
    class CosineSimilarityStrategy {
        +search(query, embeddings, data, k, threshold)
    }
    
    class WeightedSimilarityStrategy {
        -tool_weight: float
        -action_weight: float
        -summary_weight: float
        +search(query, embeddings, data, k, threshold)
    }
    
    ComponentFactory --> SearchStrategyFactory
    SearchStrategyFactory --> SearchStrategy
    SearchStrategy <|-- CosineSimilarityStrategy
    SearchStrategy <|-- WeightedSimilarityStrategy
```

## 📁 Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Layer"
        A[Excel Files]
        B[CSV Files]
        C[User Query]
    end
    
    subgraph "Processing Layer"
        D[DataLoader]
        E[SearchEngine]
        F[SentenceTransformer]
    end
    
    subgraph "Storage Layer"
        G[In-Memory Data]
        H[Embeddings Cache]
    end
    
    subgraph "Output Layer"
        I[Search Results]
        J[Gradio UI]
    end
    
    A --> D
    B --> D
    D --> G
    G --> E
    E --> F
    F --> H
    C --> E
    E --> I
    I --> J
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#fff3e0
    style I fill:#e8f5e8
    style J fill:#e8f5e8
```

## 🔧 Configuration Hierarchy

```mermaid
graph TD
    A[AppConfig] --> B[SearchConfig]
    A --> C[DataConfig]
    A --> D[UIConfig]
    
    B --> E[model_name: str]
    B --> F[similarity_threshold: float]
    B --> G[max_results: int]
    B --> H[strategy_type: str]
    
    C --> I[data_folder: str]
    C --> J[supported_formats: list]
    C --> K[required_columns: list]
    
    D --> L[server_name: str]
    D --> M[server_port: int]
    D --> N[theme: str]
    D --> O[title: str]
    
    style A fill:#ffcdd2
    style B fill:#c8e6c9
    style C fill:#bbdefb
    style D fill:#fff9c4
```

## 🎯 Component Interaction Matrix

```mermaid
graph TD
    subgraph "Core Services"
        CS[ChatbotService]
        DL[DataLoader]
        SE[SearchEngine]
        RF[ResultFormatter]
    end
    
    subgraph "UI Layer"
        CI[ChatInterface]
        GC[GradioComponents]
    end
    
    subgraph "Configuration"
        AC[AppConfig]
        SC[SearchConfig]
        DC[DataConfig]
        UC[UIConfig]
    end
    
    subgraph "Strategies"
        CSS[CosineSimilarityStrategy]
        WSS[WeightedSimilarityStrategy]
    end
    
    CS -.-> DL
    CS -.-> SE
    CS -.-> RF
    CI -.-> CS
    CI -.-> GC
    
    DL -.-> DC
    SE -.-> SC
    SE -.-> CSS
    SE -.-> WSS
    CI -.-> UC
    
    AC -.-> SC
    AC -.-> DC
    AC -.-> UC
```

## 🚦 Error Handling Flow

```mermaid
flowchart TD
    A[User Action] --> B{Valid Input?}
    B -->|No| C[Input Validation Error]
    B -->|Yes| D[Process Request]
    
    D --> E{Data Available?}
    E -->|No| F[No Data Error]
    E -->|Yes| G[Execute Search]
    
    G --> H{Search Successful?}
    H -->|No| I[Search Error]
    H -->|Yes| J[Format Results]
    
    J --> K{Results Found?}
    K -->|No| L[No Results Message]
    K -->|Yes| M[Display Results]
    
    C --> N[Error Handler]
    F --> N
    I --> N
    N --> O[User Feedback]
    
    L --> P[Helpful Message]
    M --> Q[Success Response]
    
    style C fill:#ffcdd2
    style F fill:#ffcdd2
    style I fill:#ffcdd2
    style N fill:#ff8a80
    style M fill:#c8e6c9
    style Q fill:#a5d6a7
```

## 📈 Performance Monitoring Points

```mermaid
graph LR
    subgraph "Startup Metrics"
        A[Config Load Time]
        B[Model Load Time]
        C[Data Load Time]
        D[Embedding Generation Time]
    end
    
    subgraph "Runtime Metrics"
        E[Query Processing Time]
        F[Search Execution Time]
        G[Result Formatting Time]
        H[UI Response Time]
    end
    
    subgraph "Resource Metrics"
        I[Memory Usage]
        J[CPU Usage]
        K[Disk I/O]
        L[Network I/O]
    end
    
    A --> E
    B --> F
    C --> F
    D --> F
    
    E --> I
    F --> J
    G --> K
    H --> L
```

## 🔄 State Management

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> LoadingConfig
    LoadingConfig --> LoadingData
    LoadingData --> LoadingModel
    LoadingModel --> GeneratingEmbeddings
    GeneratingEmbeddings --> Ready
    
    Ready --> Processing : User Query
    Processing --> Searching
    Searching --> Formatting
    Formatting --> Ready : Results Displayed
    
    Ready --> Reloading : Data Update
    Reloading --> LoadingData
    
    LoadingConfig --> Error : Config Error
    LoadingData --> Error : Data Error
    LoadingModel --> Error : Model Error
    GeneratingEmbeddings --> Error : Embedding Error
    Processing --> Error : Search Error
    
    Error --> Ready : Error Handled
    Error --> [*] : Fatal Error
```

## 🎨 UI Component Structure

```mermaid
graph TD
    A[ChatInterface] --> B[Main Tab]
    A --> C[Data Management Tab]
    
    B --> D[Query Input]
    B --> E[Search Button]
    B --> F[Results Display]
    B --> G[Status Messages]
    
    C --> H[File Upload]
    C --> I[Data Preview]
    C --> J[Reload Button]
    
    D --> K[Textbox Component]
    E --> L[Button Component]
    F --> M[HTML Component]
    G --> N[Markdown Component]
    
    H --> O[File Component]
    I --> P[Dataframe Component]
    J --> Q[Button Component]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#e8f5e8
```

## 🔍 Key Takeaways for Developers

### 1. **Modular Architecture**
- Each component has a single responsibility
- Dependencies are injected through constructors
- Configuration is centralized and type-safe

### 2. **Data Flow**
- Data flows unidirectionally from input to output
- Transformations happen at clear boundaries
- State is managed explicitly

### 3. **Extension Points**
- New search strategies can be added via the Strategy pattern
- UI components are modular and replaceable
- Configuration supports environment-specific overrides

### 4. **Error Handling**
- Errors are caught at component boundaries
- User feedback is provided for all error states
- System gracefully degrades when components fail

### 5. **Performance Considerations**
- Models are loaded once at startup
- Embeddings are cached in memory
- Search operations are optimized for speed

This architecture ensures the system is maintainable, testable, and extensible while providing a smooth user experience.