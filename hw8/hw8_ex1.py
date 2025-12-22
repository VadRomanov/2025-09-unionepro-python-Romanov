import asyncio
import time

async def task():
    print("Асинхронность")
    await asyncio.sleep(1)
    print("-")
    await asyncio.sleep(1.5)
    print("это")
    await asyncio.sleep(2)
    print("просто")

async def main():
    start_time = time.time()
    await task()
    print()
    print(f"Общее время: {time.time() - start_time:.2f} секунд")

asyncio.run(main())