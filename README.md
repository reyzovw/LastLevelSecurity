# LLS

[Latest release here -> click](https://github.com/reyzovw/LastLevelSecurity/releases/tag/release135)


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

## Стек

#### Ядро
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![colorama](https://img.shields.io/badge/colorama-3ECF8E?style=for-the-badge&logoColor=white)
![pycryptodome](https://img.shields.io/badge/pycryptodome-8E75B2?style=for-the-badge&logoColor=white)
#### Методы шифрования
![AES-256](https://img.shields.io/badge/AES_256-%23FF0000.svg?style=for-the-badge&logoColor=white)
![CBC](https://img.shields.io/badge/CBC-%23FF0000.svg?style=for-the-badge&logoColor=white)
![IV](https://img.shields.io/badge/IV-%23FF0000.svg?style=for-the-badge&logoColor=white)
![HMAC](https://img.shields.io/badge/HMAC-%23FF0000.svg?style=for-the-badge&logoColor=white)
![ENTROPY](https://img.shields.io/badge/ENTROPY-%23FF0000.svg?style=for-the-badge&logoColor=white)

## Преимущества

1. Блочное шифрование

2. Инициализационный вектор _(IV)_ 

3. Сложение блоков: первый блок данных перед шифрованием объединяется с инициализационным вектором, а каждый последующий блок данных объединяется с предыдущим зашифрованным блоком, это значит, что изменение любого блока данных повлияет на все последующие зашифрованные блоки

4. Использование энтропии для генерации ключа делает его менее предсказуемым

5. Каждый раз, когда вы шифруете данные, создание нового инициализационного вектора с помощью рандомных данных помогает избежать брутфорса

6. Режим CBC обеспечивает дополнительный уровень безопасности, добавляя случайность к процессу шифрования

7. Hash-based Message Authentication Code - позволяет проверить, были ли данные изменены или повреждены в процессе передачи. только обладатель этого ключа может создать верное значение HMAC. Это гарантирует, что данные действительно исходят от ожидаемого источника. Если он не совпадет при проверке это означает, что данные были скомпрометированы.  Если взломщик не знает секретный ключ, он не может сгенерировать корректный HMAC для измененного сообщения (допустим как в атаках "man-in-the-middle attacks" и "replay attacks"). Использования устойчивой хэш функции обеспечивает доп. уровень безопасности

