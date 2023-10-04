# 12.11.2020 by galaxid3d
# Вычисляет коды Рида-Соломона

row_str = ""
col_str = "	"
isDrawTable = 0  # выводить таблицы удобные для просмотра (или чтобы их можно было копировать)
if isDrawTable:
    row_str = "_"
    col_str = "|"
z = '0'  # символ нуля
alphaSymbol = 'α'

# Galois field (поле Галуа) для p(x) = x⁴ + x + 1
GF = [[z, 4, 8, 14, 1, 10, 13, 9, 2, 7, 5, 12, 11, 6, 3],
      [4, z, 5, 9, 0, 2, 11, 14, 10, 3, 8, 6, 13, 12, 7],
      [8, 5, z, 6, 10, 1, 3, 12, 0, 11, 4, 9, 7, 14, 13],
      [14, 9, 6, z, 7, 11, 2, 4, 13, 1, 12, 5, 10, 8, 0],
      [1, 0, 10, 7, z, 8, 12, 3, 5, 14, 2, 13, 6, 11, 9],
      [10, 2, 1, 11, 8, z, 9, 13, 4, 6, 0, 3, 14, 7, 12],
      [13, 11, 3, 2, 12, 9, z, 10, 14, 5, 7, 1, 4, 0, 8],
      [9, 14, 12, 4, 3, 13, 10, z, 11, 0, 6, 8, 2, 5, 1],
      [2, 10, 0, 13, 5, 4, 14, 11, z, 12, 1, 7, 9, 3, 6],
      [7, 3, 11, 1, 14, 6, 5, 0, 12, z, 13, 2, 8, 10, 4],
      [5, 8, 4, 12, 2, 0, 7, 6, 1, 13, z, 14, 3, 9, 11],
      [12, 6, 9, 5, 13, 3, 1, 8, 7, 2, 14, z, 0, 4, 10],
      [11, 13, 7, 10, 6, 14, 4, 2, 9, 8, 3, 0, z, 1, 5],
      [6, 12, 14, 8, 11, 7, 0, 5, 3, 10, 9, 4, 1, z, 2],
      [3, 7, 13, 0, 9, 12, 8, 1, 6, 4, 11, 10, 5, 2, z]]
width = len(str(len(GF))) + 1;
widthChen = width if width > 4 else 5
Mult = ["0001", "0010", "0100", "1000", "0011", "0110", "1100", "1011", "0101", "1010", "0111", "1110", "1111", "1101",
        "1001"]  # слагаемые для получения нужной степени для умножителя

def read_file_poly(s):  # конвертирует список строк с файла в числа
    for i in range(len(s)):
        if s[i].strip() == 'z':
            s[i] = z
        else:
            s[i] = int(s[i])
    return s


def get_power(number):  # возвращает символ верхнего индекса для числа
    powers = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    if number == z:
        return powers[0]
    else:
        s = ""
        for i in str(number):
            if i == "-":
                s += '⁻'
            else:
                s += powers[int(i)]
        return s


def get_index(number):  # возвращает символ нижнего индекса для числа
    indexes = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
    if number == z: return indexes[0]
    s = ""
    for i in str(number): s += '₋' if i == "-" else indexes[int(i)]
    return s


def get_alpha(alpha, isOne=False, isPrintZero=False, isPrintOne=False, isPowerSymbols=True,
             i=1):  # вернёт строку альфа в степени или z
    if alpha == z:
        if isPrintZero:
            return z
        else:
            return ""
    if alpha == 0:
        if isOne and (i == 0): return "1"
        if not isPrintZero and (i != 0): return ""
    res = alphaSymbol
    if (alpha != 1) or isPrintOne:
        if isPowerSymbols:
            res += get_power(alpha)
        else:
            res += "^" + str(alpha)
    return res


def get_poly(alpha, xPowers=[], isOne=False, isPrintZero=False, isPrintOne=False,
            isPowerSymbols=True):  # вернёт строку для полинома
    res = []
    if xPowers == []: xPowers = [(len(alpha) - 1 - i) for i in range(len(alpha))]
    for i in range(len(alpha)):
        s = ""
        if (alpha[i] != z):
            if type(alpha[i]) == list:
                tmp = []
                for j in range(len(alpha[i])):
                    if (alpha[i][j] != z) or (xPowers[i] == 0) or isPrintOne:
                        tmp.append(get_alpha(alpha[i][j], isOne, isPrintZero, isPrintOne, isPowerSymbols, 0))
                s += "(" + " + ".join(tmp) + ")"
            else:
                s += get_alpha(alpha[i], isOne, isPrintZero, isPrintOne, isPowerSymbols, len(alpha) - 1 - i)
        elif isPrintZero:
            s += "0" + '∙'
        if ((xPowers[i] != 0) and (alpha[i] != z)) or isPrintZero:
            s += "x"
            if (xPowers[i] != 1) or isPrintOne:
                if isPowerSymbols:
                    s += get_power(xPowers[i])
                else:
                    s += "^" + str(xPowers[i])
        if s != "": res.append(s)
    return " + ".join(res)


