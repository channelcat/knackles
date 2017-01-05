from knackles import Model, CharField, IDField, PostgresDatabase

database = PostgresDatabase(host='postgres', user='pguser', password='moonmoonwhy', database='moon_test')

class User(Model):
    name     = CharField(size=100, default='penis')
    password = CharField(size=32, name='passwort')

async def main():
    #await User.table.create()
    user1 = await User.create(name='test', password='poop')
    user2 = User()
    user2.name = 'test2'
    await user2.save()
    user = await User.get(name='test')
    print(user.name)

from asyncio import get_event_loop
loop = get_event_loop()
loop.run_until_complete(main())