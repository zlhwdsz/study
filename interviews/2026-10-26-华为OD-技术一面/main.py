import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List


class Solution:
    def batchExecuteTools(
        self,
        tasks: List[Dict[str, Any]],
        maxConcurrency: int
    ) -> List[Dict[str, Any]]:
        """
        请在此实现 Agent 工具批量并行执行逻辑：
        1. 控制并发调用上限不超过 maxConcurrency
        2. 支持异常捕获与在 maxRetries 范围内的自动重试
        3. 累计统计 attempts 次数
        4. 保证返回列表的顺序与 tasks 原顺序严格一致
        """
        # ==================== 候选人答题区域 (START) ====================
        executor = ThreadPoolExecutor(maxConcurrency)
        futures = []
        for task in tasks:
            new_task = Task(task)
            futures.append(executor.submit(new_task.run))
        ret = []
        for future in futures:
            ret.append(future.result())
        return ret

class Task:
    def __init__(self, orig_task):
        self.id = orig_task["id"]
        self.tool = orig_task["tool"]
        self.maxRetries = orig_task["maxRetries"]
        self.attempts = 0
    def run(self):
        while True:
            self.attempts += 1
            try:
                result = self.tool()
                return {"id": self.id, "status": "success", "result": result, "attempts": self.attempts}
            except Exception as e:
                if self.attempts <= self.maxRetries:
                    continue
                else:
                    error = str(e)
                    return {"id": self.id, "status": "error", "error": error, "attempts": self.attempts}

def build_mock_tools():
    """构造用于模拟实际业务情况的工具调用函数"""
    call_counts = {
        "flaky_search": 0,
        "timeout_db": 0,
        "slow_fail": 0,
    }

    def mock_calc():
        """算术工具：瞬间执行成功"""
        return 42

    def mock_flaky_search():
        """搜索工具：模拟前 2 次因限流抛错，第 3 次调用成功"""
        call_counts["flaky_search"] += 1
        if call_counts["flaky_search"] < 3:
            raise ConnectionError("Rate limit exceeded")
        return ["doc1", "doc2"]

    def mock_timeout_db():
        """数据库工具：持续超时，每次调用均抛出异常"""
        call_counts["timeout_db"] += 1
        raise TimeoutError("Read timed out")

    def mock_slow_fail():
        """耗时且失败的任务：单次耗时 0.08 秒后抛出参数错误"""
        call_counts["slow_fail"] += 1
        time.sleep(0.08)
        raise ValueError("Invalid params")

    def mock_fast_succ():
        """轻量级任务：几乎瞬间成功完成"""
        return "fast_result"

    def mock_sleep_block():
        """固定耗时任务：用于校验并发上限槽位控制"""
        time.sleep(0.1)
        return "ok"

    return {
        "counts": call_counts,
        "calc": mock_calc,
        "flaky_search": mock_flaky_search,
        "timeout_db": mock_timeout_db,
        "slow_fail": mock_slow_fail,
        "fast_succ": mock_fast_succ,
        "sleep_block": mock_sleep_block,
    }


def main():
    solution = Solution()
    mocks = build_mock_tools()

    print("=" * 65)
    print("Agent 工具并行执行器 (Agent Tool Batch Executor) - 测试运行")
    print("=" * 65)

    # 用例 1: 失败后重试并在限额内成功
    print("\n[用例 1] 运行示例 1：重试并在配额内成功...")
    case1_tasks = [
        {"id": "calc", "tool": mocks["calc"], "maxRetries": 1},
        {"id": "search", "tool": mocks["flaky_search"], "maxRetries": 2}
    ]
    res1 = solution.batchExecuteTools(case1_tasks, maxConcurrency=2)
    for r in res1:
        print("  ->", r)

    assert res1 is not None, "函数未返回结果！"
    assert res1[0] == {"id": "calc", "status": "success", "result": 42, "attempts": 1}
    assert res1[1] == {"id": "search", "status": "success", "result": ["doc1", "doc2"], "attempts": 3}
    assert mocks["counts"]["flaky_search"] == 3
    print("  ✓ 用例 1 通过断言")

    # 用例 2: 重试耗尽最终标记为 error
    print("\n[用例 2] 运行示例 2：重试耗尽判定为失败...")
    case2_tasks = [
        {"id": "query_db", "tool": mocks["timeout_db"], "maxRetries": 1}
    ]
    res2 = solution.batchExecuteTools(case2_tasks, maxConcurrency=1)
    for r in res2:
        print("  ->", r)

    assert res2[0]["id"] == "query_db"
    assert res2[0]["status"] == "error"
    assert res2[0]["attempts"] == 2
    assert "Read timed out" in res2[0]["error"]
    assert mocks["counts"]["timeout_db"] == 2
    print("  ✓ 用例 2 通过断言")

    # 用例 3: maxRetries=0 边界与乱序完成时的严格保序
    print("\n[用例 3] 运行边界：0 重试边界与乱序执行结果保序...")
    case3_tasks = [
        {"id": "task_0_slow", "tool": mocks["slow_fail"], "maxRetries": 0},
        {"id": "task_1_fast", "tool": mocks["fast_succ"], "maxRetries": 1}
    ]
    res3 = solution.batchExecuteTools(case3_tasks, maxConcurrency=2)
    for r in res3:
        print("  ->", r)

    assert [r["id"] for r in res3] == ["task_0_slow", "task_1_fast"], "结果顺序与输入 tasks 不一致！"
    assert res3[0]["status"] == "error" and res3[0]["attempts"] == 1
    assert res3[1]["status"] == "success" and res3[1]["attempts"] == 1
    print("  ✓ 用例 3 通过断言")

    # 用例 4: 并发槽位上限与耗时校验
    print("\n[用例 4] 运行并发约束：4 个耗时 0.1s 任务，并发限制 2...")
    case4_tasks = [
        {"id": f"t_{i}", "tool": mocks["sleep_block"], "maxRetries": 0}
        for i in range(4)
    ]
    t_start = time.perf_counter()
    res4 = solution.batchExecuteTools(case4_tasks, maxConcurrency=2)
    elapsed = time.perf_counter() - t_start

    print(f"  实际总耗时: {elapsed:.3f}s (理论耗时约 0.20s)")
    assert 0.18 <= elapsed <= 0.35, f"并发度控制异常，实测耗时为 {elapsed:.3f}s"
    assert len(res4) == 4
    print("  ✓ 用例 4 通过断言")

    # 用例 5: 空输入边界
    print("\n[用例 5] 运行边界：空任务列表输入...")
    res5 = solution.batchExecuteTools([], maxConcurrency=4)
    print("  空输入返回:", res5)
    assert res5 == []
    print("  ✓ 用例 5 通过断言")

    print("\n" + "=" * 65)
    print("All test cases passed! (恭喜，所有测试用例已全部通过)")
    print("=" * 65)


if __name__ == "__main__":
    main()
