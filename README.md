# Knackles

Knackles is an async ORM.  Knackles is currently under development and
this documentation serves as a reference for implementation.

python```
from knackles import Model, CharField, IDField, PostgresDatabase

database = PostgresDatabase(host='postgres', user='pguser', password='moonmoonwhy', database='moon_test')

class User(Model):
    name     = CharField(size=100)
    password = CharField(size=32)
    language = CharField(size=32, default='english')

async def main():
    # Create table
    await User.table.create()

    # Create a user
    user = await User.create(name='kim', password='batterystaplehorse')

    # Create a user another way
    user = User()
    user.name = 'john'
    user.password = 'password1'
    await user.save()

    # Fetch a user
    user = await User.get(name='test')

    # Fetch many users
    users = User.where(language='english')
    async for user in users:
        print(user.name)

    # Update many users
    await User.where(language='english').update(language='turbo_memes')

    # Delete many users
    await User.where(language='english').delete()

    # Atomic
    async with database.atomic():
        await User.create(name='i_wont_exist', password='password2')
        await User.create(name='i_have_no_password')


from asyncio import get_event_loop
loop = get_event_loop()
loop.run_until_complete(main())
```

## Planned Features
 * Atomic Transactions
 * Foreign Keys
 * Many to Many
 * Mysql Support
 * SQLite Support