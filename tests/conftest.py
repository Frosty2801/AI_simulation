"""
Pytest configuration and fixtures for PetCare Medellín tests.
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (may require API/DB)"
    )
    config.addinivalue_line(
        "markers", "ollama: marks tests that require Ollama running"
    )
    config.addinivalue_line(
        "markers", "openai: marks tests that require OpenAI API key"
    )


@pytest.fixture
def docs_dir():
    """Fixture providing path to docs directory."""
    return os.path.join(project_root, "docs")


@pytest.fixture
def sample_petcare_text():
    """Fixture providing sample pet care text for testing."""
    return """
    PetCare Medellín ofrece servicios de vacunación para perros y gatos.
    Los horarios de atención son de lunes a sábado de 8:00 AM a 6:00 PM.
    Las emergencias se atienden según disponibilidad del veterinario.
    Los precios de consulta son aproximadamente 70,000 COP.
    """


@pytest.fixture
def sample_appointment_message():
    """Fixture providing sample appointment request message."""
    return """
    Hola, quiero agendar una cita para mi perro Max.
    Es un golden retriever de 3 años.
    Necesita vacunación.
    Prefiero el próximo martes en la mañana.
    Mi número es 3001234567.
    """


@pytest.fixture
def sample_emergency_message():
    """Fixture providing sample emergency message."""
    return """
    URGENCIA: Mi perro no puede respirar, tiene la lengua azul.
    Está en casa y está muy mal.
    Por favor necesito ayuda inmediata.
    """


@pytest.fixture
def sample_consulta_message():
    """Fixture providing sample consultation message."""
    return """
    Buenos días, mi gato tiene el ojo irritado desde ayer.
    Está Lagrimeando mucho y lo mantiene cerrado.
    ¿Qué puedo hacer?
    """


@pytest.fixture
def sample_seguimiento_message():
    """Fixture providing sample follow-up message."""
    """
    Hola, soy María. Traje a mi mascota Luna yesterday for vaccination.
    Quería saber si ya puedo bañarla o tiene que esperar.
    """


@pytest.fixture
def sample_administrativa_message():
    """Fixture providing sample administrative message."""
    return """
    Buenas tardes, me podrían informar el horario de atención del sábado?
    Y también qué métodos de pago aceptan?
    """