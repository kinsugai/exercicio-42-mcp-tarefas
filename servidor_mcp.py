"""Ferramentas MCP que consomem a API REST de tarefas via HTTP real."""
import json
import os

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Tarefas")
API_URL = os.environ.get("TAREFAS_API_URL", "http://localhost:8000").rstrip("/")


@mcp.tool()
async def criar_tarefa(titulo: str) -> str:
    """Cria uma tarefa pela API e retorna seu JSON, incluindo o identificador."""
    async with httpx.AsyncClient(timeout=10.0, trust_env=False) as client:
        response = await client.post(f"{API_URL}/tarefas", json={"titulo": titulo})
        response.raise_for_status()
        return json.dumps(response.json(), ensure_ascii=False)


@mcp.tool()
async def listar_tarefas() -> str:
    """Lista as tarefas atualmente armazenadas na API REST."""
    async with httpx.AsyncClient(timeout=10.0, trust_env=False) as client:
        response = await client.get(f"{API_URL}/tarefas")
        response.raise_for_status()
        return json.dumps(response.json(), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")

