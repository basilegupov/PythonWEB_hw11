from logger import logger
from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# from fastapi import HTTPException
from src.entity.models import Contact
from src.schemas.schemas import ContactSchema, ContactUpdateSchema, ContactBirthdayResponse


async def get_contacts(limit: int, offset: int, db: AsyncSession, search: str = None):
    stmt = select(Contact).offset(offset).limit(limit)
    if search:
        search = f"%{search}%"
        stmt = stmt.filter(
            (Contact.first_name.ilike(search))
            | (Contact.last_name.ilike(search))
            | (Contact.email.ilike(search))
        )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_upcoming_birthdays(db: AsyncSession):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    logger.info(f"today: {today}, end_date: {end_date}")
    stmt = select(Contact).filter(
        func.date_part('month', Contact.birthday) == today.month,
        func.date_part('day', Contact.birthday) >= today.day,
        func.date_part('day', Contact.birthday) <= end_date.day
    )
    contacts = await db.execute(stmt)
    birthdays = contacts.scalars().all()
    upcoming_birthdays = [ContactBirthdayResponse(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        additional_data=contact.additional_data
    ) for contact in birthdays]

    return upcoming_birthdays
