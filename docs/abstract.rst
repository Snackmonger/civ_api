================
Civ-API Abstract
================

How does the game work?
-----------------------

Turn-based-gameplay.
    - Get information about a city, unit, etc. (API GET)
    - Issue orders to individual units on a turn (API POST)
        - Server calculates effects of orders and returns a response.
    - Issue 'end turn' notice (API POST).
        - Server calculates enemy moves and random events and returns a response.
    - The response contains details about enemy movements if they occurr within n tiles of a unit belonging to user.

Territorial acquisition.
    - Cities will expand territory when their population reaches max and they have a surplus of food.
    - Additional tiles added to the city will contribute to the city economy.
    - Tiles may make certain resources available to the player.

Battle between units.
    - Units and cities will be able to attack and defend in battle.
    - An attack posts an event requesting the battle calculation.
    - The game master receives the event, does the calculation, and applies the damage, etc. to the units.


What does the database need to track?
-------------------------------------

Players, Cities, Units
++++++++++++++++++++++

- Every player has a unique ID. In our game, one player must be human, and the others will be computers.
- A player may create cities. Each city has a unique ID and a common player ID, as well as other qualities.
- A player may create units. Each unit has a unique ID and common player ID, as well as other qualities.
- A user either has or doesn't have a certain perk or wonder, so we store the user ID as a unique key and a series of boolean flags as values.
- Likewise, a city either has or doesn't have a certain building or upgrade, so these are stored as booleans under a city ID key.
- Likewise, a unit either has or doesn't have a certain upgrade or status effect, so these are stored as booleans under a unit ID key.