def get_str_list(lst, symbol, offset=1, isInverse=False, isOne=False, isPrintZero=True, isPrintOne=False,
               isPowerSymbols=True):
    res = ""
    arr = list(lst)
    if isInverse: arr.reverse()
    for i in range(len(arr)):
        res += symbol + get_index(i + offset) + " = " + get_alpha(arr[i], isOne, isPrintZero, isPrintOne,
                                                                isPowerSymbols) + (", " if i + 1 < len(arr) else "")
    return res


###############
### Program ###
###############
import os

if os.path.isfile('R-S_Data.txt'):
    f = open('R-S_Data.txt', 'r')
    varNumberFull = int(f.readline()[9:])
    varNumber = varNumberFull % len(GF)
    I_x = read_file_poly(list(map(str, f.readline().split(","))))
    errors = read_file_poly(list(map(str, f.readline().split(","))))
    f.close()
else:
    # Номер варианта
    varNumberFull = 18
    varNumber = varNumberFull % len(GF)
    # Полином для деления (альфы), т.е. исходное слово по варианту
    I_x = [5, 9, 2, 13, 11, 7, 9, 3, 0, 4, 4, 8, 8, 5, 9]
    # Позиции и значения вносимых ошибок (сначала идут x, вторая половина списка - альфы)
    errors = [14, 10, 1, 2]
isDeterminantsMethod = (varNumberFull % 2) != 0
G_x = [i % len(GF) for i in range(varNumber, varNumber + 6)]
print("Исходные данные:"'\n'"   Вариант №", varNumberFull)
s = ""
for i in range(len(G_x)): s += "(x-" + get_alpha(G_x[i], False, True) + ")"
print("   G(x) =", s)
print("   I(x) =", get_poly(I_x))
s = ""
for i in range(len(errors) >> 1):
    s += "x" + get_index(errors[i]) + " | " + get_alpha(errors[i + (len(errors) >> 1)], False, True)
    if i + 1 < len(errors) >> 1: s += "; "
print("   Ошибки =", s)
if isDeterminantsMethod:
    print("   Определительный метод вычисления Λ(x)")
else:
    print("   Алгоритм Берлекэмпа-Мэсси вычисления Λ(x)")


def get_sum_field(a, b):  # вернёт сумму двух альфа в поле Галуа
    aa = a;
    bb = b
    if a == z:
        return b if b != z else z
    elif b == z:
        return a
    if aa < 0: aa = abs(len(GF) + aa) % len(GF)
    if bb < 0: bb = abs(len(GF) + bb) % len(GF)
    return GF[aa % len(GF)][bb % len(GF)]


def get_sum(a, b):  # вернёт сумму двух чисел (по модулю размера поля)
    aa = a;
    bb = b
    if (aa == z) or (bb == z): return z
    if aa < 0: aa = (len(GF) + aa) % len(GF)
    if bb < 0: bb = (len(GF) + bb) % len(GF)
    return (aa + bb) % len(GF)


def get_sums_field(summands):  # складывает список нескольких чисел в поле
    summa = summands[0]
    for i in range(1, len(summands)): summa = get_sum_field(summa, summands[i])
    return summa


def get_sums(summands):  # складывает список нескольких чисел
    summa = summands[0]
    for i in range(1, len(summands)): summa = get_sum(summa, summands[i])
    return summa


def get_pow(a, power):  # возводит альфа в степень
    if a == z: return z
    return a * power


def get_poly_mult_X(Poly, X):  # в полиноме вместо x ставит число
    res = [0 for i in range(len(X))]
    summands = [Poly[len(Poly) - 1] for i in range(len(Poly))]  # слагаемые для полинома
    for j in range(len(X)):
        for i in range(len(Poly) - 1): summands[i] = get_sum(Poly[i], get_pow(X[j], len(Poly) - 1 - i))
        res[j] = get_sums_field(summands)
    return res


