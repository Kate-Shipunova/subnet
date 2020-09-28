СПОСОБ ЗАПУСКА ПРОГРАММЫ:

Запуск кода, принимающего аргументы командной строки, возможен 2 способами:
1. Из PyCharm, при открытом ф-ле subnet.py, необходимо перейти к EditConfigurations -> Parameters, указать входные параметры(имя ф-ла и тип адресов)
через пробел, например: IPv6.txt IPv6, нажать Apply, OK. И запустить код на выполнение нажав 'Run'(зеленая стрелка) или 'Shift+F10'.
2. Запуск можно выполнить через консоль, перейдя в директорию с ф-лом subnet.py и ввести(для IPv4):
>> python subnet.py IPv4.txt IPv4  <Enter>


ОЦЕНКА ВРЕМЕННОЙ ЭФФЕКТИВНОСТИ ИСПОЛЬЗУЕМОГО АЛГОРИТМА:

Функция search_subnet() была запущена дважды с разным набором параметров (для "IPv4" и "IPv6"), затраченное на её выполнении время
для обоих вариантов составляет:

The search_subnet() for "IPv4" takes 0.009838338 sec.
The search_subnet() for "IPv6" takes 0.013274211 sec.

Основным фактором, влияющем на время выполнения кода, является количество считанных из ф-ла IP-адресов (для "IPv4" - 3 шт, 
для "IPv6" - 8 шт), до 7-го шага включительно алгоритм обрабатывает все полученные данные.
При достаточно "грубой" оценки можно сделать вывод, что зависимость времени выполнения от кол-ва считанных данных
прямая пропорциональная - О(n), что в общем случае приемлемо. 


ЛОГИКА:

Чтобы получить минимальную подсеть для заданного набора адресов, необходимо определить маску и адрес сети с нулевыми битами, отведенными под
идентификатор хоста.
Для определения маски выполнен перевод полученных адресов в бинарное представление, далее в цикле определяем количество одинаковых бит с начала адресов -
это число будет маской искомой минимальной подсети. Также, отталкиваясь от этого числа, рассчитывается адрес сети - для чего все последующие биты,
порядок следования которых в полученных адресах выходит за пределы маски, приравниваются "0". Результатом является приведение к требуемому формату записи
подсети исходя из рассчитанных данных.


Алгоритм работы описан с учетом следующих допущений:

- номера шагов в коде соответствуют номерам пунктов алгоритма, описанного в данном ф-ле;
- если какая-либо из проверок на корректность полученных данных не пройдена, то ф-ция завершает
свое выполнение выводом на консоль информации о причине и return None (В алгоритме описаны действия при
успешном прохождении проверок).


АЛГОРИТМ:

1. Работа ф-ции стартует с проверки количества переданных в неё аргументов. 
Исключительно для тестирования основной ф-ции search_subnet() введены позиционные аргументы с заданными по умолчанию значениями == "None", и добавлена проверка значений позиционных аргументов, для возможности переключения на аргументы CLI и обратно.
Для корректной работы это кол-во аргументов CLI должно быть 3, т.к. 1-й аргумент содержит имя программы и не зависит
от передаваемых нами аргументов, а 2 последующих - это имя ф-ла с набором IP-адресов и версия IP.
Если проверка пройдена, то, в основном для большей читабельности кода, вводятся переменные file_name и type_of_ip.
type_of_ip приводится к нижнему регистру, чтобы продолжить выполнение программы независимо от регистра полученной строки с 
типом IP-адресов (м.б. получено "Ipv4", "IPV4", "ipV4" и т.д.).

2. Проверка соответствия полученного типа IP "IPv4" или "IPv6" с помощью ф-ции check_type_of_ip(type_of_ip), ф-ция возвращает bool.
Полученное имя ф-ла тоже можно проверить на существование, но на данном этапе это не обязательно, т.к. при проверке ф-л может
существовать, а в момент открытия - нет.

3. Выполняется открытие и чтения ф-ла с очисткой содержимого строк от '\n' и добавлением в список адресов(каждый адрес
сохраняется цельной строкой).
Предусмотрена обработка возможного исключения, если ф-л с полученным именем не найден по указанному пути или не существует.

4. Происходит разбиение адресов на отдельные октеты/хекстеты, для дальнейшего сравнивания. 
Данный функционал передан вспомогательной ф-ции get_addr_by_octets(arr_with_addr, type_of_ip), что обусловлено формированием 
адресов для "IPv6" по отдельным правилам (замена одного или нескольких 16-тебитных сегментов, состоящих из 0 на '::').
Ф-ции get_addr_by_octets(arr_with_addr, type_of_ip) адреса "IPv4" разбивает на октеты по символу '.', а  "IPv6" - по ':', на месте '::"
будет '', далее определяется кол-во нулевых хекстетов, создается список с нужным кол-вом '0', и выполняется замена '' на список '0'.

5. Проверка корректности полученных адресов - для "IPv4" должно быть 4 октета, значение каждого октета должно находиться в диапозоне 
от 0 до 255 включительно, для "IPv6" - проверка кол-ва хекстетов (8 шт) и их значение от 0 до 'ffff' == 65535. 
Проверка  делигирована вспомогательной ф-ции check_correct_of_addr(addr, type_of_ip), возвращающей буленовское значение.

6. На данном шаге функционал реализован в ф-ции get_mask(arr_with_addr, ip) и заключается в следующем:
весь набор полученных адресов приводится к бинарному виду, проверяется идентичность битовых представлений адресов,
если биты соответствующих позиций всех адресов совпадают, то срабатывает инкрементирование счетчика бит для маски,
при первом же несовпадение происходит выход из вспомогательной ф-ции с возвращаемым значением маски и списка адресов в 
бинарном представлении. Если весь набор адресов одинаков, то кол-во бит маски будет соответствовать 32б или 128б для  "Ipv4" и
"Ipv6" соответственно, с дальнейшим выходом из программы.
Особенность формирования маски для IPv6 учтена (маска подсети выравнивается по границе полубайта - 4 бита,
поэтому под хост будет выделено кол-во бит кратное 4, если изначально кратность не соблюдается, то на этом шаге происходит довеление до нее).

7. Определение IP-адреса сети - октет/хектет с стартовыми биты, отведенными под хост заполняется нулями, определяется значение
адреса сети в вспомогательной ф-ции get_net(bin_addr, count_net, ip), возвращающей строковое представление адреса.

8. Завершающий шаг алгоритма заключается в создании строкового представления минимальной подсети для заданного набора IP-адресов
при получении кол-во бит маски и адреса сети. Реализация представлена в ф-ции get_result(net, count_net).
