# PROJECT2_TG_BOT

# Habits Tracker

## Описание

Telegram-бот для отслеживания привычек. Позволяет добавлять привычки, отмечать выполнение, смотреть статистику и получать мотивационные цитаты.

## Участники

- Харазов Роберт 467912
- Полымов Михаил 467140

## Cтруктура

<ul>
    <li>README.md</li>
    <li>requirements.txt</li>
    <li>bot.py <span class="comment"># Главный файл запуска бота</span></li>
    <li>.env</li>
    <li>config/
        <ul class="nested">
            <li>__init__.py</li>
            <li>settings.py <span class="comment"># Файл для хранения конфигурации и загрузки переменных окружения</span></li>
        </ul>
    </li>
    <li>routers/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Пустой файл для корректной работы импорта роутеров</span></li>
            <li>commands.py <span class="comment"># Файл с командами бота</span></li>
            <li>handlers/
                <ul class="nested">
                    <li>specific_handlers.py <span class="comment"># Хэндлеры для кастомных команд и логики FSM</span></li>
                </ul>
            </li>
        </ul>
    </li>
    <li>keyboards/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Пустой файл для корректной работы импорта клавиатур</span></li>
            <li>builders.py <span class="comment"># Здесь можно реализовать динамические клавиатуры, если потребуется</span></li>
            <li>inline.py <span class="comment"># Inline-клавиатура для главного меню</span></li>
        </ul>
    </li>
    <li>services/
        <ul class="nested">
            <li>api_client.py <span class="comment"># Взаимодействие с внешним API (мотивационные цитаты) + кэширование</span></li>
            <li>storage_service.py <span class="comment"># Работа с локальным хранилищем привычек (JSON-файл)</span></li>
        </ul>
    </li>
    <li>filters/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Пустой файл для корректной работы импорта фильтров</span></li>
            <li>admin_filter.py <span class="comment"># Кастомный фильтр для проверки, является ли пользователь админом</span></li>
        </ul>
    </li>
    <li>middlewares/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Пустой файл для корректной работы импорта мидлварей</span></li>
            <li>throttling.py <span class="comment"># Мидлварь для антиспама (ограничение частоты сообщений)</span></li>
        </ul>
    </li>
    <li>utils/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Пустой файл для корректной работы импорта утилит</span></li>
            <li>formatters.py <span class="comment"># Здесь можно реализовать функции для форматирования текста, если потребуется</span></li>
            <li>logger.py <span class="comment"># Настройка логгера для записи действий бота</span></li>
        </ul>
    </li>
    <li>states/
        <ul class="nested">
            <li>__init__.py <span class="comment"># Состояния FSM для добавления привычки</span></li>
        </ul>
    </li>
    <li>storage/
        <ul class="nested">
            <li>habits.json</li>
        </ul>
    </li>
</ul>

## Как запустить

1. Клонируйте репозиторий
2. Установите зависимости: pip install -r requirements.txt
3. Получите токен у BotFather и добавьте его в .env
4. Запустите бота: python bot.py
