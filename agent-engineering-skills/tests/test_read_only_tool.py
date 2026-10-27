"""只测试示例接口的实际可达故障路径。"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from read_only_tool import RetryableToolError, call_read_only_tool


def require_keyword(args: dict) -> None:
    """要求查询参数带有非空关键字。"""
    if not isinstance(args.get("keyword"), str) or not args["keyword"]:
        raise ValueError("keyword 必须是非空字符串")


def require_count(result: dict) -> None:
    """要求响应包含非负整数 count。"""
    if not isinstance(result.get("count"), int) or result["count"] < 0:
        raise ValueError("count 必须是非负整数")


class ToolReliabilityTests(unittest.TestCase):
    """覆盖输入校验、临时故障、输出损坏和预算用尽。"""

    def test_invalid_args_never_call_tool(self):
        """输入错误时不允许调用工具。"""
        called = []
        with self.assertRaises(ValueError):
            call_read_only_tool(lambda p: called.append(p), {}, require_keyword, require_count)
        self.assertEqual(called, [])

    def test_transient_error_then_success(self):
        """临时失败后成功，必须恰好调用两次。"""
        attempts = []

        def operation(args):
            """模拟第一次临时失败的只读请求。"""
            attempts.append(args)
            if len(attempts) == 1:
                raise RetryableToolError("service unavailable", retry_after_s=0)
            return {"count": 2}

        with patch("read_only_tool.time.sleep"):
            result = call_read_only_tool(
                operation, {"keyword": "ng"}, require_keyword, require_count
            )
        self.assertEqual(result, {"count": 2})
        self.assertEqual(len(attempts), 2)

    def test_invalid_output_is_not_retried(self):
        """结果违反契约时不得无限重试。"""
        attempts = []
        def operation(args):
            """返回不符合契约的结果。"""
            attempts.append(args)
            return {"count": None}
        with self.assertRaises(ValueError):
            call_read_only_tool(
                operation, {"keyword": "ng"}, require_keyword, require_count
            )
        self.assertEqual(len(attempts), 1)

    def test_budget_blocks_unnecessary_retry(self):
        """等待时间超过预算时立即停止。"""
        with self.assertRaises(TimeoutError):
            call_read_only_tool(
                lambda _: (_ for _ in ()).throw(RetryableToolError("rate limit", 1)),
                {"keyword": "ng"}, require_keyword, require_count,
                total_budget_s=0,
            )


if __name__ == "__main__":
    unittest.main()