Organized by Player ID 
    -  (player_id, player_type {human / computer, player_name, player_money, ...)
    -  (player_id, perk_1, perk_2, perk_3, ...)
    -  (player_id, wonder_1, wonder_2, wonder_3, ...)

City instances.
    - (city_id, city_name, player_id, city_x, city_y, number_of_citizens, city_level, city_def, city_atk, culture_pt, science_pt, ...) 
    - (city_id, next_to_water, next_to_desert, etc. [populated from the map tiles])
    - (city_id, building_1, building_2, building_3, ...)

Unit instances.
    - (unit_id, unit_name, player_id, unit_x, unit_y, unit_def, unit_atk, ...)
    - (unit_id, unit_upgrade_1, unit_upgrade_2, ...)


Map Tiles
+++++++++

- The map is made up of tiles. Each tile has qualities related to resources and terrain difficulty.
- A tile can be occupied by a city or a military unit, but it cannot be created or destroyed by the players.
- If a tile is occupied by a city, the city can be reinforced by a unit that occupies the same tile. 
- If a tile is occupied by a development upgrade, it can be occupied by a unit.
- Apart from this situation, an occupied tile cannot be occupied by another entity unless a military operation takes place.
- If the tile is occupied by a natural feature (mountain, river), the tile is impassable or passable depending on the user's perks (fording, mountaineering) and/or developments (bridge, mountain pass)

Organized by Tile ID
    - list [Tile ID] (tile_id, user_id, is_occupied, occupier_id, movement_penalty, resource_amounts)
    - list [tile_resources] (tile_id, resource_1, resource_2, resource_3)


Abstract Bases
++++++++++++++

- The abstract bases are unchanging values used to populate datasets of type instances
- A unit is an instance of a unit type defined by an abstract base.
- A unit type is something like "spearman", "stone age cavalry", where each unit type has a different atk/def, etc.
- A tile type is something like "desert", "grass plains", "tundra", where each tile type has different resources/terrain, etc.


Outline of Development 
----------------------

A 'thinking out loud' approach to refining some of the core concepts in a realistic way before committing too much to actual code.

1. Calculate a city's total RESOURCES by querying the city's TILES in the database and adding all available resources.

::

    total resources = {}
    for tile in city's tiles:
        for resource in tile's resources:
            if resource in total resources:
                total resources [resource] += tile's resources [resource]
            else:
                total resources [resource] = tile's resources [resource]


So... does the tile keep a dictionary of resources? are the resources dataclasses? is the tile an object or just a reference to the database? 

Maybe more like this:

::

    total resources = {}
    city tiles : list[dict[str, immutable type]] = self.get(TILES)
    for tile in city tiles:
        t = Tile(*tile)
        for resource in t.resources:
            if resource in total resources:
                total resources [resource] += tile's resources [resource]
            else:
                total resources [resource] = tile's resources [resource]

Where self.get() is a method supplying tables from the database like this:

::

    class City:
        init(self, ..., parameters, ...)
        ...
        self.callbacks: dict[str, callable] = {}
    
        def ... business logic ...
    
        def add callback(self, callback) -> none
            if not callback in self.callbacks  -> add callback
    
        def get(self, table_name) -> list[dict]
            -> self.callbacks[GET](self, table_name)


Where the callback is supplied by a higher-level controller or delegate. Therefore, city does not need to know about the database implementation, it just forwards the relevant info.

But then again, this calls into question: when does the city object get created? should the city's tiles simply be populated as objects when the city is created? 
Then the controller can have access to the database and feed the current information to the city object builder, and the city manipulates the data without needing to
use callbacks to get additional data? But surely the city will occasionally need to get information about tiles outside its components: when deciding which unoccupied
tile to spread to? when deciding whether an enemy has been spotted on the horizon?

Let's think this through:

The game is supposed to go through an API. You submit an attack, get the result as a response. You submit a city improvement, get a recipt as a response (or something like that). 
Whenever the API call is over, you either sent a POST/PUT request to be written into the database (e.g. an attack calculates the damage of the parties involved & adjusts the values
of those parties in the database), or you sent a GET request to read the current state, and no change to the database happened. None of the objects are needed after the write operation
takes place, and if there is no write operation, then no objects are needed and we can simply pull data from the database.

The time between POST requests might be a long time, and the game cannot keep objects in memory for no reason. This is a stateful game!

Therefore, the API-based app is responsible for 

    1. initializing the main game controller with the current game state whenever a POST request is received 
    2. asking the main game controller to perform an operation on some state contained in its components
    3. writing the result of the operation into the database
    4. returning an appropriate response with the results of the operation

So what happens to the game object after this? Does it just go out of scope and get garbage collected? I suppose so, since the next call is presumably responsible
for initializing a new controller as described above, and the old one is not needed. 

When initializing the game controller, we can write a function to calculate all tiles that are 'visible' to game entities, and create tile objects for those tiles,
since we know (or suspect) that they will probably be involved in an operation in some way or other. Then, when a tile is needed by the controller, it calls another
function that either retrieves a known tile from the list of objects, or if the tile is not know, creates it and adds it to the list before returning it.
Creating a list of tile objects is costly, especially if we only need a few. for the same reason, the map creation doesn't need to create tile objects at all, since it's
just populating the database from which the needed objects can be generated.


2. A tile should be markable as 'owned' as well as 'occupied'

- better yet: owner = 'empire name' | None


3. A city must dedicate 1 POPULATION to each tile in order to exploit its resources.

- an entity representing each unit of population?
- population_uuid, current_tile, is_working, 
- but we don't want the worker to count as an entity when deciding whether another entity can stand on the tile
- the worker represents the 'base productivity' of a worked tile, and it's different from the 'builder' unit 
that constructs roads, tile improvements, and can be 'occupied' by a military unit for protection or captured by an enemy. 
The worker cannot be captured, it just belongs conceptually to the city.
- maybe this is just a boolean in the tile :: worked =  True, then the city counts how many population it has and restricts the 
number of worked tiles to that amount. 'Reassign' a worker by turning one bool off and another on.

4. A city must provide FOOD to its population in order for them to work.
5. A starving city should be able to revolt, but let's leave that aside for the time being. (also, too many unemployed population?)

- food is provided by worked tiles with food resources, or by buildings in the city
- if a city is not fully fed, the supply/demand of food will decide how much happiness is affected
- a city lacking a little food will be able to function, but not at optimal levels, and will have a slower path forwards
- but a city lacking a lot of food will also be subject to civil unrest (creating hostile units near the city) and revolt (lose the city)


6. As the city accumulates resources, it is able to build BUILDINGS with them
7. Buildings in the city will allow the city to be more efficient in producing resources, and they provide amenities, bonuses, upgrades, etc.
8. The population of the city always produces a certain amount of CULTURE and SCIENCE per turn. Some buildings also produce culture and science.
9. Culture and science allow the user to progress through the CIVICS TREE and TECHNOLOGY TREE respectively.
10. Instead of a building, the city can work toward creating a cultural or scientific achievement, which will improve the city's future output and may confer other bonuses.
11. Instead of a building, the city can build UNITS for military, diplomatic, and mercantile purposes.

Even without worrying about how to handle player-to-player interaction vis-a-vis diplomacy, trade, and battle, 
we have an enormous amount of basic city growth work to do. In the list above 1-4 and 6-8 seem pretty doable with the material we have already written.
