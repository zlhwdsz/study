# 给定无序整数数组 nums 和目标值 target，找出数组中两个数字相加等于 target，返回所有(值)不重复二元组，不能重复使用同一个元素(位置)，结果去重(值)。
# 示例：nums = [2,7,11,15,2], target=9 → [[2,7]]

def twosum(nums, target):
    num_indexes = {}
    for i, n in enumerate(nums):
        num_indexes.setdefault(n,[]).append(i)
    d = {}
    for i, n in enumerate(nums):
        diff = target - n
        diff_indexes = num_indexes.get(diff,[])
        if diff == n and len(diff_indexes) > 1:
            d[n] = n
        elif diff_indexes:
            mi, ma =  min(n, diff), max(n, diff)
            d[mi] = ma
    return list(map(list,d.items()))

print(twosum([2,7,11,15,2], 9))
