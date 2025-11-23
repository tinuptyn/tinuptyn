"""
HTTP客户端工具
"""

import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin
try:
    import urllib.request as request
    import urllib.error as error
except ImportError:
    import urllib2 as request


class HTTPResponse:
    """HTTP响应封装"""
    
    def __init__(self, status_code: int, body: str, headers: Dict):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        
    def json(self) -> Any:
        """解析JSON响应"""
        return json.loads(self.body)
        
    @property
    def text(self) -> str:
        """获取文本响应"""
        return self.body


class HTTPClient:
    """HTTP客户端，用于集成测试"""
    
    def __init__(self, base_url: str = "", default_headers: Optional[Dict] = None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.session_cookies = {}
        
    def get(self, path: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> HTTPResponse:
        """发送GET请求"""
        return self._request('GET', path, headers=headers, params=params)
        
    def post(self, path: str, data: Any = None, json_data: Any = None, 
             headers: Optional[Dict] = None) -> HTTPResponse:
        """发送POST请求"""
        return self._request('POST', path, data=data, json_data=json_data, headers=headers)
        
    def put(self, path: str, data: Any = None, json_data: Any = None,
            headers: Optional[Dict] = None) -> HTTPResponse:
        """发送PUT请求"""
        return self._request('PUT', path, data=data, json_data=json_data, headers=headers)
        
    def delete(self, path: str, headers: Optional[Dict] = None) -> HTTPResponse:
        """发送DELETE请求"""
        return self._request('DELETE', path, headers=headers)
        
    def patch(self, path: str, data: Any = None, json_data: Any = None,
              headers: Optional[Dict] = None) -> HTTPResponse:
        """发送PATCH请求"""
        return self._request('PATCH', path, data=data, json_data=json_data, headers=headers)
        
    def _request(self, method: str, path: str, data: Any = None, 
                 json_data: Any = None, headers: Optional[Dict] = None,
                 params: Optional[Dict] = None) -> HTTPResponse:
        """发送HTTP请求"""
        # 构建完整URL
        url = urljoin(self.base_url, path)
        
        # 添加查询参数
        if params:
            from urllib.parse import urlencode
            url = f"{url}?{urlencode(params)}"
        
        # 合并请求头
        req_headers = {**self.default_headers}
        if headers:
            req_headers.update(headers)
            
        # 处理请求体
        body = None
        if json_data is not None:
            body = json.dumps(json_data).encode('utf-8')
            req_headers['Content-Type'] = 'application/json'
        elif data is not None:
            if isinstance(data, str):
                body = data.encode('utf-8')
            elif isinstance(data, bytes):
                body = data
            else:
                body = str(data).encode('utf-8')
                
        # 创建请求
        req = request.Request(url, data=body, headers=req_headers, method=method)
        
        try:
            # 发送请求
            with request.urlopen(req) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')
                response_headers = dict(response.headers)
                
                return HTTPResponse(status_code, response_body, response_headers)
                
        except error.HTTPError as e:
            # 处理HTTP错误
            status_code = e.code
            response_body = e.read().decode('utf-8') if e.fp else ""
            response_headers = dict(e.headers) if hasattr(e, 'headers') else {}
            
            return HTTPResponse(status_code, response_body, response_headers)
            
    def set_header(self, key: str, value: str):
        """设置默认请求头"""
        self.default_headers[key] = value
        
    def set_auth(self, username: str, password: str):
        """设置基本认证"""
        import base64
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.set_header('Authorization', f'Basic {credentials}')
        
    def set_bearer_token(self, token: str):
        """设置Bearer Token"""
        self.set_header('Authorization', f'Bearer {token}')
