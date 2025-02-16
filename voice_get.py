import asyncio
import edge_tts
async def test_tts():
    tts = edge_tts.Communicate("谢晓虎哥哥~，抱抱我", "zh-CN-XiaoyiNeural")
    await tts.save("test2.mp3")
#
asyncio.run(test_tts())