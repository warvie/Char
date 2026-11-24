# Dead Ground

A 3D zombie-apocalypse survival game that runs in the browser. Raid ruined towns, hunt in the wilds, dig into caves, build walls before nightfall, and get an old car running.

## Play

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). It needs an internet connection the first time to load Three.js from cdnjs.

To play from a link, turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**. The game will be at `https://warvie.github.io/char/`.

## The world

- **320 × 320 m world** built from half-metre pixel-textured blocks: a large central town plus several smaller towns, rolling hills and mountains, forests and caves. Every world comes from a **seed**, so the same seed always builds the same world.
- **Chunk streaming:** only the 8 × 8 m chunks around the players are meshed; the rest load in as you move and unload behind you. Pick a render distance from 32 to 128 m. Fog and camera range follow it.
- **Realistic towns:** 6 m two-lane roads, 1.5 m sidewalks, 15 m lots, and houses 11–15 m across with 3.5 m floors, 1–3 storeys, framed windows (some smashed or boarded), front and back doors, stairs and roof access.
- **Furnished rooms:** each floor is split into rooms joined by doorways and doors.
  - Living rooms: couch facing a TV on a TV stand, coffee table, rug, armchair, bookcase.
  - Kitchens: fridge, counters, sink and stove, plus a table and chairs.
  - Bathrooms: tiled floor, bathtub, toilet, and a sink with a mirror.
  - Bedrooms: bed, nightstand, wardrobe, dresser.
  - Basements (in some houses): shelves, a workbench and a water heater.
  - Furniture is solid.
- **Sewers** under every town road, reached through open manholes with ladders.
- **Caves** that open into the hillsides and wind underground, with exposed coal and iron, stalactites and stashes.

## Surviving

- **Zombies** are slow by day and fast at night. They jump 2 blocks, smash wood, glass and doors, and at night even stone. Some wear hard hats, helmets, vests or jackets that soak up damage.
- **Shooting:** bullets leave holes where they hit. Shoot off arms and legs: legless zombies crawl, armless ones bite weaker, and a headshot pops the head off. Cars and tripwire bombs tear limbs off too.
- **Loot:** crates in houses, basements, sewers and caves. Dead zombies drop loot bags, sometimes with the clothing they wore.
- **Wild animals:** deer and rabbits flee, wolves hunt in packs (worse at night), and boars charge if you get close. Kill them for raw meat, hide and bone. Cook meat at a campfire, because raw meat can make you sick.
- **Clothing and armor:** hard hat, metal helmet, leather jacket, police vest, hide coat, scrap armor, padded pants, riot pants. Each blocks part of the incoming damage, up to 70%. Wear them from the backpack.
- **Crafting** at the workbench in the backpack:
  - Materials: planks, metal plates, ammo (from scrap or bone), bandages, repair kits, fuel.
  - Placeables: spike traps, bear traps, tripwire bombs, beds, campfires.
  - Wearables: helmets, armor, coats, pants.
- **Building and digging:** place plank, stone, dirt or metal blocks and dig anything except bedrock. Build walls 3 high in stone or metal.
- **Beds:** sleep through the night (in co-op, both players lie down). A bed also sets your respawn point.
- **Vehicles:** sedans and pickup trucks need fuel and repairs.
  - First-person cabin with a turning steering wheel, working gauges, seats and mirror, or switch to the outside view.
  - Run zombies over and carry a passenger.
- Health, hunger, stamina, day/night cycle and flashlight. The light turns on by itself underground.

## Saving

The world is rebuilt from its seed, so a save only stores the seed plus the blocks you changed (delta + varint packed), your inventories, clothing, beds, fires, traps, cars, opened doors and looted crates, then deflated. A whole game fits in a short **save code** (about 1–2 KB). The game also autosaves in your browser every 90 seconds. Use **Continue**, or paste a code into **Load a save code**.

## Controls

**Player 1:** WASD move · mouse look · click act · right-click place block · 1–5 / wheel tools (bat, pistol, pickaxe, build, place) · R block material or item to place · E use / doors / loot / sleep / cook / enter car · V driver or outside view · Space jump (brake in car) · Shift sprint · Tab backpack · G eat · X bandage · T flashlight

**Player 2:** I K / J L move & turn · U / O look · H act · Y use · N jump · P sprint · B tool · M material or item · , car view · [ eat · ] bandage · \ backpack · or a gamepad

**Touch:** drag the left side to move, drag the right side to look · Act, Jump, Use, Place buttons bottom right · Bag, Tool, Type, View, Run along the top
