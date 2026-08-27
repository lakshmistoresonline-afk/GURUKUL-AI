from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..services.resource_service import ResourceService
from ..services.vector_rag_service import vector_rag
from ..utils.auth import get_current_user, AuthUser

router = APIRouter()
orchestrator = AIOrchestrator()
resource_service = ResourceService(orchestrator)

class GenerateRequest(BaseModel):
    prompt: str
    task_type: Optional[str] = "general"
    class_level: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None

class StructuredGenerateRequest(BaseModel):
    prompt: str
    output_schema: Dict[str, Any] = Field(alias="schema")
    task_type: Optional[str] = "structured"

@router.post("/generate")
async def generate(
    request: GenerateRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Generates AI content with class-scoped RAG context and verified identity."""
    authorized_class = user.class_name

    # Authorization: Student can only use RAG context for their own verified class
    rag_class = authorized_class

    context = ""

    if rag_class or request.subject:
        # Perform semantic search in ChromaDB
        context_chunks = await vector_rag.search(
            query=request.prompt,
            class_level=rag_class,
            subject=request.subject,
            limit=5
        )

        if context_chunks:
            context = "\n[OFFICIAL SOURCES (DIKSHA)]\n"
            for c in context_chunks:
                context += f"Source: {c['metadata'].get('title')} | {c['content']}\n"

    final_prompt = request.prompt
    if context:
        final_prompt = f"Using the following verified educational context, answer the student's question accurately.\n\nContext:\n{context}\n\nQuestion: {request.prompt}\n\nAnswer (Cite the source):"

    result = await orchestrator.generate(final_prompt, request.task_type)
    if not result["success"]:
        raise HTTPException(status_code=502, detail=result["error"])

    if context:
        result["rag_applied"] = True
        result["source_context"] = context
        result["verified_attribution"] = "DIKSHA"

    return result

@router.post("/generate-structured")
async def generate_structured(
    request: StructuredGenerateRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Generates structured AI content with verified identity."""
    result = await orchestrator.generate_structured(request.prompt, request.output_schema, request.task_type)
    if not result["success"]:
        raise HTTPException(status_code=502, detail=result["error"])
    return result

class EmbeddingRequest(BaseModel):
    text: str

@router.post("/embeddings")
async def generate_embeddings(
    request: EmbeddingRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Generates text embeddings with verified identity."""
    for provider in orchestrator.active_providers:
        try:
            vector = await provider.generate_embeddings(request.text)
            return {"embedding": vector}
        except:
            continue
    raise HTTPException(status_code=502, detail="Failed to generate embeddings")

class DictionaryRequest(BaseModel):
    word: str
    context: Optional[str] = ""

@router.post("/dictionary")
async def dictionary_lookup(
    request: DictionaryRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Provides a simple dictionary entry for a student."""
    prompt = f'''
    Provide a simple dictionary entry for a Class 5-6 student:
    Word: "{request.word}"
    Context: "{request.context}"

    Include:
    1. Meaning (simple words)
    2. Example sentence
    3. Fun memory trick to remember it.

    Return as JSON:
    {{
      "meaning": "...",
      "example": "...",
      "memoryTrick": "..."
    }}
    '''
    schema = {
        "type": "object",
        "properties": {
            "meaning": {"type": "string"},
            "example": {"type": "string"},
            "memoryTrick": {"type": "string"}
        },
        "required": ["meaning", "example", "memoryTrick"]
    }
    result = await orchestrator.generate_structured(prompt, schema, "DICTIONARY")
    if not result["success"]:
        raise HTTPException(status_code=502, detail=result["error"])
    return result["data"]
