import asyncio

async def fetch_data():
    await asyncio.sleep(2)  # 模拟异步 I/O 操作
    return "Data fetched"
 
async def main_Coroutines():
    result = await fetch_data()
    print(result)
 
asyncio.run(main_Coroutines())

async def worker(name, delay):
    await asyncio.sleep(delay)
    print(f"Worker {name} completed")
 
async def main_task():
    task1 = asyncio.create_task(worker("A", 2))
    task2 = asyncio.create_task(worker("B", 3))
    await task1
    await task2
 
asyncio.run(main_task())

async def main_Future():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_soon(future.set_result, "Hello, Future!")
    result = await future
    print(result)
 
asyncio.run(main_Future())