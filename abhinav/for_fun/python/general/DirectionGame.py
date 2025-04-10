'''
This is an RPG game.
'''

def showInstructions():
    print('''
RPG Game
========

Get to the Garden with a key and a potion
Avoid the monsters!

You are getting tired, each time you move you loose 1 health point.

Commands:
  go [direction]
  get [item]
''')
def showStatus():
  print('---------------------------')
  print(name + ' is in the ' + currentRoom)
  print("Health : " + str(health))
  print("Inventory : " + str(inventory))
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  print("---------------------------")

# setup the game
name = None
health = 10
currentRoom = 'Hall'
inventory = []

rooms = {

            'Hall' : { 'south' : 'Dining Room',
                  'east'  : 'Smallest Room',
                  'north' : 'Garden'
                },

            'Kitchen' : { 'north' : 'Intersection',
                  'item'  : 'monster'
                },

            'Dining Room' : { 'north'  : 'Hall',
                    'east' : 'Bed Room',
                    'west' : 'Intersection'

                },

            'Garden' : { 'south' : 'Hall' },

            'Smallest Room':{'west' : 'Hall'},

            'Bed Room' : {'west' : 'Dining Room',
                'item' : 'key'},
            'Intersection' : {'north' : 'Master Room',
                'south' : 'Kitchen'},
            'Master Room' : {'item': 'potion',
                'south' : 'Intersection'},

         }

if name is None:
  name = input("What is your name Adventurer? ")
  showInstructions()

while True:

  showStatus()

  move = ''
  while move == '':
    move = input('>')

  move = move.lower().split()

  if move[0] == 'go':
    health = health - 1
    if move[1] in rooms[currentRoom]:
      currentRoom = rooms[currentRoom][move[1]]
    else:
      print('You can\'t go that way!')
      health += 1

  if move[0] == 'get' :
    if 'item' in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      inventory += [move[1]]
      print(move[1] + ' got!')
      del rooms[currentRoom]['item']
    else:
      print('Can\'t get ' + move[1] + '!')

  if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
    print('A monster has got you... GAME OVER!')
    break

  if health == 0:
    print('You collapse from exhaustion... GAME OVER!')

  if currentRoom == 'Garden' and 'key' in inventory and 'potion' in inventory:
    print('You escaped the house... YOU WIN!')
    break

  if currentRoom == 'Garden'  and 'potion' in inventory:
      print('The door is locked. You will need the key.')
  if currentRoom == 'Garden' and 'key' in inventory:
      print('You will need the potion to escape.')

  if currentRoom == 'Garden':
      print('You will need the key and potion to escape.')