import tkinter as tk
from tkinter import filedialog, ttk
import tokenize
import io
import os
import re
import contextlib
import webbrowser

# Полный словарь чистого Python (все ключевые слова, функции, типы и ошибки)
ПОЛНЫЙ_СЛОВАРЬ_PYTHON = {
    # 1. Ключевые слова (35 + мягкие)
    "Ложь": "False",
    "Ничего": "None",
    "Истина": "True",
    "и": "and",
    "как": "as",
    "утверждать": "assert",
    "асинхронно": "async",
    "ждать": "await",
    "прервать": "break",
    "класс": "class",
    "продолжить": "continue",
    "функция": "def",
    "удалить": "del",
    "иначе_если": "elif",
    "иначе": "else",
    "исключение": "except",
    "наконец": "finally",
    "для": "for",
    "из": "from",
    "глобальная": "global",
    "если": "if",
    "импорт": "import",
    "в": "in",
    "является": "is",
    "лямбда": "lambda",
    "нелокальная": "nonlocal",
    "не": "not",
    "или": "or",
    "пропустить": "pass",
    "вызвать": "raise",
    "вернуть": "return",
    "попробовать": "try",
    "пока": "while",
    "с": "with",
    "отдать": "yield",
    "сопоставить": "match",
    "вариант": "case",

    # 2. Встроенные функции и типы данных
    "модуль_числа": "abs",
    "аситератор": "aiter",
    "все": "all",
    "аследующий": "anext",
    "любой": "any",
    "аски": "ascii",
    "двоичное": "bin",
    "логическое": "bool",
    "точка_останова": "breakpoint",
    "массив_байтов": "bytearray",
    "байты": "bytes",
    "вызываемый": "callable",
    "символ": "chr",
    "метод_класса": "classmethod",
    "компилировать": "compile",
    "комплексное": "complex",
    "удалить_атрибут": "delattr",
    "словарь": "dict",
    "список_атрибутов": "dir",
    "деление_с_остатком": "divmod",
    "перечислить": "enumerate",
    "вычислить": "eval",
    "выполнить": "exec",
    "выход": "exit",
    "фильтр": "filter",
    "дробное": "float",
    "формат": "format",
    "неизменяемое_множество": "frozenset",
    "получить_атрибут": "getattr",
    "глобальные": "globals",
    "есть_атрибут": "hasattr",
    "хэш": "hash",
    "справка": "help",
    "шестнадцатеричное": "hex",
    "идентификатор": "id",
    "ввод": "input",
    "целое": "int",
    "экземпляр": "isinstance",
    "подкласс": "issubclass",
    "итератор": "iter",
    "длина": "len",
    "список": "list",
    "локальные": "locals",
    "применить": "map",
    "максимум": "max",
    "область_памяти": "memoryview",
    "минимум": "min",
    "следующий": "next",
    "объект": "object",
    "восьмеричное": "oct",
    "открыть": "open",
    "код_символа": "ord",
    "степень": "pow",
    "печать": "print",
    "свойство": "property",
    "выйти": "quit",
    "диапазон": "range",
    "представление": "repr",
    "развернуть": "reversed",
    "округлить": "round",
    "множество": "set",
    "задать_атрибут": "setattr",
    "срез": "slice",
    "сортировать": "sorted",
    "статический_метод": "staticmethod",
    "строка": "str",
    "сумма": "sum",
    "родитель": "super",
    "кортеж": "tuple",
    "тип": "type",
    "переменные": "vars",
    "объединить": "zip",

    # 3. Встроенные исключения и ошибки
    "АрифметическаяОшибка": "ArithmeticError",
    "ОшибкаУтверждения": "AssertionError",
    "ОшибкаАтрибута": "AttributeError",
    "БазовоеИсключение": "BaseException",
    "ГруппаБазовыхИсключений": "BaseExceptionGroup",
    "ОшибкаБлокировкиВводаВывода": "BlockingIOError",
    "ОшибкаРазорванногоКанала": "BrokenPipeError",
    "ОшибкаБуфера": "BufferError",
    "ПредупреждениеБайтов": "BytesWarning",
    "ОшибкаДочернегоПроцесса": "ChildProcessError",
    "ОшибкаПрерыванияСоединения": "ConnectionAbortedError",
    "ОшибкаСоединения": "ConnectionError",
    "ОшибкаОтказаСоединения": "ConnectionRefusedError",
    "ОшибкаСбросаСоединения": "ConnectionResetError",
    "ПредупреждениеУстаревания": "DeprecationWarning",
    "ОшибкаКонцаФайла": "EOFError",
    "Многоточие": "Ellipsis",
    "ПредупреждениеКодировки": "EncodingWarning",
    "ОшибкаОкружения": "EnvironmentError",
    "Исключение": "Exception",
    "ГруппаИсключений": "ExceptionGroup",
    "ОшибкаСуществованияФайла": "FileExistsError",
    "ОшибкаФайлНеНайден": "FileNotFoundError",
    "ОшибкаПлавучейТочки": "FloatingPointError",
    "ПредупреждениеБудущего": "FutureWarning",
    "ВыходГенератора": "GeneratorExit",
    "ОшибкаВводаВывода": "IOError",
    "ОшибкаИмпорта": "ImportError",
    "ПредупреждениеИмпорта": "ImportWarning",
    "ОшибкаОтступа": "IndentationError",
    "ОшибкаИндекса": "IndexError",
    "ПрерваннаяОшибка": "InterruptedError",
    "ОшибкаЭтоПапка": "IsADirectoryError",
    "ОшибкаКлюча": "KeyError",
    "ПрерываниеСКлавиатуры": "KeyboardInterrupt",
    "ОшибкаПоиска": "LookupError",
    "ОшибкаПамяти": "MemoryError",
    "ОшибкаМодульНеНайден": "ModuleNotFoundError",
    "ОшибкаИмени": "NameError",
    "ОшибкаНеПапка": "NotADirectoryError",
    "НеРеализовано": "NotImplemented",
    "ОшибкаНеРеализовано": "NotImplementedError",
    "ОшибкаОС": "OSError",
    "ОшибкаПереполнения": "OverflowError",
    "ОжидаемоеПредупреждениеУстаревания": "PendingDeprecationWarning",
    "ОшибкаДоступа": "PermissionError",
    "ОшибкаПоискаПроцесса": "ProcessLookupError",
    "ОшибкаЗавершенияPython": "PythonFinalizationError",
    "ОшибкаРекурсии": "RecursionError",
    "ОшибкаСсылки": "ReferenceError",
    "ПредупреждениеРесурсов": "ResourceWarning",
    "ОшибкаВыполнения": "RuntimeError",
    "ПредупреждениеВыполнения": "RuntimeWarning",
    "ОстановкаАсинхроннойИтерации": "StopAsyncIteration",
    "ОстановкаИтерации": "StopIteration",
    "СинтаксическаяОшибка": "SyntaxError",
    "СинтаксическоеПредупреждение": "SyntaxWarning",
    "СистемнаяОшибка": "SystemError",
    "СистемныйВыход": "SystemExit",
    "ОшибкаТабуляции": "TabError",
    "ОшибкаВремениОжидания": "TimeoutError",
    "ОшибкаТипа": "TypeError",
    "ОшибкаНесвязаннойЛокальнойПеременной": "UnboundLocalError",
    "ОшибкаДекодированияЮникода": "UnicodeDecodeError",
    "ОшибкаКодированияЮникода": "UnicodeEncodeError",
    "ОшибкаЮникода": "UnicodeError",
    "ОшибкаПереводаЮникода": "UnicodeTranslateError",
    "ПредупреждениеЮникода": "UnicodeWarning",
    "ПользовательскоеПредупреждение": "UserWarning",
    "ОшибкаЗначения": "ValueError",
    "Предупреждение": "Warning",
    "ОшибкаWindows": "WindowsError",
    "ОшибкаДеленияНаНоль": "ZeroDivisionError",

    # 4. Системные имена
    "__построить_класс__": "__build_class__",
    "__отладка__": "__debug__",
    "__документация__": "__doc__",
    "__импорт__": "__import__",
    "__загрузчик__": "__loader__",
    "__имя__": "__name__",
    "__пакет__": "__package__",
    "__спецификация__": "__spec__",
    "авторские_права": "copyright",
    "благодарности": "credits",
    "лицензия": "license",
}

