# Architectural Decisions - Project Gurukul AI

## ADR 1: Foundation Selection
**Decision:** Use Sunbird ED as the foundational architecture.
**Rationale:** Sunbird provides battle-tested standards for Telemetry, Frameworks, and Assessment (QuML) that ensure interoperability with national education systems (DIKSHA).

## ADR 2: Tech Stack
**Decision:** Flutter for Frontend, Firebase for Backend.
**Rationale:** Flutter allows for a highly responsive, Material 3-compliant UI across platforms. Firebase offers managed services (Auth, Firestore, Functions) that fit within the required "free tier" constraints while providing production-ready scalability.

## ADR 3: AI Engine
**Decision:** Google Gemini 1.5 Flash via Generative AI SDK.
**Rationale:** Provides high performance and context window required for tutoring while maintaining a cost-effective (free tier) profile for initial deployment.

## ADR 4: Offline Strategy
**Decision:** Offline-First with Hive and background Sync Service.
**Rationale:** Students in low-connectivity areas need a seamless experience. Local metadata storage in Hive ensures the app remains interactive without internet.

## ADR 5: Knowledge Graph
**Decision:** Recursive Concept Node structure in Firestore.
**Rationale:** Simplifies prerequisites and dependency mapping without the overhead of a dedicated graph database (Neo4j) for the initial MVP, while remaining scalable to a graph DB later.
