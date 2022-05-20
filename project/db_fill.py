import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','ecommerce.settings')

import django
django.setup()

import random
from datetime import date, timedelta
import string

from webshop.core.models import FAQ, CustomUser, FAQTopic
from webshop.product.models import Product, Category, PackageType, Action

# Packages

package_types = []

package_types.append(
    PackageType.objects.create(
        summary_name='darab',
        display_name='db',
        quantity=1
    )
)
package_types.append(
    PackageType.objects.create(
        summary_name='póló karton',
        display_name='karton',
        quantity=6
    )
)
package_types.append(
    PackageType.objects.create(
        summary_name='cipő karton',
        display_name='karton',
        quantity=4
    )
)
package_types.append(
    PackageType.objects.create(
        summary_name='pár',
        display_name='pár',
        quantity=1
    )
)
package_types.append(
    PackageType.objects.create(
        summary_name='raklap',
        display_name='raklap',
        quantity=12
    )
)

# Categories

categories = []

categories.append(
    Category.objects.create(
        name='Szülő kategória1'
    )
)
categories.append(
    Category.objects.create(
        name='Szülő kategória2'
    )
)
categories.append(
    Category.objects.create(
        name='Szülő kategória3'
    )
)
categories.append(
    Category.objects.create(
        name='Gyerek kategória1-1',
        parent_id=categories[0]
    )
)
categories.append(
    Category.objects.create(
        name='Gyerek kategória1-2',
        parent_id=categories[0]
    )
)
categories.append(
    Category.objects.create(
        name='Gyerek kategória2-1',
        parent_id=categories[1]
    )
)
categories.append(
    Category.objects.create(
        name='Gyerek kategória2-2',
        parent_id=categories[1]
    )
)
categories.append(
    Category.objects.create(
        name='Gyerek kategória3-1',
        parent_id=categories[2]
    )
)
categories.append(
    Category.objects.create(
        name='Unoka kategória1-1-1',
        parent_id=categories[3]
    )
)
categories.append(
    Category.objects.create(
        name='Unoka kategória1-1-2',
        parent_id=categories[3]
    )
)
categories.append(
    Category.objects.create(
        name='Unoka kategória2-2-1',
        parent_id=categories[6]
    )
)
categories.append(
    Category.objects.create(
        name='Unoka kategória3-1-1',
        parent_id=categories[7]
    )
)

# Actions

actions = []

actions.append(
    Action.objects.create(
        name="Teszt akció1",
        percent=30,
        from_date=date.today(),
        to_date=date.today() + timedelta(days=7)
    )
)
actions.append(
    Action.objects.create(
        name="Teszt akció2",
        percent=50,
        from_date=date.today(),
        to_date=date.today() + timedelta(days=7)
    )
)
actions.append(
    Action.objects.create(
        name="Teszt akció3",
        percent=90,
        from_date=date.today() - timedelta(days=5),
        to_date=date.today() - timedelta(days=1)
    )
)
actions.append(
    Action.objects.create(
        name="Teszt akció2",
        percent=85,
        from_date=date.today() + timedelta(days=2),
        to_date=date.today() + timedelta(days=7)
    )
)

# Products

products = []

for i in range(500):
    product =Product.objects.create(
        name=f"Teszt termék-{i}",
        producer=f"Teszt gyártó-{i%10}",
        net_price=random.randint(500, 20000)*100,
        vat=27,
        description=''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(20, 100))),
        free_stock=random.randint(10, 200),
        reserved_stock=0,
        category_id=categories[random.randint(0, len(categories)-1)],
    )

    if i % 5 == 0:
        type_num = random.randint(1, 3)

        for j in range(type_num):
            product.package_type_id.add(package_types[random.randint(0, len(package_types)-1)])

    if random.randint(1, 4) == 4:
        action_num = random.randint(1, 2)

        for j in range(action_num):
            product.action_id.add(actions[random.randint(0, len(actions)-1)])
    product.save()

# FAQ topics

faq_topics = []

for i in range(6):
    faq_topics.append(
        FAQTopic.objects.create(
            name=f"Teszt téma{i+1}"
        )
    )

# FAQ's

for i in range(60):
    FAQ.objects.create(
        question=''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(20, 50))),
        answer=''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(70, 200))),
        topic_id=faq_topics[random.randint(0, len(faq_topics)-1)]
    )

# Users

for i in range(100):
    CustomUser.objects.create(
        is_staff=False,
        email=f"test{i+1}@test.com",
        first_name=f"Test{i+1}",
        last_name=f"Name",
        username=f"test{i+1}",
        password='test'
    )