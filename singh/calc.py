def check_squareness(A):
    if len(A) != len(A[0]):
        raise ArithmeticError("Matrix must be square to inverse.")

def determinant(A, total=0):
    indices = list(range(len(A)))
    
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    for fc in indices:
        As = copy_matrix(A)
        As = As[1:]
        height = len(As)

        for i in range(height):
            As[i] = As[i][0:fc] + As[i][fc+1:]

        sign = (-1) ** (fc % 2)
        sub_det = determinant(As)
        total += A[0][fc] * sign * sub_det

    return total

def check_non_singular(A):
    det = determinant(A)
    if det != 0:
        return det
    else:
        raise ArithmeticError("Singular Matrix!")
        
def zeros_matrix(rows, cols):

    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M

def identity_matrix(n):

    I = zeros_matrix(n, n)
    for i in range(n):
        I[i][i] = 1.0

    return I

def copy_matrix(M):

    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def print_matrix(M):

    for row in M:
        print([round(x,3)+0 for x in row])


def matrix_multiply(A, B):

    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if colsA != rowsB:
        raise ArithmeticError(
            'Number of A columns must equal number of B rows.')
 
    C = zeros_matrix(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total
 
    return C

def check_matrix_equality(A,B, tol=None):

    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            if tol == None:
                if A[i][j] != B[i][j]:
                    return False
            else:
                if round(A[i][j],tol) != round(B[i][j],tol):
                    return False

    return True

def invert_matrix(A, tol=None):


    check_squareness(A)
    check_non_singular(A)


    n = len(A)
    AM = copy_matrix(A)
    I = identity_matrix(n)
    IM = copy_matrix(I)


    indices = list(range(n))
    for fd in range(n): 
        fdScaler = 1.0 / AM[fd][fd]

        for j in range(n): 
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler

        for i in indices[0:fd] + indices[fd+1:]: 
            crScaler = AM[i][fd] 
            for j in range(n): 
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]

    if check_matrix_equality(I,matrix_multiply(A,IM),tol):
        return IM
    else:
        raise ArithmeticError("Matrix inverse out of tolerance.")

A = [[5,4,3,6],[4,3,2,5],[3,2,9,9],[7,8,2,1]]
B = [[2],[5],[4],[10]]

def solve(A, B):
    Inv = invert_matrix(A,9)
    sol = matrix_multiply(Inv, B)
    return sol

print(solve(A, B))