def get_prim_poly(a, b, c, d, e, f):  # получает примитивный полином после раскрытия скобок
    g_x = [0 for i in range(7)]  # операции "+" и "-" равносильны в двоичном поле
    g_x[1] = get_sums_field([a, b, c, d, e, f])
    g_x[2] = get_sums_field(
        [get_sums([a, b]), get_sums([a, c]), get_sums([a, d]), get_sums([a, e]), get_sums([a, f]), get_sums([b, c]),
         get_sums([b, d]), get_sums([b, e]), get_sums([b, f]), get_sums([c, d]), get_sums([c, e]), get_sums([c, f]),
         get_sums([d, e]), get_sums([d, f]), get_sums([e, f])])
    g_x[3] = get_sums_field(
        [get_sums([a, b, c]), get_sums([a, b, d]), get_sums([a, b, e]), get_sums([a, b, f]), get_sums([a, c, d]),
         get_sums([a, c, e]), get_sums([a, c, f]), get_sums([a, d, e]), get_sums([a, d, f]), get_sums([a, e, f]),
         get_sums([b, c, d]), get_sums([b, c, e]), get_sums([b, c, f]), get_sums([b, d, e]), get_sums([b, d, f]),
         get_sums([b, e, f]), get_sums([c, d, e]), get_sums([c, d, f]), get_sums([c, e, f]), get_sums([d, e, f])])
    g_x[4] = get_sums_field([get_sums([a, b, c, d]), get_sums([a, b, c, e]), get_sums([a, b, c, f]), get_sums([a, b, d, e]),
                           get_sums([a, b, d, f]), get_sums([a, b, e, f]), get_sums([a, c, d, e]), get_sums([a, c, d, f]),
                           get_sums([a, c, e, f]), get_sums([a, d, e, f]), get_sums([b, c, d, e]), get_sums([b, c, d, f]),
                           get_sums([b, c, e, f]), get_sums([b, d, e, f]), get_sums([c, d, e, f])])
    g_x[5] = get_sums_field(
        [get_sums([a, b, c, d, e]), get_sums([a, b, c, d, f]), get_sums([a, b, c, e, f]), get_sums([a, b, d, e, f]),
         get_sums([a, c, d, e, f]), get_sums([b, c, d, e, f])])
    g_x[6] = get_sums([a, b, c, d, e, f])
    return g_x


def get_division(divisible, divisor, isPrint=False):  # вернёт [0-Частное, 1-Остаток]
    xDivisor = [i for i in range(len(divisor) - 1, -1, -1)]  # степени x
    quotient = [[], []]  # 0-alpha, 1-x
    currentPoly = [[divisible[i] for i in range(len(divisor))], [len(divisor) + i for i in range(len(divisor), 0, -1)]]
    currentDiv = [[0 for i in range(len(divisor))], [0 for i in range(len(divisor))]]
    for j in range(len(divisible)):
        if currentPoly[0][0] == z:
            quotient[0].append(z)
        else:
            quotient[0].append(get_sum(currentPoly[0][0], -divisor[0]))
        quotient[1].append(get_sum(currentPoly[1][0], -xDivisor[0]))
        for i in range(len(divisor)):
            currentDiv[0][i] = get_sum(quotient[0][j], divisor[i])
            currentDiv[1][i] = get_sum(quotient[1][j], xDivisor[i])
        currentResult = [[0 for i in range(len(divisor))], [currentPoly[1][i] - 1 for i in range(len(divisor))]]
        for i in range(1, len(divisor)): currentResult[0][i - 1] = get_sum_field(currentPoly[0][i], currentDiv[0][i])
        if len(divisor) + j < len(divisible):
            currentResult[0][len(divisor) - 1] = divisible[len(divisor) + j]
        else:
            currentResult[0][len(divisor) - 1] = z
        if j + 1 == len(divisible):
            currentResult = [currentResult[0][:len(currentResult[0]) - 1], currentResult[1][:len(currentResult[1]) - 1]]
        if isPrint:
            print("Step =", j)
            print("quotient =     ", get_poly(quotient[0], quotient[1], False, True, True))
            print("currentPoly =  ", get_poly(currentPoly[0], currentPoly[1], False, True, True))
            print("currentDiv =   ", get_poly(currentDiv[0], currentDiv[1], False, True, True))
            print("currentResult =", get_poly(currentResult[0], currentResult[1], False, True, True))
        currentPoly = list(currentResult)
    return [quotient, currentResult[0]]


