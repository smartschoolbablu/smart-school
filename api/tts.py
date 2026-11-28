from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import asyncio
import edge_tts

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        text = query.get('text', ['السلام علیکم'])[0]
        voice = query.get('voice', ['ur-PK-UzmaNeural'])[0]
        rate = query.get('rate', ['+0%'])[0]
        pitch = query.get('pitch', ['+0Hz'])[0]

        async def get_audio():
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data

        audio_bytes = asyncio.run(get_audio())

        self.send_response(200)
        self.send_header('Content-Type', 'audio/mpeg')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(audio_bytes)
