"""
Configuraciones del servidor MCP y preparación de herramientas de análisis de seguridad.
"""

import os
from typing import Dict, Any
from agents.mcp import MCPServerStdio, create_static_tool_filter

def get_semgrep_server_params() -> Dict[str, Any]:
    """Obtiene los parámetros de configuración para el servidor MCP de Semgrep."""
    semgrep_app_token = os.getenv("SEMGREP_APP_TOKEN")
    
    # Entorno mejorado para depuración
    env = {
        "SEMGREP_APP_TOKEN": semgrep_app_token,
        "PYTHONUNBUFFERED": "1",  # Asegura que la salida no esté almacenada en búfer
    }
    
    return {
        "command": "uvx",
        "args": [
            "--with", "mcp==1.12.2", 
            "--quiet",  # Reduce el ruido de salida de uvx
            "semgrep-mcp"
        ],
        "env": env,
    }

def create_semgrep_server() -> MCPServerStdio:
    """Crea y configura la instancia del servidor MCP de Semgrep."""
    params = get_semgrep_server_params()
    return MCPServerStdio(
        params=params,
        client_session_timeout_seconds=120,
        tool_filter=create_static_tool_filter(allowed_tool_names=["semgrep_scan"]),
    )