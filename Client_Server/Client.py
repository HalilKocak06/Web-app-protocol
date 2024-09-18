import asyncio
from Maip_Builder import Maip_Builder
from Maip_Resolver import Maip_Resolver

# Bu fonksiyon sunucu yanıtını okur ve yazdırır.
async def read_from_server(reader):
    resolver_obj = Maip_Resolver()
    while True:
        data = await reader.read(1024)
        if not data:
            break
        # Print the received message
        decoded_data =data.decode('utf-8').strip()
        print(f"Received from server: {data.decode().strip()}",end="")
        
        resolver_obj.resolver(decoded_data)


async def send_to_server(writer):
    loop = asyncio.get_running_loop()
    while True:
        client_input = await loop.run_in_executor(None, input, "\nEnter message to send (type 'exit' to quit): ")
        pars_obj = Maip_Builder()
        parsed_format=pars_obj.set_request_identification('INF','inf_accept_client')


        outData = pars_obj.generate_payload(client_input)
        

        if client_input.lower() == 'exit':
            break
        writer.write(outData.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def start_client():
    reader, writer = await asyncio.open_connection('192.168.110.78', 8070) 
    # Sunucudan gelen mesajları okumak için bir görev başlat
    asyncio.create_task(read_from_server(reader))
    # Sunucuya mesaj göndermek için ana fonksiyonu çalıştır
    await send_to_server(writer)

# myData = '''MAIP3.2 2000
# CSID:15;14;13;12
# CLID:3645644232 
# LENGTH:11
# END
# Hello world'''

# myResolver = Maip_Resolver()
# myResolver.resolver(myData)

if __name__ == "__main__":
     asyncio.run(start_client())