def get_Gorner_table(G_x, r_i):
    gorner = [["".center(width) for i in range(len(G_x) * 2 + 1)] for i in range(len(r_i) + 2)]
    gorner[0][len(G_x) * 2] = "r"'ᵢ'.center(width)
    for i in range(len(r_i)): gorner[i + 2][len(G_x) * 2] = r_i[i]
    for i in range(len(G_x)):
        gorner[0][i * 2] = ("S" + get_index(i + 1)).center(width)
        gorner[1][i * 2] = '∑'.center(width)
        gorner[1][i * 2 + 1] = ('×' + get_alpha(G_x[i], False, True)).center(width)
        gorner[2][i * 2] = r_i[0]
        gorner[2][i * 2 + 1] = get_sum(r_i[0], G_x[i])
    for j in range(1, len(r_i)):
        for i in range(len(G_x)):
            gorner[2 + j][i * 2] = get_sum_field(r_i[j], gorner[1 + j][i * 2 + 1])
            gorner[2 + j][i * 2 + 1] = get_sum(gorner[2 + j][i * 2], G_x[i])
    return gorner


def print_Gorner_table(gorner, isHide=True):
    if isDrawTable: print(row_str + row_str * 2 * (2 + len("".join(gorner[0]))) + '\n' + col_str, end="")
    for i in range((len(gorner[0]) >> 1) + 1): print(gorner[0][i * 2].center(11 if i < len(gorner[0]) >> 1 else 9),
                                                     end=col_str)
    if isDrawTable:
        print('\n' + (col_str + row_str * 11) * len(G_x) + col_str + "         " + col_str + '\n' + col_str, end="")
    else:
        print()
    for j in range(1, len(gorner)):
        for i in range(len(gorner[j])):
            if j == 1:
                s = gorner[j][i]
            else:
                s = get_alpha(gorner[j][i], False, True, True)
                if isHide and (j + 1 == len(gorner)) and (i % 2 == 1): s = ""
            print(s.center(4 if i + 1 < len(gorner[j]) else 8), end=" " + col_str)
        if isDrawTable:
            print('\n' + (col_str + row_str * 5) * (len(G_x) << 1) + col_str + row_str * 9 + col_str + '\n', end="")
            if j + 1 < len(gorner): print(end=col_str)
        else:
            print()


def get_multiplier(power, isPrint=True):
    c = [[] for i in range((len(G_x) >> 1) + 1)]  # слагаемые при обобщении
    for j in range(len(c)):
        k = get_sum(len(c) - 1 - j, power)
        for i in range(len(Mult[k])):
            if Mult[k][i] != '0': c[j].append(len(Mult[k]) - 1 - i)
    C = [[] for i in range((len(G_x) >> 1) + 1)]  # слагаемые при объединении
    C_str = [[] for i in range((len(G_x) >> 1) + 1)]
    for j in range(len(C)):
        for i in range(len(c)):
            for cc in c[i]:
                if len(c) - 1 - cc == j:
                    C[j].append(len(c) - 1 - i)
                    C_str[j].append(get_alpha(len(c) - 1 - i, False, True))
                    break
    if isPrint:
        print("c = a∙" + alphaSymbol + get_power(power))
        s = ""
        for i in range(len(C) - 1, -1, -1):
            s += (('t' + (get_power(i) if i > 1 else "")) if i > 0 else "") + alphaSymbol + get_index(i) + (
                " + " if i > 0 else "")
        print(alphaSymbol + " = t; a = " + s)
        s = ""
        for i in range(len(C) - 1, -1, -1):
            s += (('t' + (get_power(get_sum(i, power)) if get_sum(i, power) > 0 else "")) if get_sum(i, power) > 0 else "") \
                 + alphaSymbol + get_index(i) + (" + " if i > 0 else "")
        print("c = " + s, end=" = ")
        s = ""
        for j in range(len(c)):
            s += alphaSymbol + get_index(len(c) - 1 - j) + ("(" if len(c[j]) > 1 else "")
            for i in range(len(c[j])): s += 't' + get_power(c[j][i]) + (" + " if i + 1 < len(c[j]) else "")
            s += (")" if len(c[j]) > 1 else "")
            s += " + " if j + 1 < len(c) else ""
        print(s + ';')
        s = ""
        for j in range(len(C)):
            s += (("t" + (get_power(len(C) - 1 - j) if j + 2 < len(C) else "")) if j + 1 < len(C) else "") \
                 + ("(" if len(C[j]) > 1 else "")
            for i in range(len(C[j])): s += alphaSymbol + get_index(C[j][i]) + (" + " if i + 1 < len(C[j]) else "")
            s += (")" if len(C[j]) > 1 else "")
            s += " + " if j + 1 < len(C) else ""
        print("c = " + s)
    return [C, C_str]  # вернёт компоненты умножителя: 0-числами, 1-альфа в степени


