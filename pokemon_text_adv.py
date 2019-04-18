##
## ****************************************************
##   Ali Zohair (20762382)
##   CS 116 Winter 2019
##   Assignment 09
## ****************************************************
##



class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
    def __repr__(self):
        return '<exit {0}>'.format(self.name)
# c = Exit('a', Room())
class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        look(self, noun) consumes a World and a string noun and returns None and does one of the
        following depending on what noun is: Look at the player, look at the room,
        look at item in inventory, look at item in room, or prints an error 
        message if that is not seen.
        Effects: 
        Prints to screen
        look: World Str -> None
        '''
        if noun == 'me':
            self.player.look()
        elif noun == 'here':
            self.player.location.look()
        else:
            for things in self.player.inventory:
                if things.name == noun:
                    return things.look()
            for things in self.player.location.contents:
                if things.name == noun:
                    return things.look()
            print(self.msg_look_fail)
            
    def inventory(self):
        """
        inventory(self) consumes a World and returns None. It prints the
        inventory of the player, or an error message stating the inventory is empty.

        Effects: 
        Prints to the screen
        
        inventory: World -> None
        """
        if self.player.inventory != []:
            items = ''
            for things in self.player.inventory:
                items += things.name + ', '
            items1 = items[0:-2]
            print ('Inventory: ' + items1)
        else:
            print(self.msg_no_inventory)

        # print( '[NOT IMPLEMENTED] inventory' )  
            
    def take(self, noun):
        """
        take(self, noun) consumes a World and a noun, and adds the noun to the player inventory
        if it is in the players room.
        Effects: 
        Mutates Room's contents and Player's inventory i.e. Mutates World
        Prints to the screen

        take: World Str -> None
        """
        for thing in self.player.location.contents:
            if thing.name == noun:
                self.player.inventory.append(thing)
                self.player.location.contents.remove(thing)
                print(self.msg_take_succ)
                return
        print(self.msg_take_fail)
            


                    
    def drop(self, noun):
        """
        drop(self, noun) consumes a World and a noun, removes the noun from the players
        inventory if noun exists in Player's inventory and mutates noun by adding noun to Room's contents.
        
        Effects: 
        Mutates world i.e. mutates Room's contents and Player's inventory
        Prints to the screen

        drop: World Str -> None
        """
        for things in self.player.inventory:
            if noun == things.name:
                self.player.inventory.remove(things)
                self.player.location.contents.append(things)
                print(self.msg_drop_succ)
                return
        print(self.msg_drop_fail)
        ## Replace this body with your owngo shop
        # print( '[NOT IMPLEMENTED] drop' )
        
    def go(self, noun):
        """
        go(self, noun) consumes a world, and noun(name of an exit), and mutates the player's location
        to the room indicated by the given Exit if player's inventory has the key for Exit 
        or Exit has no key. Otherwise prints error message.

        Effects: 
        Mutates world, by mutating player's contents
        Prints to screen
        go: World Str -> None
        """
        for elem in self.player.location.exits:
            if elem.name == noun and elem.key == None:
                self.player.location = elem.destination
                return self.player.location.look()
            elif elem.name == noun and elem.key != None:
                if elem.key in self.player.inventory:
                    self.player.location = elem.destination
                    return self.player.location.look()
                else:
                    print(elem.message)
                    return
        print(self.msg_go_fail)
                
    def play(self): 
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3



    def save(self, fname):
        """
        save(self, fname) consumes a World and a Str fname (name of file), and
        saves the current gamestate by writing to a text file to be resumed later.
        
        Effects:
        Writes to a file fname

        save: World Str -> None
        """
        all_things = []
        op = open(fname, 'w')
        for room in self.rooms:
            all_things.extend(room.contents)
        all_things.extend(self.player.inventory)
        for thing in all_things:
            ws = 'thing #{0} {1}\n'.format(thing.id, thing.name)
            op.write(ws)
            op.write('{0}\n'.format(thing.description))
        for room in self.rooms:
            ws = 'room #{0} {1}\n'.format(room.id, room.name)
            op.write(ws)
            op.write('{0}\n'.format(room.description))
            thing_ids =[]
            for item in room.contents:
                thing_ids.append(str(item.id))
            s = ' #'.join(thing_ids)
            if thing_ids == []:
                op.write('contents\n')
            else:
                op.write('contents #{0}\n'.format(s))
        ######################## player:
        op.write('player #{0} {1}\n'.format(self.player.id, self.player.name))
        op.write('{0}\n'.format(self.player.description))
        thing_ids = []
        for item in self.player.inventory:
            thing_ids.append(str(item.id))
        s = ' #'.join(thing_ids)
        if thing_ids == []:
            op.write('inventory\n')
        else:
            op.write('inventory #{0}\n'.format(s))
        op.write('location #{0}\n'.format(self.player.location.id))
        ####################### exits:
        for room in self.rooms:
            loc = room.id
            for exits in room.exits:
                dest = exits.destination.id
                if exits.key == None:
                    op.write('exit #{0} #{1} {2}\n'.format(loc, dest, exits.name))
                else:
                    op.write('keyexit #{0} #{1} {2}\n'.format(loc, dest, exits.name))
                    op.write('#{0} {1}\n'.format(exits.key.id, exits.message))


        op.close()


            

        


        

## Q2
def list_thing(info):
    '''
    list_thing(info) consumes a list info and returns a Thing based on info
    list_thing: (listof (listof Str) Str)

    '''
    id = int(info[0][1][1:])
    space = ' '
    new_name = space.join(info[0][2:])
    new_desc = info[1]
    item = Thing(id)
    item.name = new_name
    item.description = new_desc
    return item

def list_room(info, objects, objects_dict):
    '''
    list_room(info, objects, objects_dict) consumes a list info and objects(contains Thing information)
    and objects_dict(contains dictionary of Things) and returns a Room based on info
    list_room: (listof (listof Str) Str) (listof Str) (dictof Int Thing) -> Room

    '''
    #print(objects_dict)
    id = int(info[0][1][1:])
    space = ' '
    new_name = space.join(info[0][2:])
    new_desc = info[1]
    room = Room(id)
    room.name = new_name
    room.description = new_desc
    for item in objects[0][1:]:
        thing = int(item[1:])
        #print(objects_dict[thing])
        room.contents.append(objects_dict[thing])
    #print(room.contents)
    return room

def list_player(info, objects, objects_dict, location, rooms_dict):
    '''
    list_player(info, objects, objects_dict, location, rooms_dict) consumes a list info
    and objects(contains Thing information) and objects_dict(contains dictionary of Things)
    and location of the Player and a dictionary of Room and returns a Player based on info
    list_player: (listof (listof Str) Str) (listof Str) (dictof Int Thing) (Str) (dictof Int Room) -> Player

    '''
    id = int(info[0][1][1:])
    space = ' '
    new_name = space.join(info[0][2:])
    new_desc = info[1]
    player = Player(id)
    player.name = new_name
    player.description = new_desc
    for item in objects[0][1:]:
        thing = int(item[1:])
        player.inventory.append(objects_dict[thing])
    player.location = rooms_dict[int(location[1:])]
    return player
    
    


def load( fname ):
    """
    load(fname) consumes the name of a file, and returns a World generated from
    the file.
    Effects:
    Reads from a file.

    load: Str -> World
    
    """
    tf = open(fname, 'r')
    objects_dict ={}
    rooms_dict = {}
    next_str = tf.readline()
    line = next_str.split()
    # print(line[0])
    while line[0] != 'room':
        info =[]
        info.append(next_str.split())
        next_str = tf.readline()
        info.append(next_str[:-2])
        # print(info)
        objects_dict[int(info[0][1][1:])] = list_thing(info)
        next_str = tf.readline()
        line = next_str.split()
    while line[0] != 'player':
        info = []
        objects = []
        info.append(next_str.split())
        next_str = tf.readline()
        info.append(next_str[:-2])
        next_str = tf.readline()
        objects.append(next_str.split())
        #print(objects_dict)
        ######################
        rooms_dict[int(info[0][1][1:])] = list_room(info, objects, objects_dict)
        ######################
        next_str = tf.readline()
        line = next_str.split()
    # print(rooms_dict)
    while line[0] != 'exit':
        info = []
        objects = []
        info.append(next_str.split())
        next_str = tf.readline()
        info.append(next_str[:-1])
        next_str = tf.readline()
        objects.append(next_str.split())
        next_str = tf.readline()
        location = next_str.split()[1]
        ######################
        player = list_player(info, objects, objects_dict, location, rooms_dict)
        ######################
        next_str = tf.readline()
        # print(next_str)
        line = next_str.split()
        if line == []:
            break
        # print(line)
    while next_str != '':
        info = []
        space = ' '
        info.append(line)
        # print(info)
        dest = int(info[0][2][1:])
        room_num = int(info[0][1][1:])
        name = space.join(info[0][3:])    
        exit1 = Exit(name, rooms_dict[dest])
        if line[0] == 'keyexit':
            next_str = tf.readline()
            line = next_str.split()
            key = objects_dict[int(line[0][1:])]
            message = space.join(line[1:])
            exit1.key = key
            exit1.message = message
        next_str = tf.readline()
        line = next_str.split()
        rooms_dict[room_num].exits.append(exit1) 

            
    tf.close()
    all_rooms = []
    for rooms in rooms_dict.values():
        all_rooms.append(rooms)
    # print(all_rooms)
    play_world = World(all_rooms, player)
    # return play_world
    return play_world

    

# (load('thingworld.txt'))
# testworld.play()


def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)




# testworld = load('testworld_key.txt')
# testworld.play()
# testworld.save('save_test.txt')
# testworld_key = makeTestWorld(True)

# testworld.play()