# Library file for Lab 5 import
# I had chatgpt put all the code together and remove commenting for the sake of minimizing tedious work 
# of putting this matrix_lib.py file together myself. Since everything was already made, this seems fair.

class matrix:
    def __init__(self, a, b=None):
        if b is not None:
            n = a
            m = b

            if not (isinstance(n, int) and isinstance(m, int)):
                raise TypeError("matrix(n,m): n and m must be integer values")
            if n <= 0 or m <= 0:
                raise ValueError("matrix(n,m): n and m must be positive values")

            self.data = []
            for i in range(n):
                row = []
                for j in range(m):
                    row.append(0.0)
                self.data.append(row)
            return

        L = a

        if not isinstance(L, list) or len(L) == 0:
            raise ValueError("Must be list of lists")

        for row in L:
            if not isinstance(row, list):
                raise ValueError("Each row must be a list")

        row_len = len(L[0])
        for row in L:
            if len(row) != row_len:
                raise ValueError("Rows must have same length")

        self.data = []
        for row in L:
            new_row = []
            for value in row:
                new_row.append(float(value))
            self.data.append(new_row)

    def __repr__(self):
        return str(self.data)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            r, c = key

            if isinstance(r, int) and isinstance(c, int):
                return self.data[r][c]

            if isinstance(r, int):
                rows = [self.data[r]]
            else:
                rows = self.data[r]

            if isinstance(c, int):
                return matrix([[row[c]] for row in rows])
            else:
                return matrix([row[c] for row in rows])

        if isinstance(key, slice):
            return matrix([row[:] for row in self.data[key]])

        return self.data[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            i, j = key
            self.data[i][j] = float(value)
            return

        if isinstance(key, slice):
            if isinstance(value, matrix):
                src = value.data
            else:
                src = value

            if not isinstance(src, list) or len(src) == 0:
                raise ValueError("Invalid source")

            row_len = len(src[0])
            for row in src:
                if len(row) != row_len:
                    raise ValueError("Invalid source")

            if len(src) != len(self.data) or row_len != len(self.data[0]):
                raise ValueError("Size mismatch")

            for i in range(len(self.data)):
                for j in range(len(self.data[0])):
                    self.data[i][j] = float(src[i][j])
            return

    def shape(self):
        return (len(self.data), len(self.data[0]))

    def transpose(self):
        return matrix([list(col) for col in zip(*self.data)])

    def row(self, n):
        if not isinstance(n, int):
            raise TypeError("row(n): n needs to be an integer value")
        if n < 0 or n >= len(self.data):
            raise IndexError("row(n): n is out of range")
        return matrix([self.data[n][:]])

    def column(self, n):
        if not isinstance(n, int):
            raise TypeError("column(n): n must be an integer value")
        if n < 0 or n >= len(self.data[0]):
            raise IndexError("column(n): n is out of range")
        col = []
        for i in range(len(self.data)):
            col.append([self.data[i][n]])
        return matrix(col)

    def to_list(self):
        out = []
        for row in self.data:
            out.append(row[:])
        return out

    def block(self, n_0, n_1, m_0, m_1):
        n, m = self.shape()

        if n_0 < 0 or n_1 > n or n_0 > n_1:
            raise IndexError("block: row bounds are out of range")
        if m_0 < 0 or m_1 > m or m_0 > m_1:
            raise IndexError("block: column bounds are out of range")

        return matrix([row[m_0:m_1] for row in self.data[n_0:n_1]])

    def scalarmul(self, c):
        out = []
        for row in self.data:
            new_row = []
            for value in row:
                new_row.append(float(value) * float(c))
            out.append(new_row)
        return matrix(out)

    def add(self, N):
        if not isinstance(N, matrix):
            raise TypeError("add(N): N must be a matrix insttance")
        if self.shape() != N.shape():
            raise ValueError("add(N): matrix size mismatch")

        out = []
        for i in range(len(self.data)):
            new_row = []
            for j in range(len(self.data[0])):
                new_row.append(self.data[i][j] + N.data[i][j])
            out.append(new_row)
        return matrix(out)

    def sub(self, N):
        if not isinstance(N, matrix):
            raise TypeError("sub(N): N must be a matrix insttance")
        if self.shape() != N.shape():
            raise ValueError("sub(N): matrix size mismatch")

        out = []
        for i in range(len(self.data)):
            new_row = []
            for j in range(len(self.data[0])):
                new_row.append(self.data[i][j] - N.data[i][j])
            out.append(new_row)
        return matrix(out)

    def mat_mult(self, N):
        if not isinstance(N, matrix):
            raise TypeError("mat_mult(N): N must be a matrix insttance")

        n, m = self.shape()
        n2, m2 = N.shape()

        if m != n2:
            raise ValueError("mat_mult(N): size mismatch (inner dimensions must match)")

        out = []
        for i in range(n):
            new_row = []
            for j in range(m2):
                s = 0.0
                for k in range(m):
                    s = s + self.data[i][k] * N.data[k][j]
                new_row.append(s)
            out.append(new_row)
        return matrix(out)

    def element_mult(self, N):
        if not isinstance(N, matrix):
            raise TypeError("element_mult(N): N must be a matrix insttance")
        if self.shape() != N.shape():
            raise ValueError("element_mult(N): matrix size mismatch")

        out = []
        for i in range(len(self.data)):
            new_row = []
            for j in range(len(self.data[0])):
                new_row.append(self.data[i][j] * N.data[i][j])
            out.append(new_row)
        return matrix(out)

    def equals(self, N):
        if not isinstance(N, matrix):
            return False
        if self.shape() != N.shape():
            return False

        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] != N.data[i][j]:
                    return False
        return True

    def __rmul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return self.scalarmul(scalar)
        return NotImplemented

    def __mul__(self, operand):
        if isinstance(operand, (int, float)):
            return self.scalarmul(operand)
        if isinstance(operand, matrix):
            return self.mat_mult(operand)
        return NotImplemented

    def __add__(self, other_matrix):
        if isinstance(other_matrix, matrix):
            return self.add(other_matrix)
        return NotImplemented

    def __sub__(self, other_matrix):
        if isinstance(other_matrix, matrix):
            return self.sub(other_matrix)
        return NotImplemented

    def __eq__(self, other_matrix):
        return self.equals(other_matrix)


def constant(n, m, c):
    if not (isinstance(n, int) and isinstance(m, int)):
        raise TypeError("constant(n,m,c): n and m must be integer values")
    if n <= 0 or m <= 0:
        raise ValueError("constant(n,m,c): n and m must be positive values")

    X = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(float(c))
        X.append(row)
    return matrix(X)


def zeros(n, m):
    return constant(n, m, 0.0)


def ones(n, m):
    return constant(n, m, 1.0)


def eye(n):
    if not isinstance(n, int):
        raise TypeError("eye(n): n must be of an integer value")
    if n <= 0:
        raise ValueError("eye(n): n must be a positive value")

    Y = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        Y.append(row)
    return matrix(Y)