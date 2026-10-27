"""只读工具的有限重试与输入/输出契约演示。"""

import random
import time
from typing import Any, Callable


class RetryableToolError(RuntimeError):
    """表示仅可对只读操作重试的临时故障。"""

    def __init__(self, message: str, retry_after_s: float | None = None):
        """保存服务端建议的最短等待时间。"""
        super().__init__(message)
        self.retry_after_s = retry_after_s


def call_read_only_tool(
    operation: Callable[[dict[str, Any]], dict[str, Any]],
    args: dict[str, Any],
    validate_args: Callable[[dict[str, Any]], None],
    validate_output: Callable[[dict[str, Any]], None],
    *,
    max_attempts: int = 3,
    total_budget_s: float = 5.0,
) -> dict[str, Any]:
    """校验只读工具并仅针对临时错误实施有预算的重试。"""
    validate_args(args)
    started = time.monotonic()

    for attempt in range(1, max_attempts + 1):
        try:
            output = operation(args)
            validate_output(output)
            return output
        except RetryableToolError as error:
            if attempt == max_attempts:
                raise

            # 服务端 Retry-After 优先，否则使用指数退避与小幅随机抖动。
            backoff = min(0.4 * (2 ** (attempt - 1)), 4.0)
            minimum_wait = error.retry_after_s if error.retry_after_s is not None else backoff
            delay = minimum_wait + random.uniform(0.0, 0.15)

            # 避免下一轮等待超过整个任务的预算。
            remaining = total_budget_s - (time.monotonic() - started)
            if delay > remaining:
                raise TimeoutError("工具重试预算耗尽") from error
            time.sleep(delay)

    raise AssertionError("不可达的工具循环出口")
