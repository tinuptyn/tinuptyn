"""
负载测试工具
"""

import time
import threading
from typing import Callable, List, Dict, Any
from queue import Queue
import statistics


class LoadTestResult:
    """负载测试结果"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times: List[float] = []
        self.errors: List[str] = []
        self.start_time = 0
        self.end_time = 0
        
    @property
    def duration(self) -> float:
        """测试持续时间（秒）"""
        return self.end_time - self.start_time
        
    @property
    def requests_per_second(self) -> float:
        """每秒请求数"""
        return self.total_requests / self.duration if self.duration > 0 else 0
        
    @property
    def success_rate(self) -> float:
        """成功率"""
        return (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        
    @property
    def avg_response_time(self) -> float:
        """平均响应时间（毫秒）"""
        return statistics.mean(self.response_times) * 1000 if self.response_times else 0
        
    @property
    def p95_response_time(self) -> float:
        """95百分位响应时间（毫秒）"""
        if not self.response_times:
            return 0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[index] * 1000
        
    @property
    def p99_response_time(self) -> float:
        """99百分位响应时间（毫秒）"""
        if not self.response_times:
            return 0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.99)
        return sorted_times[index] * 1000
        
    def __str__(self):
        return f"""
Load Test Results:
==================
Total Requests: {self.total_requests}
Successful: {self.successful_requests}
Failed: {self.failed_requests}
Success Rate: {self.success_rate:.2f}%
Duration: {self.duration:.2f}s
Requests/sec: {self.requests_per_second:.2f}
Avg Response Time: {self.avg_response_time:.2f}ms
P95 Response Time: {self.p95_response_time:.2f}ms
P99 Response Time: {self.p99_response_time:.2f}ms
"""


class LoadTest:
    """负载测试工具"""
    
    def __init__(self):
        self.result = LoadTestResult()
        self._lock = threading.Lock()
        
    def run(self, func: Callable, 
            concurrent_users: int = 10,
            requests_per_user: int = 100,
            ramp_up_time: float = 0) -> LoadTestResult:
        """
        运行负载测试
        
        Args:
            func: 要测试的函数
            concurrent_users: 并发用户数
            requests_per_user: 每个用户的请求数
            ramp_up_time: 启动时间（秒）
        """
        self.result = LoadTestResult()
        self.result.start_time = time.time()
        
        threads = []
        ramp_up_delay = ramp_up_time / concurrent_users if ramp_up_time > 0 else 0
        
        print(f"\nStarting load test:")
        print(f"  Concurrent Users: {concurrent_users}")
        print(f"  Requests per User: {requests_per_user}")
        print(f"  Total Requests: {concurrent_users * requests_per_user}")
        print(f"  Ramp-up Time: {ramp_up_time}s\n")
        
        # 创建并启动线程
        for i in range(concurrent_users):
            thread = threading.Thread(
                target=self._worker,
                args=(func, requests_per_user)
            )
            threads.append(thread)
            thread.start()
            
            # 渐进启动
            if ramp_up_delay > 0:
                time.sleep(ramp_up_delay)
                
        # 等待所有线程完成
        for thread in threads:
            thread.join()
            
        self.result.end_time = time.time()
        
        print(self.result)
        return self.result
        
    def _worker(self, func: Callable, requests: int):
        """工作线程"""
        for _ in range(requests):
            start_time = time.perf_counter()
            
            try:
                func()
                success = True
            except Exception as e:
                success = False
                with self._lock:
                    self.result.errors.append(str(e))
                    
            end_time = time.perf_counter()
            response_time = end_time - start_time
            
            with self._lock:
                self.result.total_requests += 1
                self.result.response_times.append(response_time)
                
                if success:
                    self.result.successful_requests += 1
                else:
                    self.result.failed_requests += 1
                    
    def stress_test(self, func: Callable, 
                    max_users: int = 100,
                    step: int = 10,
                    duration_per_step: float = 10.0):
        """
        压力测试：逐步增加负载
        
        Args:
            func: 要测试的函数
            max_users: 最大用户数
            step: 每步增加的用户数
            duration_per_step: 每步持续时间（秒）
        """
        results = []
        
        print(f"\nStarting stress test:")
        print(f"  Max Users: {max_users}")
        print(f"  Step: {step}")
        print(f"  Duration per Step: {duration_per_step}s\n")
        
        for users in range(step, max_users + 1, step):
            print(f"\nTesting with {users} concurrent users...")
            
            # 计算每个用户应该发送的请求数
            requests_per_user = max(1, int(duration_per_step * 10))
            
            result = self.run(func, users, requests_per_user, ramp_up_time=0)
            results.append({
                'users': users,
                'rps': result.requests_per_second,
                'avg_response_time': result.avg_response_time,
                'success_rate': result.success_rate
            })
            
        # 打印汇总
        print("\n" + "="*60)
        print("Stress Test Summary")
        print("="*60)
        print(f"{'Users':<10} {'RPS':<15} {'Avg RT (ms)':<15} {'Success %':<10}")
        print("-"*60)
        
        for r in results:
            print(f"{r['users']:<10} {r['rps']:<15.2f} "
                  f"{r['avg_response_time']:<15.2f} {r['success_rate']:<10.2f}")
                  
        return results
