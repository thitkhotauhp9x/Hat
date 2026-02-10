import asyncio

from langchain_core.tools import tool


@tool
async def weather(city: str) -> str:
    """
    The weather of the city
    :param city:
    :return:
    """
    await asyncio.sleep(1)
    return f"The weather in {city} is sunny."
