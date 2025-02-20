# Управление спортивным инвентарем

Эффективный учет и контроль спортивного инвентаря в школе играет важную роль в обеспечении высокого уровня проведения
спортивных мероприятий и занятий физической культурой. Необходимо разработать приложение, которое позволит отслеживать
наличие, состояние и распределение спортивного инвентаря, а также планировать его закупку.

## [Видеодемонстрация](https://rutube.ru/video/54afd8fe5d7418659a993c00a05dba4d/)
Видео опубликовано на [RUTUBE.RU](https://rutube.ru/video/54afd8fe5d7418659a993c00a05dba4d/)

## Техническое задание

**Необходимо предусмотреть роли с уровнями доступа:**

- администратор;
- пользователь.

**Функциональность приложения для администратора:**

- авторизация администратора в приложении;
- добавление позиций инвентаря с указанием названия, количества;
- редактирование позиций инвентаря в части состояния (новый, используемый, сломанный), количества, названия;
- закрепление за пользователями инвентаря;
- планирование и управление закупками инвентаря: добавление в план закупок с указанием цены и планируемого поставщика
  (учитывается только название поставщика);
- создание отчётов по использованию и состоянию инвентаря.

**Функциональность приложения для пользователя:**
- регистрация и авторизация пользователя;
- просмотр доступного инвентаря и его состояния;
- создание заявок на получение инвентаря;
- отслеживание статуса заявок на получение инвентаря.

**Дополнительная функциональность приложения со стороны пользователя:**
- создание заявки о необходимости ремонта или замены инвентаря.

## Регламент испытаний

Испытания должны включать проверку всех функциональных требований, указанных в техническом задании, в том числе:
- регистрация и авторизация пользователей;
- добавление не менее четырех позиций инвентаря, редактирование не менее двух позиций,
  удаление одной позиции администратором;
- назначение не менее двух позиций инвентаря двум разным пользователям;
- добавление не менее двух позиций в план закупок администратором;
- оформление двух заявок на новый инвентарь пользователями, одобрение одной заявки
  и отклонение одной заявки администратором;
- формирование отчета администратором об использовании инвентаря с указанием статуса и пользователя;
- тестирование обработки исключительных ситуаций
  (например, недостаток инвентаря для выполнения заявки).

## Инструкция для запуска

1. Установить зависимости
```bash
pip install -r requirements.txt
```
2. Выполнить миграции и создать администратора
```bash
python backend/manage.py migrate
python backend/manage.py createsuperuser
```
3. Запустить сервер
```bash
python backend/manage.py runserver
```