def get_dets_method(S_x, isPrint=True):
    def getMatrix_n(n):
        matrix = [[i for i in range(n)] for i in range(n)]
        S_str = [[i + 1 for i in range(n)] for i in range(n)]  # строковая матрица для вывода индексов
        for j in range(n):
            for i in range(n):
                matrix[j][i] = S_x[matrix[j][i] + j]
                S_str[j][i] = ('S' + get_index(S_str[j][i] + j)).ljust(width)
        return [matrix, S_str]

    def printMatrix(S):
        for j in range(len(S[0])):
            s = "| = |" if j == len(S[0]) >> 1 else "|   |"
            for i in range(len(S[0][j])):
                s += (get_alpha(S[0][j][i], False, True)).ljust(width) + (" " if i + 1 < len(S[0][0]) else "")
            print(('S''̅' + get_index(len(S[0])) + " = |" if j == len(S[0]) >> 1 else "     |") + " ".join(
                map(str, S[1][j])) + s + '|')

    def strMatrixSummands(S):
        res = ['' for i in range(len(S) << 1 if len(S) == 3 else len(S))]
        if len(S) == 3:
            s = [[S[0][0], S[1][1], S[2][2]], [S[0][1], S[1][2], S[2][0]], [S[1][0], S[2][1], S[0][2]],
                 [S[2][0], S[1][1], S[0][2]], [S[0][0], S[1][2], S[2][1]], [S[0][1], S[1][0], S[2][2]]]
        elif len(S) == 2:
            s = [[S[0][0], S[1][1]], [S[0][1], S[1][0]]]
        else:
            s = [[S[0][0]]]
        for j in range(len(res)):
            for i in range(len(s[0])): res[j] += get_alpha(s[j][i], False, True, True)
        return res

    S_x.reverse()
    L_x = [0 for i in range((len(G_x) >> 1) + 1)]
    for i in range(len(G_x) >> 1, 0, -1):
        S = getMatrix_n(i)
        if i == 3:
            s = get_sums_field(
                [get_sums([S[0][0][0], S[0][1][1], S[0][2][2]]), get_sums([S[0][0][1], S[0][1][2], S[0][2][0]]),
                 get_sums([S[0][1][0], S[0][2][1], S[0][0][2]]), get_sums([S[0][2][0], S[0][1][1], S[0][0][2]]),
                 get_sums([S[0][0][0], S[0][1][2], S[0][2][1]]), get_sums([S[0][0][1], S[0][1][0], S[0][2][2]])])
        elif i == 2:
            s = get_sums_field([get_sum(S[0][0][0], S[0][1][1]), get_sum(S[0][0][1], S[0][1][0])])
        else:
            s = S[0][0][0]
        if isPrint:
            printMatrix(S)
            print('S''̅' + get_index(i) + " = " + " + ".join(map(str, strMatrixSummands(S[0]))) + " = "
                  + get_alpha(s, False, True) + (" > 0" if s != z else "") + '\n')
        if s != z:
            break
        else:
            L_x[len(L_x) - 1 - i] = z
    if s != z:
        if len(S[0]) == 1:
            L_x[len(L_x) - 2] = get_sum(S_x[1], -s)
            if isPrint:
                print('λ' + get_index(1) + S[1][0][0] + "=", 'S' + get_index(2))
                print('λ' + get_index(1) + get_alpha(S[0][0][0], False, True) + " =",
                      get_alpha(L_x[len(L_x) - 2], False, True))
        elif len(S[0]) == 2:
            if S_x[0] != z:
                L_x[len(L_x) - 2] = get_sum_field(S_x[3], get_sum(get_sum(S_x[2], -S_x[0]), S_x[1]))  # числитель λ1
                L_x[len(L_x) - 2] = get_sum(L_x[len(L_x) - 2],
                                           -get_sum_field(S_x[2], get_sum(get_sum(S_x[1], -S_x[0]), S_x[1])))  # λ1
                L_x[len(L_x) - 3] = get_sum_field(get_sum(S_x[2], -S_x[0]),
                                                get_sum(get_sum(S_x[1], -S_x[0]), L_x[len(L_x) - 2]))  # λ2
            else:
                L_x[len(L_x) - 2] = get_sum(S_x[2], -S_x[1])  # λ1
                L_x[len(L_x) - 3] = get_sum(get_sum_field(S_x[3], get_sum(get_sum(S_x[2], -S_x[1]), S_x[2])), -S_x[1])  # λ2
            if isPrint:
                print('⎡''λ' + get_index(2) + S[1][0][0] + " + " + 'λ' + get_index(1) + S[1][0][1] + " =",
                      'S' + get_index(3))
                print('⎣''λ' + get_index(2) + S[1][1][0] + " + " + 'λ' + get_index(1) + S[1][1][1] + " =",
                      'S' + get_index(4))
                print()
                print('⎡''λ' + get_index(2) + get_alpha(S[0][0][0], False, True) + " + " + 'λ' + get_index(1) + get_alpha(
                    S[0][0][1], False, True) + " =", get_alpha(S_x[2], False, True))
                print('⎣''λ' + get_index(2) + get_alpha(S[0][1][0], False, True) + " + " + 'λ' + get_index(1) + get_alpha(
                    S[0][1][1], False, True) + " =", get_alpha(S_x[3], False, True))
        else:
            print("РЕШАТЬ НАДО СИСТЕМУ > 2 ПЕРЕМЕННЫХ !!!")
    index = -1
    for i in range(len(L_x)):
        if L_x[i] == z:
            index = i
        else:
            break
    L_x = L_x[index + 1:]
    if isPrint:
        L_x.reverse()
        print(get_str_list(L_x[1:1 + len(S[0])], 'λ'))
        L_x.reverse()
    S_x.reverse()
    return L_x


