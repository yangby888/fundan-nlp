"""AI Shop MCP Server - 让任何AI智能体/开发者调用AI数字商品商店API
Tools:
- list_products: 列出全部商品
- recommend_product: 按需求推荐商品
- get_product_detail: 获取商品详情
- check_service_status: 检查商店服务状态
"""
import json
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ai-shop")

SHOP_BASE = "http://ai.ywtechai.cn:18087"

def _get(url: str) -> dict:
    r = httpx.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def list_products() -> list[dict[str, Any]]:
    """列出AI数字商品商店的全部商品(含价格/描述)"""
    data = _get(f"{SHOP_BASE}/shop.json")
    return data.get("products", [])

@mcp.tool()
def recommend_product(need: str) -> dict[str, Any]:
    """按用户需求推荐商品。need: 用户想买什么(如"答辩PPT""老人手机教程""情书""塔罗")"""
    r = httpx.post(f"{SHOP_BASE}/recommend.json", json={"need": need}, timeout=15)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def get_product_detail(product_id: str) -> dict[str, Any]:
    """获取单个商品详情"""
    products = _get(f"{SHOP_BASE}/shop.json").get("products", [])
    for p in products:
        if p.get("id") == product_id or p.get("name") == product_id:
            return p
    return {"error": "product not found", "products": [p.get("name") for p in products]}

@mcp.tool()
def check_service_status() -> dict[str, Any]:
    """检查商店服务是否在线"""
    try:
        data = _get(f"{SHOP_BASE}/shop.json")
        return {"status": "online", "products": len(data.get("products", [])), "url": SHOP_BASE}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    mcp.run()
