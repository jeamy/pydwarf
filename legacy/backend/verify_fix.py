import asyncio
import logging
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.lib.dwarfii_api import WebSocketHandler, DWARF_IP
from app.lib.dwarfii_camera import message_camera_tele_open_camera
from app.utils.constants import MODULE_CAMERA_TELE, CMD_CAMERA_TELE_OPEN_CAMERA

async def test_connection():
    logger.info(f"Testing connection to DWARF II at {DWARF_IP}")
    
    ws_handler = WebSocketHandler(DWARF_IP)
    
    # Event to wait for response
    response_received = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        logger.info(f"Received message: {result_data}")
        
        if result_data.get("module_id") == MODULE_CAMERA_TELE and \
           result_data.get("cmd") == CMD_CAMERA_TELE_OPEN_CAMERA:
            
            code = result_data.get("code")
            logger.info(f"Camera Open Response Code: {code}")
            
            if code == 0:
                logger.info("SUCCESS: Camera opened successfully!")
                response_received.set()
            elif code == 374:
                logger.info("SUCCESS: Camera was already open!")
                response_received.set()
            else:
                logger.error(f"FAILURE: Camera open failed with code {code}")
                response_received.set()

    ws_handler.register_message_callback("test_callback", message_callback)
    
    try:
        logger.info("Connecting to WebSocket...")
        await ws_handler.open()
        
        # Wait a bit for connection
        await asyncio.sleep(1)
        
        if not ws_handler.is_connected():
            logger.error("Failed to connect to WebSocket")
            return
            
        logger.info("WebSocket connected. Sending Open Camera command...")
        
        # Create Open Camera packet
        message_data = message_camera_tele_open_camera(binning=0, rtsp_encode_type=0)
        packet = ws_handler.create_packet(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_OPEN_CAMERA,
            message_data
        )
        
        ws_handler.send_packet(packet)
        
        logger.info("Command sent. Waiting for response...")
        
        try:
            await asyncio.wait_for(response_received.wait(), timeout=10.0)
            logger.info("Response received.")
            
            # Now check RTSP port
            logger.info("Checking RTSP port 554...")
            try:
                reader, writer = await asyncio.open_connection(DWARF_IP, 554)
                logger.info("SUCCESS: RTSP port 554 is open and reachable!")
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                logger.error(f"FAILURE: Could not connect to RTSP port: {e}")
                
        except asyncio.TimeoutError:
            logger.error("Timeout waiting for camera response")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await ws_handler.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
