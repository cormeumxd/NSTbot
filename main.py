import asyncio
from bot import dp

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
