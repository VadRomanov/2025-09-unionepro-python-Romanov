import asyncio
import time

async def prepare():
    print("Подготовка...")
    await asyncio.sleep(0.1)

async def execute():
    print("Выполнение...")
    await asyncio.sleep(0.2)

async def cleanup():
    print("Завершение...")
    await asyncio.sleep(0.05)

async def main():
    start_time = time.time()
    await prepare()
    await execute()
    await cleanup()
    print()
    print(f"Общее время: {time.time() - start_time:.2f} секунд")

asyncio.run(main())