def get_Berlekamp_Massey(S_x, isPrint=True):
    S_x.reverse()
    L = 0;
    L_x = [0];
    B_x = [0]  # L_x = a^0 = 1; B_x = a^0 = 1
    for r in range(len(G_x)):
        d = [S_x[r]]  # невязка
        for i in range(1, len(L_x)):
            if S_x[r - i] != z: d.append(get_sum(L_x[L - i], S_x[r - i]))
        if isPrint:
            print("r = r + 1 =", r + 1)
            s = ["S" + get_index(r + 1)]
            for i in range(1, len(L_x)): s.append('λ' + get_index(i) + "S" + get_index(r + 1 - i))
            print('Δ' + get_index(r + 1) + " = " + " + ".join(s) + " =", end=" ")
        d = get_sums_field(d)
        if isPrint: print(get_alpha(d, False, True), "" if d == z else "> 0")
        if d == z:
            B_x.append(z)  # домножаем на x
            if isPrint: print("B(x) =", get_poly(B_x, [], True))
        else:
            T_x = list(L_x)
            if len(T_x) < len(B_x) + 1: T_x = [z for i in range(len(B_x) + 1 - len(T_x))] + T_x
            for i in range(len(B_x)):
                T_x[len(T_x) - len(B_x) - 1 + i] = get_sum_field(T_x[len(T_x) - len(B_x) - 1 + i], get_sum(B_x[i], d))
            if isPrint:
                print("T(x) = Λ(x) + Δ" + get_index(r + 1) + "xB(x) =", get_poly(T_x, [], True))
                print("2L", "<=" if L << 1 <= r else ">", "r - 1")
            if L << 1 > r:
                L_x = list(T_x)
                B_x.append(z)
                if isPrint:
                    print("Λ(x) = T(x) =", get_poly(L_x, [], True))
                    print(get_str_list(L_x, 'λ', 0, True, True, True))
                    print("B(x) =", get_poly(B_x, [], True))
            else:
                B_x = [get_sum(i, -d) for i in L_x]
                L_x = list(T_x)
                L = r + 1 - L
                if isPrint:
                    print("B(x) = Δ" + get_index(r + 1) + get_power(-1) + "Λ(x) =", get_poly(B_x, [], True))
                    print("Λ(x) = T(x) =", get_poly(L_x, [], True))
                    print(get_str_list(L_x, 'λ', 0, True, True, True))
                    print("L = r - L = " + str(r + 1) + " - " + str(r + 1 - L) + " =", L)
        if isPrint and (r + 1 < len(G_x)): print()
    if isPrint:
        if L + 1 == len(L_x):
            print("deg(Λ(x)) = L =", L)
        else:
            print("deg(Λ(x))" + (" < " if len(L_x) < L + 1 else " > ") + "L : "
                  + str(len(L_x) - 1) + (" < " if len(L_x) < L + 1 else " > ") + str(L))
    S_x.reverse()
    return L_x


def get_Chen_table(L_x):
    chen = [[z for i in range(len(L_x) + 2)] for i in range(len(GF) + 1)]
    chen[0][0] = "Корни".center(widthChen)
    for i in range(len(L_x)):
        chen[0][i + 1] = ('λ' + get_index(i) + ("x" if i > 0 else "") + (get_power(i) if i > 1 else "")).center(widthChen)
    chen[0][len(chen[0]) - 1] = '∑'.center(widthChen)
    L_x.reverse()
    for j in range(1, len(chen)):
        chen[j][0] = j - 1
        for i in range(len(L_x)): chen[j][i + 1] = get_sum(L_x[i], (j - 1) * i)
        chen[j][len(chen[0]) - 1] = get_sums_field(chen[j][1:len(chen[0]) - 1])
    L_x.reverse()
    return chen


