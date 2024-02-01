class Solution:
    def predictTheWinner(self, nums) -> bool:

        def helper(nums, left, right, score1, score2, round):
            if left == right:
                return score1 >= score2

            if round % 2 == 0:
                return helper(nums, left + 1, right, score1 + nums[left], score2, round + 1) \
                       or helper(nums, left, right - 1, score1 + nums[right], score2, round + 1)
            else:
                return helper(nums, left + 1, right, score1, score2 + nums[left], round + 1) \
                       and helper(nums, left, right - 1, score1, score2 + nums[right], round + 1)

        return helper(nums, 0, len(nums) - 1, 0, 0, 0)


a = Solution()
print(a.predictTheWinner([1, 5, 2, 4, 6]))
