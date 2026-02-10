import asyncio

from langchain_core.tools import tool


@tool
async def add(a: int, b: int) -> int:
    """
    Add 2 numbers
    :param a: the first number
    :param b: the second number
    :return:
    """
    await asyncio.sleep(10)
    return a + b
