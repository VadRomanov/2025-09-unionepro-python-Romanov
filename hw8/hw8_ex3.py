import asyncio
import time
import random


def finish_callback(future, tasks):
    for task in tasks:
        task.cancel()

async def generate_data(output_queue, items_count):
    for i in range(items_count):
        data = {"id": i, "status": "raw"}
        await asyncio.sleep(random.uniform(0, 0.5))
        print(f"[ГЕНЕРАТОР] Сгенерированы данные: {data}")
        await output_queue.put(data)

async def process_data(worker_id, input_queue, output_queue):
    try:
        while True:
            data = await output_queue.get()
            await asyncio.sleep(random.uniform(0.1, 1.0))
            data.update({"status": "processed"})
            print(f"[ВОРКЕР_{worker_id}] Обработаны данные: {data}")
            await input_queue.put(data)
    except asyncio.CancelledError:
        print(f"[ВОРКЕР_{worker_id}] Завершил работу")


async def aggregate_results(input_queue, items_count):
    for _ in range(items_count):
        result = await input_queue.get()
        print(f"[АГРЕГАТОР] Получен результат: {result}")

async def main(items_count, worker_count):
    start_time = time.time()

    output_queue = asyncio.Queue()
    input_queue = asyncio.Queue()

    workers = [asyncio.create_task(process_data(i, input_queue, output_queue)) for i in range(worker_count)]

    generate_task = asyncio.create_task(generate_data(output_queue, items_count))
    aggregate_task = asyncio.create_task(aggregate_results(input_queue, items_count))
    aggregate_task.add_done_callback(lambda f: finish_callback(f, workers))

    await asyncio.gather(generate_task, aggregate_task, *workers)

    print()
    print(f"Общее время: {time.time() - start_time:.2f} секунд")

asyncio.run(main(3, 3))
