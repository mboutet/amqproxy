import asyncio
import os

from aio_pika import (
    DeliveryMode,
    Message,
    connect,
)


async def main(loop):
    while True:
        try:
            connection = await connect(
                host=os.environ["AMPQ_HOST"],
                port=int(os.environ["AMPQ_PORT"]),
                login="guest",
                password="guest",
                loop=loop,
            )

            try:
                channel = await connection.channel(publisher_confirms=False)

                message = Message(
                    b"Hello World!",
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                async with channel.transaction():
                    await channel.default_exchange.publish(
                        message, routing_key="task_queue",
                    )

                print("Sent %r" % message, flush=True)

            finally:
                await connection.close()

        except Exception as e:
            print(e, flush=True)
            await asyncio.sleep(5)

        else:
            await asyncio.sleep(5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
