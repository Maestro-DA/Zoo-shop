from app import db, Product  # Замените 'your_flask_app' на название вашего модуля приложения

# Данные для примерных товаров
sample_products = [
    {
        "title": "Корм",
        "description": "VITAPOL Economic корм для морской свинки 1200гр",
        "price": 10.99,
        "category": "Грызуны",
        "image_url": "/static/img/products/m2.jpg"
    },
    {
        "title": "Vitapol Economic Корм для хомяков",
        "description": "Vitapol Economic Корм для хомяков",
        "price": 15.99,
        "category": "Грызуны",
        "image_url": "/static/img/products/m3.jpg"
    },
    {
        "title": "Домик",
        "description": "Домик Mr.Kranch для грызунов Лимончик 13х8х9 см",
        "price": 20.99,
        "category": "Грызуны",
        "image_url": "/static/img/products/m4.jpg"
    },

{
        "title": "Корм",
        "description": "Versele Laga Корм для карликовых",
        "price": 20.99,
        "category": "Грызуны",
        "image_url": "/static/img/products/m6.png"
    },
{
        "title": "Корм для морских свинок",
        "description": "Triol Original Корм для морских свинок, 450г",
        "price": 20.99,
        "category": "Грызуны",
        "image_url": "/static/img/products/m7.jpg"
    }


]

# Добавление товаров в базу данных
for product_data in sample_products:
    product = Product(
        title=product_data["title"],
        description=product_data["description"],
        price=product_data["price"],
        category=product_data["category"],
        image_url=product_data["image_url"]
    )
    db.session.add(product)

# Сохранение изменений в базе данных
db.session.commit()

print("Примерные товары успешно добавлены!")


# For Adding in console
# flask shell
# exec(open('sample.py', encoding='utf-8').read())