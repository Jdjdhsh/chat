import aiohttp
import asyncio
import time

async def send_request(session, url):
    try:
        async with session.get(url) as response:
            return response.status, await response.text()[:10]  # Trả về mã trạng thái và 100 ký tự đầu tiên
    except Exception as e:
        return None, f"Error: {e}"

async def main(url, num_requests, timeout):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url) for _ in range(num_requests)]
        results = await asyncio.wait_for(asyncio.gather(*tasks), timeout)
        return results

if __name__ == "__main__":
    url = input("Nhập URL của website: ")
    num_requests = int(input("Nhập số lượng yêu cầu: "))
    timeout = int(input("Nhập thời gian giới hạn (giây): "))
    
    start_time = time.time()
    
    try:
        results = asyncio.run(main(url, num_requests, timeout))
        for status, response in results:
            if status:
                print(f"Mã trạng thái: {status}, Phản hồi: {response}")
            else:
                print(response)
    except asyncio.TimeoutError:
        print("Thời gian gửi yêu cầu đã vượt quá giới hạn.")

    print(f"Tổng thời gian: {time.time() - start_time:.2f} giây")
    
