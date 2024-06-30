import asyncio,httpx
from time import perf_counter



async def main():
    start = perf_counter()
    tasks = []
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            tasks.append(client.get('https://dog.ceo/api/breeds/image/random'))
        responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response.text)
    print("Seconds Took: ",perf_counter() - start)

if __name__ == '__main__':
    asyncio.run(main())