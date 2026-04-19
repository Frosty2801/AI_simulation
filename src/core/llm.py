"""
LLM module for PetCare Medellín automation.

This module provides:
- Chat client using OpenAI or Ollama
- Structured output for classification
- Response generation for RAG
"""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


# =============================================================================
# Pydantic Models for Structured Output
# =============================================================================

class MessageClassification(BaseModel):
    """Classification result for incoming messages."""
    categoria: str = Field(description="One of: URGENCIA, AGENDAMIENTO, CONSULTA, SEGUIMIENTO, ADMINISTRATIVA")
    prioridad: str = Field(description="One of: ALTA, MEDIA, BAJA")
    justificacion: str = Field(description="Brief explanation of the classification")
    accion_sugerida: Optional[str] = Field(default=None, description="Suggested action if applicable")


class AppointmentRequest(BaseModel):
    """Structured appointment request data."""
    nombre_mascota: str
    especie: str
    motivo: str
    fecha_preferida: str
    contacto: str


# =============================================================================
# LLM Client
# =============================================================================

class LLMClient:
    """
    Unified LLM client supporting OpenAI and Ollama.
    """
    
    def __init__(
        self,
        provider: str = None,
        model: str = None,
        temperature: float = 0.0,
        base_url: str = None
    ):
        """
        Initialize the LLM client.
        
        Args:
            provider: "openai" or "ollama" (default: from env)
            model: Model name (default: from env or "gpt-4o-mini")
            temperature: Sampling temperature
            base_url: Custom base URL for OpenAI-compatible APIs
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", os.getenv("EMBEDDING_PROVIDER", "openai"))
        
        if self.provider == "openai":
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self._client = ChatOpenAI(
                model=self.model,
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=base_url
            )
        elif self.provider == "ollama":
            self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
            self._client = ChatOllama(
                model=self.model,
                temperature=temperature,
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def chat(self, message: str, system_prompt: str = None) -> str:
        """
        Simple chat completion.
        
        Args:
            message: User message
            system_prompt: Optional system prompt
            
        Returns:
            Assistant response as string
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=message))
        
        response = self._client.invoke(messages)
        return response.content
    
    def chat_json(self, message: str, response_model: type[BaseModel], system_prompt: str = None) -> BaseModel:
        """
        Chat with JSON structured output.
        
        Args:
            message: User message
            response_model: Pydantic model for structured output
            system_prompt: Optional system prompt
            
        Returns:
            Parsed Pydantic model instance
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=message))
        
        # Use with_structured_method for newer langchain versions
        if hasattr(self._client, 'with_structured_output'):
            structured_llm = self._client.with_structured_output(response_model)
            return structured_llm.invoke(message)
        else:
            # Fallback: parse JSON from response
            response = self._client.invoke(messages)
            return response_model.model_validate_json(response.content)
    
    def classify_message(self, message: str, context: str = None) -> MessageClassification:
        """
        Classify an incoming message into one of 5 categories.
        
        Args:
            message: The incoming message to classify
            context: Optional context about the user/session
            
        Returns:
            MessageClassification with categoria, prioridad, justificacion
        """
        system_prompt = """Eres un asistente de clasificación para una clínica veterinaria.
Tu tarea es clasificar cada mensaje en una de estas categorías:

- URGENCIA: Emergencias reales o potenciales (dificultad respiratoria, convulsiones, sangrado, envenenamiento, trauma)
- AGENDAMIENTO: Solicitudes de citas, reprogramación o cancelaciones
- CONSULTA: Preguntas sobre servicios, precios, procedimientos, vacunas
- SEGUIMIENTO: Consultas sobre casos previos, resultados de exámenes
- ADMINISTRATIVA: Horarios, ubicación, políticas, certificados, pagos

Responde ÚNICAMENTE con JSON en este formato:
{
  "categoria": "CATEGORIA",
  "prioridad": "ALTA|MEDIA|BAJA",
  "justificacion": "explicación breve",
  "accion_sugerida": "acción recomendada si aplica"
}"""
        
        user_message = message
        if context:
            user_message = f"Contexto: {context}\n\nMensaje: {message}"
        
        return self.chat_json(user_message, MessageClassification, system_prompt)
    
    def generate_rag_response(
        self,
        query: str,
        context_docs: List[str],
        system_prompt: str = None
    ) -> str:
        """
        Generate a response based on retrieved documents (RAG).
        
        Args:
            query: User question
            context_docs: List of retrieved document chunks
            system_prompt: Optional custom system prompt
            
        Returns:
            Generated response string
        """
        default_system = """Eres un asistente de PetCare Medellín.
Responde las preguntas del usuario basándote ÚNICAMENTE en los documentos proporcionados.
Si la información no está en los documentos, indica que no tienes esa información.
Sé amable, profesional y conciso."""
        
        context = "\n\n".join([f"Documento {i+1}:\n{doc}" for i, doc in enumerate(context_docs)])
        
        full_prompt = f"""Basándote en esta información:

{context}

Responde esta pregunta: {query}"""
        
        return self.chat(full_prompt, system_prompt or default_system)


# =============================================================================
# Convenience Functions
# =============================================================================

def get_llm_client(provider: str = None, model: str = None) -> LLMClient:
    """
    Get a configured LLM client.
    
    Args:
        provider: "openai" or "ollama"
        model: Model name
        
    Returns:
        LLMClient instance
    """
    return LLMClient(provider=provider, model=model)


def classify(message: str, context: str = None) -> MessageClassification:
    """
    Quick classification function.
    
    Args:
        message: Message to classify
        context: Optional context
        
    Returns:
        MessageClassification
    """
    client = get_llm_client()
    return client.classify_message(message, context)


# =============================================================================
# Testing
# =============================================================================

if __name__ == "__main__":
    print("Testing LLM Client...")
    
    # Test basic chat
    client = get_llm_client()
    print(f"\nUsing provider: {client.provider}, model: {client.model}")
    
    # Test classification
    test_messages = [
        "Mi perro no puede respirar, está jadeando mucho",
        "Quiero agendar una cita para vaccunar a mi gato",
        "A qué hora abren la clínica?",
        "Mi perro fue operado hace una semana, cómo está?"
    ]
    
    print("\n--- Classification Tests ---")
    for msg in test_messages:
        try:
            result = client.classify_message(msg)
            print(f"\nMensaje: {msg}")
            print(f"  Categoría: {result.categoria}")
            print(f"  Prioridad: {result.prioridad}")
            print(f"  Justificación: {result.justificacion}")
        except Exception as e:
            print(f"\nError classifying: {msg}")
            print(f"  {e}")