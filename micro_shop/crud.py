import asyncio
from itertools import product, count

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.testing.suite.test_reflection import users

from core.models import db_helper, User, Profile, Post
from micro_shop.core.models import Order, Product, OrderProductAssociation


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"user: {user}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none() # scalar_one_or_none - ожидаем получить один элемент или None
    user = await session.scalar(stmt)
    print("Fount user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id) # для получения связанных моделей, где тип связи - один-к-одному: используем selectinload
    users = await session.scalars(stmt) # scalars - ожидаем получить коллекцию элементов
    for user in users:
        print(user)
        print(user.profile)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    posts_titles: list[str],
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts) # add_all - если нужно добавить несколько записей в бд в виде list
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id) # для получения связанных моделей, где тип связи - один-ко-многим: используем selectinload
    users = await session.scalars(stmt)
    for user in users:
        print(f"User: {user}, posts: {[post for post in user.posts]}")


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(f"post: {post}")
        print(f"author: {post.user}")


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile), selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print("*" * 10)
        print(f"user: {user}, user_profile: {user.profile}")
        for post in user.posts:
            print(f"post: {post}")


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    # join нужен для работы where, т.к. запрос сложный
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == "john")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="alice")
    await create_user(session=session, username="sam")
    user_sam = await get_user_by_username(session=session, username="sam")
    user_john = await get_user_by_username(session=session, username="john")
    user_alice = await get_user_by_username(session=session, username="alice")
    await get_user_by_username(session=session, username="bob")
    await create_user_profile(
        session=session,
        user_id=user_sam.id,
        first_name="Sam",
    )
    await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name="John",
    )
    await show_users_with_profiles(session)
    await create_posts(
        session=session,
        user_id=user_sam.id,
        posts_titles=["SQLA 2.0", "SQLA Joins"],
    )
    await create_posts(
        session=session,
        user_id=user_john.id,
        posts_titles=["SQLA intro", "SQLA Advanced", "SQLA More"],
    )
    await create_posts(user_id=user_alice.id, posts_titles=[])
    await get_users_with_posts(session=session)
    await get_posts_with_authors(session=session)
    await get_users_with_posts_and_profiles(session=session)
    await get_profiles_with_users_and_users_with_posts(session=session)
    await get_user_by_username(session=session, username="john")


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


"___________________________________"


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
):
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_1 = await create_order(session)
    order_promo = await create_order(session=session, promocode="promo")

    mouse = await create_product(
        session=session,
        name="Mouse",
        description="Greate gaming mouse",
        price=123,
    )
    keyboard = await create_product(
        session=session,
        name="Keyboard",
        description="Greate gaming keyboard",
        price=149,
    )
    display = await create_product(
        session=session,
        name="Display",
        description="Office display",
        price=299,
    )

    order_1 = await session.scalar(
        select(Order)
        .where(Order.id == order_1.id)
        .options(selectinload(Order.products)),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products)),
    )
    order_1.products.append(mouse)
    order_1.products.append(keyboard)
    # order_promo.products.append(keyboard)
    # order_promo.products.append(display)
    order_promo.products.extend([keyboard, display])
    await session.commit()

async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.product))
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(f"id {order.id}, promocode {order.promocode}, promocode {order.created_ad}, products:")
        for product in order.products:
            print(f"-- id {product.id}, name {product.name}, price {product.price}")


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(OrderProductAssociation.product)
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    for order in orders:
        print(f"id {order.id}, promocode {order.promocode}, promocode {order.created_ad}, products:")
        for order_product_details in order.products_details:
            print(
                f"- id {order_product_details.product.id}, "
                f"price {order_product_details.product.price}, "
                f"qty {order_product_details.count}"
            )


async def create_gift_product_for_existing_orders(session: AsyncSession):
    await demo_get_orders_with_products_with_assoc(session)
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session=session,
        name="Gift",
        description="Gift for you",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )
    await session.commit()


async def demo_m2m(session: AsyncSession):
    await create_gift_product_for_existing_orders(session)



if __name__ == "__main__":
    asyncio.run(main())
