import os
import uvicorn

from app import build_app

if __name__ == '__main__':
    uvicorn.run(
        build_app(),
        # host=os.getenv('server_address', get_settings().server.host),
        # port=int(os.getenv('server_port', get_settings().server.port)),
        # https://www.uvicorn.org/settings/#http
        proxy_headers=True,
        forwarded_allow_ips='*'
    )