# Обратный словарь для перевода системных ошибок на русский
ПЕРЕВОД_ОШИБОК = {значение: ключ for ключ, значение in ПОЛНЫЙ_СЛОВАРЬ_PYTHON.items()}

ПОДСКАЗКИ_ПО_ОШИБКАМ = {
    "SyntaxError": "Проверь знаки препинания, кавычки и двоеточия после 'если', 'для', 'пока' или 'функция'.",
    "IndentationError": "Нарушены пробелы (отступы) в начале строки. После двоеточия нужен отступ в 4 пробела.",
    "NameError": "Используется неизвестная команда или переменная. Проверь, нет ли опечатки в названии.",
    "TypeError": "Несовместимые типы данных (например, попытка сложить текст и число без перевода в строку).",
    "ZeroDivisionError": "Делить на ноль нельзя!",
    "IndexError": "Попытка обратиться к элементу списка по номеру, которого не существует.",
    "KeyError": "В словаре нет такого ключа.",
    "ValueError": "Передано неподходящее значение (например, попытка превратить буквы в целое число).",
    "FileNotFoundError": "Указанный файл не найден. Проверь имя файла и путь к нему.",
    "ModuleNotFoundError": "Библиотека не найдена или не установлена на компьютере.",
}

СЛОВАРИ = {
    "Python (.rupy -> .py)": {
        "in_ext": ".rupy",
        "out_ext": ".py",
        "words": ПОЛНЫЙ_СЛОВАРЬ_PYTHON
    },
    "Lua (.rulua -> .lua)": {
        "in_ext": ".rulua",
        "out_ext": ".lua",
        "words": {
            "локальная": "local",
            "функция": "function",
            "вернуть": "return",
            "конец": "end",
            "печать": "print",
            "истина": "true",
            "ложь": "false",
            "ничего": "nil",
            "если": "if",
            "тогда": "then",
            "иначе_если": "elseif",
            "иначе": "else",
            "и": "and",
            "или": "or",
            "не": "not",
            "пока": "while",
            "делать": "do",
            "для": "for",
            "в": "in",
            "повторять": "repeat",
            "до_тех_пор": "until",
            "прервать": "break",
            "ждать": "wait",
            "игра": "game",
            "рабочее_пространство": "workspace",
            "игроки": "Players",
            "родитель": "Parent",
            "имя": "Name",
            "уничтожить": "Destroy",
            "клонировать": "Clone",
        }
    },
    "JavaScript (.rujs -> .js)": {
        "in_ext": ".rujs",
        "out_ext": ".js",
        "words": {
            "переменная": "let",
            "константа": "const",
            "функция": "function",
            "вернуть": "return",
            "если": "if",
            "иначе": "else",
            "пока": "while",
            "для": "for",
            "консоль": "console",
            "печать": "log",
            "предупреждение": "alert",
            "документ": "document",
            "найтиПоId": "getElementById",
            "истина": "true",
            "ложь": "false",
        }
    },
    "HTML (.ruhtml -> .html)": {
        "in_ext": ".ruhtml",
        "out_ext": ".html",
        "words": {
            "страница": "html",
            "голова": "head",
            "заголовок_страницы": "title",
            "тело": "body",
            "заголовок1": "h1",
            "заголовок2": "h2",
            "абзац": "p",
            "блок": "div",
            "кнопка": "button",
            "ссылка": "a",
            "адрес": "href",
            "картинка": "img",
            "источник": "src",
            "список": "ul",
            "пункт": "li",
        }
    },
    "CSS (.rucss -> .css)": {
        "in_ext": ".rucss",
        "out_ext": ".css",
        "words": {
            "тело": "body",
            "кнопка": "button",
            "блок": "div",
            "цвет": "color",
            "фон": "background",
            "цвет_фона": "background-color",
            "ширина": "width",
            "высота": "height",
            "размер_шрифта": "font-size",
            "отступ_внутри": "padding",
            "отступ_снаружи": "margin",
            "рамка": "border",
            "скругление": "border-radius",
            "центр": "center",
            "красный": "red",
            "синий": "blue",
            "зеленый": "green",
            "белый": "white",
            "черный": "black",
        }
    }
}


