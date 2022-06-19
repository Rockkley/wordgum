def return_dict(dict_data):
    if dict_data == 'animals_eng':
        return {'Dog': 'Собака', 'Cat': 'Кошка', 'Parrot': 'Попугай', 'Elephant': 'Слон', 'Bird': 'Птица',
                'Eagle': 'Орёл', 'Bug': 'Жук', 'Mouse': 'Мышь', 'Horse': 'Лошадь', 'Armadillo': 'Броненосец',
                'Snake': 'Змея', 'Wolf': 'Волк', 'Cow': 'Корова', 'Lion': 'Лев', 'Fly': 'Муха', 'Sheep': 'Овца',
                'Bull': 'Бык', 'Bear': 'Медведь', 'Fish': 'Рыба', 'Worm': 'Червь', 'Сhicken': 'Курица',
                'Rooster': 'Петух', 'Rabbit': 'Кролик'}

    elif dict_data == 'food_eng':
        return {'Carrot': 'Морковь', 'Bread': 'Хлеб', 'Apple': 'Яблоко', 'Orange': 'Апельсин', 'Cheese': 'Сыр',
                'Cookie': 'Печенька', 'Salad': 'Салат', 'Sandwich': 'Сэндвич', 'Soup': 'Суп', 'Pizza': 'Пицца',
                'Starter': 'Первое блюдо', 'Seafoods': 'Морепродукты', 'Side dish': 'Гарнир', 'Lasagna': 'Лазанья',
                'Stew': 'Рагу', 'Meatballs': 'Фрикадельки', 'Flapjack': 'Блин', 'Cutlet': 'Отбивная'
                }

    elif dict_data == 'animals_fin':
        return {'Ankka': 'Утка', 'Heinäsirkka': 'Кузнечик', 'Koira': 'Собака', 'Kissa': 'Кошка', 'Lintu': 'Птица',
                'Varis': 'Ворона', 'Sammakko': 'Лягушка', 'Hiiri': 'Мышь', 'Hevonen': 'Лошадь', 'Pöllö': 'Сова',
                'Vuohi': 'Коза', 'Leijona': 'Лев', 'Vasikka': 'Телёнок', 'Papukaija': 'Попугай',
                'Riikinkukko': 'Павлин', 'Lokki': 'Чайка', 'Majava': 'Бобр', 'Peura': 'Олень', 'Kotka': 'Орёл'}

    elif dict_data == 'food_fin':
        return {'Porkkana': 'Морковь', 'Leipä': 'Хлеб', 'Omena': 'Яблоко', 'Appelsiini': 'Апельсин', 'Juusto': 'Сыр',
                'Keksit': 'Печенька', 'Salaatti': 'Салат', 'Voileipä': 'Сэндвич', 'Keitto': 'Суп',
                'Öljy': 'Растительное масло', 'Sipuli': 'Лук', 'Valkosipuli': 'Чеснок', 'Paahtoleipä': 'Гренки',
                'Kurpitsa': 'Тыква', 'Maissi': 'Кукуруза', 'Piirakka': 'Пирог', 'Kakku': 'Торт', 'Raejuusto': 'Творог',
                'Kerma': 'Сливки'}

    elif dict_data == 'city_fin':
        return {'Kaupunki': 'Город', 'Katu': 'Улица', 'Myymälä': 'Магазин', 'Liikennevalot': 'Светофор',
                'Maanalainen': 'Метро', 'Puisto': 'Парк', 'Pilvenpiirtäjä': 'Небоскрёб', 'Ravintola': 'Ресторан'}

    elif dict_data == 'city_eng':
        return {'City': 'Город', 'Street': 'Улица', 'Shop': 'Магазин', 'Traffic lights': 'Светофор',
                'Subway': 'Метро', 'Park': 'Парк', 'Skyscraper': 'Небоскрёб', 'Restaurant': 'Ресторан'}

