![статус работы](https://github.com/exp-ext/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

# Проект YaMDb

<p  align="right">
<a href="#res">Ресурсы API YaMDb</a>
</p>

<p  align="right">
<a href="#rol">Пользовательские роли и права доступа</a>
</p>

<p  align="right">
<a href="#reg">Регистрация новых пользователей</a>
</p>

<p  align="right">
<a href="#data">Связанные данные и каскадное удаление</a>
</p>

<p align="center">
<img src="https://vogazeta.ru/uploads/full_size_1559805406-cd6a299889def10b711bbe19d218836b.jpg" width="700">
</p>

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

<section id="res">
    <h2> Ресурсы API YaMDb </h2>
</section>
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

<section id="rol">
    <h2> Пользовательские роли и права доступа </h2>
</section>

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.


<section id="reg">
    <h2> Самостоятельная регистрация новых пользователей </h2>
</section>

1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
2. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
3. В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

## Создание пользователя администратором
Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения.

После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.

Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

<section id="data">
    <h2> Связанные данные и каскадное удаление </h2>
</section>

При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).

При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.

При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.

При удалении объекта категории Category не нужно **удалять связанные с этой категорией произведения.

При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.
___

## Технологие задействованные в проекте:

<ul>
  <li> Django  <img src="https://cdn.icon-icons.com/icons2/2415/PNG/512/django_plain_logo_icon_146558.png" alt="Django" style="width:35px;"/></li>
  <li> Django-rest-framework  <img src="https://www.django-rest-framework.org/img/logo.png" alt="SQLite" style="width:70px;"/></li>
</ul>

___

## Авторы проекта:

**Андрей Борокин** - Technical Lead
- git: [exp-ext](https://github.com/exp-ext)
- [![Join Telegram](https://img.shields.io/badge/My%20Telegram-Join-blue)](https://t.me/Borokin)
___
**Евгений Волков** - Team Lead
- git: [IncubTLT](https://github.com/IncubTLT)
___
