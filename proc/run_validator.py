# encoding: utf-8
"""
验证器逻辑
"""

import asyncio
import time
from db import conn
from config import *
import aiohttp
from aiohttp_socks import ProxyConnector

loop = asyncio.get_event_loop()


def main(proc_lock):
    """
    验证器
    主要逻辑：
    创建VALIDATE_THREAD_NUM个验证线程，这些线程会不断运行
    While True:
        检查验证线程是否返回了代理的验证结果
        从数据库中获取若干当前待验证的代理
        将代理发送给前面创建的线程
    """
    conn.set_proc_lock(proc_lock)

    in_que = asyncio.Queue()
    out_que = asyncio.Queue()

    tasks = []
    for _ in range(VALIDATE_THREAD_NUM):
        func = validate_thread(in_que, out_que)
        tasks.append(asyncio.ensure_future(func))
    tasks.append(asyncio.ensure_future(get_new_proxy(in_que, out_que)))
    loop.run_until_complete(asyncio.wait(tasks))


async def get_new_proxy(in_que: asyncio.Queue, out_que: asyncio.Queue):
    running_proxies = set()  # 储存哪些代理正在运行，以字符串的形式储存
    while True:
        out_cnt = 0
        result_list = []
        while not out_que.empty():
            proxy, success, latency = await out_que.get()
            result_list.append([proxy, success, latency])
            uri = f'{proxy.protocol}://{proxy.ip}:{proxy.port}'
            running_proxies.remove(uri)
            out_cnt = out_cnt + 1
        if out_cnt > 0:
            conn.pushValidateResult(result_list)
            print(f'完成了{out_cnt}个代理的验证')

        # 如果正在进行验证的代理足够多，那么就不着急添加新代理
        if len(running_proxies) >= VALIDATE_THREAD_NUM * 2:
            await asyncio.sleep(PROC_VALIDATOR_SLEEP)
            continue

        # 找一些新的待验证的代理放入队列中
        added_cnt = 0
        for proxy in conn.getToValidate(VALIDATE_THREAD_NUM * 4):
            uri = f'{proxy.protocol}://{proxy.ip}:{proxy.port}'
            # 这里找出的代理有可能是正在进行验证的代理，要避免重复加入
            if uri not in running_proxies:
                running_proxies.add(uri)
                await in_que.put(proxy)
                added_cnt += 1

        if added_cnt == 0:
            await asyncio.sleep(PROC_VALIDATOR_SLEEP)


async def validate_once(proxy: conn.Proxy):
    """
    进行一次验证，如果验证成功则返回True，否则返回False或者是异常
    """
    connector = ProxyConnector.from_url(f'{proxy.protocol}://{proxy.ip}:{proxy.port}')
    timeout = aiohttp.ClientTimeout(total=VALIDATE_TIMEOUT)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with session.get(VALIDATE_URL, allow_redirects=False) as response:
            if VALIDATE_METHOD == "GET":
                if VALIDATE_KEYWORD in await response.text():
                    return True
                return False
            else:
                if VALIDATE_HEADER in response.headers and VALIDATE_KEYWORD in response.headers[VALIDATE_HEADER]:
                    return True
                return False


async def validate_thread(in_que: asyncio.Queue, out_que: asyncio.Queue):
    """
    验证函数，这个函数会在一个线程中被调用
    in_que: 输入队列，用于接收验证任务
    out_que: 输出队列，用于返回验证结果
    in_que和out_que都是线程安全队列，并且如果队列为空，调用in_que.get()会阻塞线程
    """

    while True:
        proxy = await in_que.get()
        success = False
        latency = None
        for _ in range(VALIDATE_MAX_FAILS):
            try:
                start_time = time.time()
                if await validate_once(proxy):
                    end_time = time.time()
                    latency = int((end_time - start_time) * 1000)
                    success = True
                    break
            except Exception as e:
                pass

        await out_que.put((proxy, success, latency))