def print_Chen_table(chen):
    if isDrawTable: print(row_str * int(1.44 * len("".join(chen[0]))) + '\n' + col_str, end="")
    for j in range(len(chen)):
        for i in range(len(chen[j])):
            if j == 0:
                s = chen[j][i]
            else:
                s = get_alpha(chen[j][i], i == 1, True, True, True, 0)
            print(s.center(widthChen), end=" " + col_str)
        if isDrawTable:
            print('\n' + (col_str + row_str * 6) * (len(chen[0]) - 1) + col_str + row_str * 6 + col_str + '\n', end="")
            if j + 1 < len(chen): print(end=col_str)
        else:
            print()


def get_Forney(S_x, L_x, X_, X, isPrint=False):
    forney = [0 for i in X]
    Omega_x = [[z] for i in range((len(S_x) - 1) + (len(L_x) - 1))]  # слагаемые от умножения: S(x) * Λ(x) mod x^(2t)
    for j in range(len(S_x) - 1, -1, -1):
        for i in range(len(L_x) - 1, -1, -1):
            if j + i < len(G_x): Omega_x[j + i].append(get_sum(S_x[len(S_x) - 1 - j], L_x[len(L_x) - 1 - i]))
    Omega_x.reverse()
    if isPrint:
        print("b = " + str(varNumberFull) + "; t =", len(G_x) >> 1)
        s = ""
        for j in range(len(Omega_x)):
            if len(Omega_x) - 1 - j >= len(G_x): continue
            tmp_s = ""
            for i in range(1, len(Omega_x[j])):
                if Omega_x[j][i] != z: tmp_s += get_alpha(Omega_x[j][i], False, False, True, True, 0) + " + "
            if (tmp_s != "") and (tmp_s != " + "):
                s += (" + " if j > len(Omega_x) - len(G_x) else "") + ("x" if j + 1 < len(Omega_x) else "") \
                     + (get_power(len(Omega_x) - 1 - j) if j + 2 < len(Omega_x) else "") + (
                         "(" if j + 1 < len(Omega_x) else "") \
                     + tmp_s[:len(tmp_s) - 3] + (")" if j + 1 < len(Omega_x) else "")
        print("Ω(x) =", s, end="")
    for i in range(len(Omega_x)): Omega_x[i] = get_sums_field(Omega_x[i])
    Lambda_x = [L_x[i] if ((len(L_x) - i) % 2) == 0 else z for i in
                range(len(L_x) - 1)]  # формальая производная от Λ(x). Слагаемые с чётной степенью равны нулю
    Lambdas_X = get_poly_mult_X(Lambda_x, X_)  # Λ'(Xi⁻¹)
    Omegas_X = get_poly_mult_X(Omega_x, X_)  # Ω(Xi⁻¹)
    for i in range(len(forney)): forney[i] = get_sum(Omegas_X[i], -get_sum(Lambdas_X[i], get_pow(X[i], varNumberFull - 1)))
    if isPrint:
        print(" =", get_poly(Omega_x))
        print("Λ'(x) =", get_poly(Lambda_x))
        for j in range(len(X)):
            s = ""
            for i in range(len(Omega_x)):
                if Omega_x[i] == z: continue
                if i + 1 == len(Omega_x):
                    s += (" + " if Omega_x[i - 1] != z else "") + get_alpha(Omega_x[i], True, True, True)
                else:
                    s += (" + " if (i > 0) and (Omega_x[i - 1] != z) else "") + get_alpha(Omega_x[i], True, True, True) \
                         + get_alpha(get_pow(X_[j], len(Omega_x) - 1 - i), True, False, True)
            print("Ω(X" + get_index(j + 1) + get_power(-1) + ") = " + s + " = " + get_alpha(Omegas_X[j], True, True))
        for i in range(len(X)):
            s = get_alpha(Omegas_X[i], False, True) + " / (" + get_alpha(Lambdas_X[i], True, True) \
                + "(" + get_alpha(X[i], True, True) + ")" + get_power(varNumberFull - 1) + ")"
            print("Y" + get_index(i + 1) + " = " + s + " = " + get_alpha(forney[i], False, True))
    return forney


print('\n'"Раскрытие скобок G(x):")
g_x = get_prim_poly(G_x[0], G_x[1], G_x[2], G_x[3], G_x[4], G_x[5])
print("   g(x) =", get_poly(g_x))

