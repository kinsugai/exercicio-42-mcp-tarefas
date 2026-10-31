"""Exercita o servidor via MCP stdio e imprime somente o envelope JSON."""
import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def decode_result(result):
    if result.isError:
        raise RuntimeError(f"Ferramenta MCP falhou: {result.content}")
    texts = [block.text for block in result.content if block.type == "text"]
    if len(texts) != 1:
        raise ValueError("Esperado exatamente um bloco de texto JSON")
    return json.loads(texts[0])


async def main() -> dict:
    server = Path(__file__).resolve().with_name("servidor_mcp.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = sorted(tool.name for tool in tools.tools)
            if not {"criar_tarefa", "listar_tarefas"}.issubset(names):
                raise ValueError("Ferramentas obrigatorias ausentes")
            created = decode_result(await session.call_tool(
                "criar_tarefa", {"titulo": "tarefa via mcp"},
            ))
            listed = decode_result(await session.call_tool("listar_tarefas", {}))
            if not isinstance(created, dict) or not isinstance(created.get("id"), int):
                raise ValueError("A API nao devolveu uma tarefa com identificador")
            if created.get("titulo") != "tarefa via mcp" or created.get("concluida") is not False:
                raise ValueError("Tarefa criada diverge da solicitacao")
            if not isinstance(listed, list) or created not in listed:
                raise ValueError("A tarefa criada nao aparece na lista da API")
            return {"tools": names, "criar_resultado": created, "listar_resultado": listed}


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main()), ensure_ascii=False))

