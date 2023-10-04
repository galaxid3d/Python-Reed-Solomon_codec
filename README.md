# Python-Reed-Solomon_codec
Script "Reed–Solomon_codec" start create by 11.2020

Script purpose: helps in the development of the [Reed-Solomon codec](https://en.wikipedia.org/wiki/Reed–Solomon_error_correction).

> [!NOTE]\
> The Reed-Solomon code (15, 9) is defined over the field *GF(2⁴)*, *p(x) = x⁴ + x + 1*.
>
> Generative polynomial of the Reed-Solomon code:
*G(x) = (x-α³)⋅(x-α⁴)⋅(x-α⁵)⋅(x-α⁶)⋅(x-α⁷)⋅(x-α⁸)*.

#### Main stages of calculations:
*   Classic algorithms for hard decoding of Reed-Solomon codes
*   Development of a Reed-Solomon decoder syndrome calculator
*   Finding polynomial coefficients of error locators using the Berlekamp-Massey method
*   Finding the roots of the error locator equation using Chen's method
*   Calculating the value of erroneous symbols
*   Error correction.

You can set individual word parameters for the Reed-Solomon code (*x¹⁴* - *x⁰*).

You can specify errors for the Reed-Solomon code: the position of *x* and the value of *α* itself.

---

Назначение скрипта: помогает в разработке [кодека Рида-Соломона](https://ru.wikipedia.org/wiki/Код_Рида_—_Соломона).

> [!NOTE]\
> Код Рида-Соломона (15, 9) определён над полем *GF(2⁴)*, *p(x) = x⁴ + x + 1*.
>
> Порождающий многочлен кода Рида-Соломона:
*G(x) = (x-α³)⋅(x-α⁴)⋅(x-α⁵)⋅(x-α⁶)⋅(x-α⁷)⋅(x-α⁸)*.

#### Основные этапы вычислений:
*   Классические алгоритмы жёсткого декодирования кодов Рида-Соломона
*   Разработка вычислителя синдрома декодера Рида-Соломона
*   Поиск коэффициентов полинома локаторов ошибок с помощью метода Берлекэмпа-Мэсси
*   Поиск корней уравнения локаторов ошибок с использованием метода Ченя
*   Вычисление значений ошибочных символов
*   Исправление ошибок.

Вы можете задать индивидуальные параметры слова для кода Рида-Соломона (*x¹⁴* - *x⁰*).

Вы можете указать ошибки для кода Рида-Соломона: позицию *x* и само значение ошибки *α*.

Структура файла для считывания начальных условий:

Вариант №<номер>

<code> 9, 11,  7,  0,  z,  7,  4,  3,  1,  z,  7,  3, 14, 11,  8
 4,  8,  2,  1
</code>
 
indexes help:

<code>14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0
 6,  5,  4,  3,  2,  1,  0
Первый полином - данное по варианту слово без внесённых ошибок
Позиции вносимых ошибок (x). Значения вносимых ошибок (альфа)
</code>