class RoundedButton(tk.Canvas):
    """Скругленная кнопка с плавной подсветкой при наведении курсора"""
    def __init__(self, parent, text, command, width=130, height=34, radius=14,
                 bg_color="#3c3f41", hover_color="#4e5254", text_color="white", parent_bg="#2b2b2b"):
        super().__init__(parent, width=width, height=height, bg=parent_bg, highlightthickness=0, cursor="hand2")
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color

        self.rect = self._draw_rounded_rect(2, 2, width - 2, height - 2, radius, fill=bg_color, outline="")
        self.label = self.create_text(width // 2, height // 2, text=text, fill=text_color, font=("Segoe UI", 10, "bold"))

        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
            x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
            x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2,
            x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_hover(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)

    def _on_click(self, event):
        if self.command:
            self.command()


class LangCodeIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("LangCode IDE v0.2.0 — Full Core Edition (by EXLACO)")
        self.root.geometry("980x670")
        self.текущий_путь = None

        панель_цвет = "#2b2b2b"
        панель = tk.Frame(root, bg=панель_цвет, pady=8)
        панель.pack(fill=tk.X)

        self.иконка_ру = None
        if os.path.exists("ru_btn.png"):
            self.иконка_ру = tk.PhotoImage(file="ru_btn.png")
            tk.Label(панель, image=self.иконка_ру, bg=панель_цвет).pack(side=tk.LEFT, padx=10)
        else:
            RoundedButton(
                панель, text="🇷🇺 РУССКИЙ", command=None,
                width=125, height=34, radius=14,
                bg_color="#383c4a", hover_color="#383c4a", parent_bg=панель_цвет
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(панель, text="Язык:", bg=панель_цвет, fg="#cccccc", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(6, 4))
        self.выбор_режима = ttk.Combobox(панель, values=list(СЛОВАРИ.keys()), state="readonly", width=23, font=("Segoe UI", 10))
        self.выбор_режима.pack(side=tk.LEFT, padx=4)
        self.выбор_режима.current(0)

        RoundedButton(
            панель, text="📄 Новый", command=self.новый_файл,
            width=100, height=34, radius=14,
            bg_color="#3c3f41", hover_color="#505355", parent_bg=панель_цвет
        ).pack(side=tk.LEFT, padx=5)

        RoundedButton(
            панель, text="📂 Открыть", command=self.открыть_файл,
            width=110, height=34, radius=14,
            bg_color="#3c3f41", hover_color="#505355", parent_bg=панель_цвет
        ).pack(side=tk.LEFT, padx=5)

        RoundedButton(
            панель, text="💾 Сохранить (Ctrl+S)", command=self.сохранить_и_перевести,
            width=165, height=34, radius=14,
            bg_color="#2e7d32", hover_color="#388e3c", parent_bg=панель_цвет
        ).pack(side=tk.LEFT, padx=5)

        RoundedButton(
            панель, text="▶ Запустить (F5)", command=self.запустить_код,
            width=145, height=34, radius=14,
            bg_color="#1565c0", hover_color="#1976d2", parent_bg=панель_цвет
        ).pack(side=tk.LEFT, padx=5)

        self.редактор = tk.Text(
            root, font=("Consolas", 13), bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white", undo=True, padx=12, pady=12
        )
        self.редактор.pack(expand=True, fill=tk.BOTH)

        tk.Label(
            root, text="Готовый английский код (автосохранение рядом) и результат запуска:",
            bg=панель_цвет, fg="#aaaaaa", anchor="w", padx=10, pady=4, font=("Segoe UI", 9)
        ).pack(fill=tk.X)

        self.предпросмотр = tk.Text(
            root, height=11, font=("Consolas", 11), bg="#121212", fg="#9cdcfe",
            state=tk.DISABLED, padx=12, pady=8
        )
        self.предпросмотр.pack(fill=tk.X)

        self.root.bind("<Control-s>", lambda e: self.сохранить_и_перевести())
        self.root.bind("<F5>", lambda e: self.запустить_код())

    def перевести_код(self, код, режим):
        словарь = СЛОВАРИ[режим]["words"]

        if режим.startswith("Python"):
            токены = tokenize.generate_tokens(io.StringIO(код).readline)
            результат = []
            for тип_токена, значение, _, _, _ in токены:
                if тип_токена == tokenize.NAME and значение in словарь:
                    значение = словарь[значение]
                результат.append((тип_токена, значение))
            return tokenize.untokenize(результат)

        шаблон = r'("[^"]*"|\'[^\']*\')|\b([а-яА-ЯёЁ_][а-яА-ЯёЁ0-9_]*)\b'

        def замена(совпадение):
            if совпадение.group(1):
                return совпадение.group(1)
            слово = совпадение.group(2)
            return словарь.get(слово, слово)

        return re.sub(шаблон, замена, код)

    def объяснить_ошибку(self, ошибка):
        тип_англ = type(ошибка).__name__
        тип_рус = ПЕРЕВОД_ОШИБОК.get(тип_англ, тип_англ)
        совет = ПОДСКАЗКИ_ПО_ОШИБКАМ.get(тип_англ, "Проверь синтаксис и логику в указанной строке.")
        строка = getattr(ошибка, "lineno", None)
        где = f" (строка {строка})" if строка else ""
        return f"[{тип_рус} / {тип_англ}]{где}: {ошибка}\n💡 Подсказка: {совет}"

    def новый_файл(self):
        self.текущий_путь = None
        self.редактор.delete("1.0", tk.END)
        self.показать_предпросмотр("")
        self.root.title("LangCode IDE v0.2.0 — Новый файл")

    def открыть_файл(self):
        путь = filedialog.askopenfilename(
            filetypes=[("LangCode файлы", "*.rupy *.rulua *.rujs *.ruhtml *.rucss"), ("Все файлы", "*.*")]
        )
        if путь:
            self.текущий_путь = путь
            with open(путь, "r", encoding="utf-8") as f:
                self.редактор.delete("1.0", tk.END)
                self.редактор.insert("1.0", f.read())
            self.root.title(f"LangCode IDE v0.2.0 — {os.path.basename(путь)}")

    def сохранить_и_перевести(self):
        режим = self.выбор_режима.get()
        вход_расш = СЛОВАРИ[режим]["in_ext"]
        выход_расш = СЛОВАРИ[режим]["out_ext"]

        if not self.текущий_путь:
            путь = filedialog.asksaveasfilename(
                defaultextension=вход_расш,
                filetypes=[(режим, f"*{вход_расш}")]
            )
            if not путь:
                return None, None
            self.текущий_путь = путь

        русский_код = self.редактор.get("1.0", tk.END).strip()

        with open(self.текущий_путь, "w", encoding="utf-8") as f:
            f.write(русский_код)

        try:
            готовый_код = self.перевести_код(русский_код, режим)
            путь_выхода = os.path.splitext(self.текущий_путь) + выход_расш
            with open(путь_выхода, "w", encoding="utf-8") as f:
                f.write(готовый_код)

            self.показать_предпросмотр(готовый_код)
            self.root.title(f"LangCode IDE v0.2.0 — {os.path.basename(self.текущий_путь)} -> {os.path.basename(путь_выхода)}")
            return готовый_код, путь_выхода
        except Exception as ошибка:
            self.показать_предпросмотр(f"--- ОШИБКА ПЕРЕВОДА ---\n{self.объяснить_ошибку(ошибка)}")
            return None, None

    def запустить_код(self):
        готовый_код, путь_выхода = self.сохранить_и_перевести()
        if not готовый_код:
            return

        режим = self.выбор_режима.get()
        if режим.startswith("Python"):
            буфер = io.StringIO()
            try:
                with contextlib.redirect_stdout(буфер):
                    exec(готовый_код, {})
                вывод = буфер.getvalue()
                self.показать_предпросмотр(f"--- ПЕРЕВОД (.py) ---\n{готовый_код}\n\n--- РЕЗУЛЬТАТ ЗАПУСКА ---\n{вывод or 'Программа выполнена успешно.'}")
            except Exception as ошибка:
                self.показать_предпросмотр(f"--- ПЕРЕВОД (.py) ---\n{готовый_код}\n\n--- ОШИБКА ВЫПОЛНЕНИЯ ---\n{self.объяснить_ошибку(ошибка)}")
        elif режим.startswith("HTML"):
            webbrowser.open(f"file:///{os.path.abspath(путь_выхода)}")
            self.показать_предпросмотр(f"--- ПЕРЕВОД (.html) ---\n{готовый_код}\n\n[Страница открыта в браузере]")
        else:
            self.показать_предпросмотр(f"--- ГОТОВЫЙ КОД ({os.path.basename(путь_выхода)}) ---\n{готовый_код}\n\n[Файл переведен и сохранен на диск]")

    def показать_предпросмотр(self, текст):
        self.предпросмотр.config(state=tk.NORMAL)
        self.предпросмотр.delete("1.0", tk.END)
        self.предпросмотр.insert("1.0", текст)
        self.предпросмотр.config(state=tk.DISABLED)


if __name__ == "__main__":
    окно = tk.Tk()
    приложение = LangCodeIDE(окно)
    окно.mainloop()
