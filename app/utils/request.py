from fastapi import Request as FastAPIRequest

def get_ip_address(req: FastAPIRequest) -> str:
    ip_address = req.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if not ip_address:
        ip_address = req.client.host if req.client else "0.0.0.0"
    return ip_address