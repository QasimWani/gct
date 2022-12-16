from typing import Union

# define a new type `ArithmeticInput` that can be either int or float
# Note: you can't do: type('ArithmeticInput', (int, float), {})
# because you're int and float have a common base class which creates lay-out conflict.
ArithmeticInput = Union[int, float]


class Math:
    """Simple class that defines basic numerical operations"""

    def __init__(self) -> None:
        self._buffer = []

    @property
    def buffer(self):
        return self._buffer

    def _add_output_to_buffer(self, result: ArithmeticInput):
        self.buffer.append(result)

    def add(self, op1: ArithmeticInput, op2: ArithmeticInput):
        ans = op1 + op2
        self._add_output_to_buffer(ans)
        return ans

    def sub(self, op1: ArithmeticInput, op2: ArithmeticInput):
        ans = op1 - op2
        self._add_output_to_buffer(ans)
        return ans

    def mul(self, op1: ArithmeticInput, op2: ArithmeticInput):
        ans = op1 * op2
        self._add_output_to_buffer(ans)
        return ans

    def div(self, op1: ArithmeticInput, op2: ArithmeticInput):
        def is_division_by_zero(num):
            if num == 0:
                return True

        if is_division_by_zero(op2):
            return float("inf")

        ans = op1 / op2
        self._add_output_to_buffer(ans)
        return ans

    def output_basic_operations(self, op1: ArithmeticInput, op2: ArithmeticInput):
        assert isinstance(op1, (int, float)), "`op1` Must be either int or float"
        assert isinstance(op2, (int, float)), "`op2` Must be either int or float"
        self.add(op1, op2)
        self.sub(op1, op2)
        self.mul(op1, op2)
        self.div(op1, op2)


if __name__ == "__main__":
    math = Math()
    op1, op2 = 10, 5
    math.output_basic_operations(op1, op2)
    memory = math.buffer
    print(memory)