print('\n'"Деление I(x)∙x⁶ mod g(x) + I(x)∙x⁶:")
divisible = I_x[:len(I_x) - len(g_x) + 1]  # информационные биты
division = get_division(divisible, g_x, False)
print("   I(x) =", get_poly(divisible, [i for i in range(14, 5, -1)]), '\n'"   g(x) =", get_poly(g_x))
print("   Частное =", get_poly(division[0][0], division[0][1]))
print("   Остаток =", get_poly(division[1]))
C_x = sum([[i for i in I_x[:9]], [i for i in division[1]]], [])  # информационные биты и сформированные проверочные
print("   C(x) =", get_poly(C_x))

print('\n'"Вычисление синдромов по схеме Горнера:")
R_x = list(C_x)  # слово с внесёнными ошибками
for i in range(len(errors) >> 1):  # первая половина позиции, через середину - значения
    R_x[len(R_x) - 1 - errors[i]] = get_sum_field(R_x[len(R_x) - 1 - errors[i]], errors[i + (len(errors) >> 1)])
print("   R(x) =", get_poly(R_x))
gorner = get_Gorner_table(G_x, R_x)
print_Gorner_table(gorner, True)
S_x = [gorner[len(gorner) - 1][i * 2] for i in range(len(G_x))];
S_x.reverse()
print("   S(x) =", get_poly(S_x))

print('\n'"Регистр с обратными связями:")
print("   xa" + " -> xa".join(map(get_power, reversed(g_x[1:]))))

print('\n'"Вычисление компонентов умножителя на " + get_alpha(varNumber, False, True) + ":")
c = get_multiplier(varNumber, True)
for i in range(len(c[1])):
    print("c" + get_index(len(c[1]) - 1 - i) + " = " + " + ".join(c[1][i]) + (';' if i + 1 < len(c[1]) else "."))

if isDeterminantsMethod and (
        len(G_x) >> 1) < 4:  # чтобы решал определительным для любого числа ошибок > 3 нужна ф-ия рассчёта определителя размера > 3
    print('\n'"Поиск коэффициентов Определительным методом:")
    L_x = get_dets_method(S_x, True)
else:
    print('\n'"Поиск коэффициентов по алгоритму Берлекэмпа-Мэсси:")
    L_x = get_Berlekamp_Massey(S_x, True)
print("   Λ(x) =", get_poly(L_x, [], True))
if (len(L_x) - 1) * 2 < len(errors): print("ERROR!!!",
                                           "Количество ошибок > " + str(len(G_x) >> 1) + ", их все нельзя исправить")

print('\n'"Вычисление корней многочлена методом Ченя:")
chen = get_Chen_table(L_x)
print_Chen_table(chen)
X_ = []
for j in range(1, len(GF) + 1):
    if chen[j][len(chen[0]) - 1] == z: X_.append(chen[j][0])
s = ""
for i in range(len(X_)): s += "X" + get_index(i + 1) + get_power(-1) + " = " + get_alpha(X_[i], False, True) + (
    ", " if i + 1 < len(X_) else "")
print("   Корни многочлена:", s)
X = [get_sum(len(GF), -X_[i]) for i in range(len(X_))]
s = ""
for i in range(len(X_)):
    s += "X" + get_index(i + 1) + get_power(len(GF)) + get_power("-") + get_power(X_[i]) \
         + " = " + get_alpha(X[i], False, True) + (", " if i + 1 < len(X_) else "")
print("   Локаторы ошибок:", s)

print('\n'"Вычисление ошибочных символов методом Форни:")
Y = get_Forney(S_x, L_x, X_, X, True)
print("   Значения ошибок:", get_str_list(Y, 'Y'))

print('\n'"Исправление ошибок в слове:")
RE_x = list(R_x)  # слово с исправленными ошибками
for i in range(len(X)): RE_x[len(GF) - 1 - X[i]] = get_sum_field(RE_x[len(GF) - 1 - X[i]], Y[i])
E_x = [get_alpha(Y[i], False, True) + "x" + get_power(X[i]) for i in range(len(X))]
s = ""
for i in range(len(E_x)): s += E_x[i] + (" + " if i + 1 < len(E_x) else "")
print("   E(x) =", s)
E_x = list(R_x)
for i in range(len(X)): E_x[len(GF) - 1 - X[i]] = [E_x[len(GF) - 1 - X[i]], Y[i]]
print("   R(x) - E(x) =", get_poly(E_x, ), "=", get_poly(RE_x))
print("   Исходное слово восстановлено верно" if C_x == RE_x else "   Исходное слово не восстановлено. Ошибки!!!")
input()
