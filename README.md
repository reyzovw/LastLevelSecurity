# LLS

Latest release: https://github.com/reyzovw/LastLevelSecurity/releases/tag/alpha130


## Установка
Для работы вы должны установить **[Python версии 3.12 или версией больше](https://www.python.org/downloads/)**

1. Создайте каталог и перейдите в него:
    ```shell
    mkdir "название папки"
   
    cd "название папки"
    ```
2. Скопируйте репозиторий:
    ```shell
    git clone https://github.com/reyzovw/LastLevelSecurity
    ```
3. Установите библиотеки:
    ```shell
    pip install -r requirements.txt
    ```
4. Запуск:
    ```shell
    python main.py
    ```

## Алгоритмы шифрования

1. Блочное шифрование

2. Инициализационный вектор _(IV)_ 

3. Сложение блоков: первый блок данных перед шифрованием объединяется с инициализационным вектором, а каждый последующий блок данных объединяется с предыдущим зашифрованным блоком, это значит, что изменение любого блока данных повлияет на все последующие зашифрованные блоки

4. Использование энтропии для генерации ключа делает его менее предсказуемым

5.  Каждый раз, когда вы шифруете данные, создание нового инициализационного вектора с помощью рандомных данных помогает избежать брутфорса

6. Режим CBC обеспечивает дополнительный уровень безопасности, добавляя случайность к процессу шифрования

7. Hash-based Message Authentication Code - позволяет проверить, были ли данные изменены или повреждены в процессе передачи. только обладатель этого ключа может создать верное значение HMAC. Это гарантирует, что данные действительно исходят от ожидаемого источника. Если он не совпадет при проверке это означает, что данные были скомпрометированы.  Если взломщик не знает секретный ключ, он не может сгенерировать корректный HMAC для измененного сообщения (допустим как в атаках "man-in-the-middle attacks" и "replay attacks"). Использования устойчивой хэш функции обеспечивает доп. уровень безопасности.
