import time
import random
import asyncio
def process_item(item):
    # 模拟耗时操作
    print(f"处理中：{item}")
    process_time = random.uniform(0.5, 2.0)
    time.sleep(process_time)
    return f"处理完成：{item}，耗时 {process_time:.2f} 秒"

def process_all_items():
    items = ["任务A", "任务B", "任务C", "任务D"]
    results = []
    for item in items:
        result = process_item(item)
        results.append(result)
    return results

def main():
    start = time.time()
    results = process_all_items()
    end = time.time()
    
    print("\n".join(results))
    print(f"总耗时：{end - start:.2f} 秒")
    return results

async def process_item_Coroutines(item):
    print(f"处理中：{item}")
    # async 定义的函数变成了协程
    process_time = random.uniform(0.5, 2.0)
    # time.sleep() 换成 asyncio.sleep()
    await asyncio.sleep(process_time)  # await 等待异步操作完成
    return f"处理完成：{item}，耗时 {process_time:.2f} 秒"

async def process_all_items_Coroutines():
    items = ["任务A", "任务B", "任务C", "任务D"]
    # 创建任务列表
    tasks = [
        asyncio.create_task(process_item_Coroutines(item))
        for item in items
    ]
    print("开始处理")
    results = await asyncio.gather(*tasks)
    return results

async def main_Coroutines():
    start = time.time()
    results = await process_all_items_Coroutines()
    end = time.time()
    
    print("\n".join(results))
    print(f"总耗时：{end - start:.2f} 秒")

if __name__ == "__main__":
    main()
    asyncio.run(main_Coroutines())

