from faker import Faker
import asyncio

from src.database.db import sessionmanager
from src.schemas.schemas import ContactSchema
from src.repository.contacts import create_contact

fake = Faker()


async def create_fake_contacts(num_contacts: int):
    async with sessionmanager.session() as db:
        for _ in range(num_contacts):
            fake_contact = ContactSchema(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
                additional_data="foobar",
            )

            await create_contact(fake_contact, db)


if __name__ == "__main__":
    asyncio.run(create_fake_contacts(num_contacts=30))
