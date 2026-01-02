import asyncio
import requests


async def reg():
    r = requests.get('https://ya.ru')

    return r

async def ex1():
    print('ex1 start')
    await asyncio.sleep(2)
    print('ex1 stop')

async def ex2():
    print('ex2 start')
    await asyncio.sleep(2)
    print('ex2 stop')


async def main():
    r = await reg()
    await asyncio.gather(ex1(), ex2())
    print(r)

if __name__ == '__main__':
    asyncio.run(main())