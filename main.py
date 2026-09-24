import asyncio


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Cliente conectado: {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            print(f"Cliente desconectado: {addr}")
            break

        msg = data.decode()
        print(f"Recebido de {addr}: {msg}")

        resposta = "Mensagem recebida pelo servidor!"
        writer.write(resposta.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5000)
    addr = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Servidor rodando em {addr}")

    async with server:
        await server.serve_forever()

asyncio.run(main())
