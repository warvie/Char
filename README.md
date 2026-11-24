# Dead Ground

A 3D zombie-apocalypse survival game that runs in the browser. Raid ruined towns, hunt in the wilds, dig into caves, build walls before nightfall, and get an old car running.

## Play

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). It needs an internet connection the first time to load Three.js from cdnjs.

To play from a link, turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**. The game will be at `https://warvie.github.io/char/`.

## The world

- **320 × 320 m world** built from half-metre pixel-textured blocks, with quarter-height grass caps that smooth hills and slopes, a large central town plus several smaller towns, rolling hills and mountains, forests and caves. Every world comes from a **seed**, so the same seed always builds the same world.
- **Chunk streaming:** only the 8 × 8 m chunks around the players are meshed; the rest load in as you move and unload behind you. Pick a render distance from 32 to 128 m. Fog and camera range follow it.
- **Realistic towns:** 6 m two-lane roads, 1.5 m sidewalks, 15 m lots, and houses 11–15 m across (level with the sidewalks) with 3.5 m floors, 1–3 storeys, painted drywall in a different colour per room, real stair blocks (two steps per block) with wooden or iron railings, framed windows (some smashed or boarded), front and back doors, stairs and roof access.
- **Furnished rooms:** each floor is split into rooms joined by doorways and doors.
  - Living rooms: couch facing a flat-screen or an old CRT TV (rabbit ears, VCR) on a TV stand, coffee table, rug, armchair, bookcase.
  - Kitchens: fridge, counters, sink and stove, plus a table and chairs.
  - Bathrooms: tiled floor, bathtub, toilet, and a sink with a mirror.
  - Bedrooms: bed, nightstand, wardrobe, dresser.
  - Basements (in some houses): shelves, a workbench and a water heater.
  - Furniture is solid.
- **Sewers** under every town road, reached through open manholes with ladders.
- **Caves** that open into the hillsides and wind underground, with exposed coal and iron, stalactites and stashes.

## Graphics

Four quality levels (start screen or backpack). They change effects only, never the resolution:
- **Ultra:** everything in High, plus **pixel ray tracing**. A 3D copy of the nearby blocks lives on the GPU, and for every texture pixel (16 per block side, the same as the textures) a ray is traced to the sun for shadow, with short rays for corner shading. Sunlight falls through windows in pixel-exact patches. Needs WebGL2, and is the default on desktop.
- **High:** pixelated sun shadows, crepuscular rays, lens flare that hides when the sun is blocked, motion blur, real-time rain reflections, edge smoothing, drifting ground fog, distance haze, vignette and color grading.
- **Medium:** lighter shadows and effects, no motion blur.
- **Low:** fastest, the default on phones.

Shadows are snapped to texture pixels on every level that has them. When it rains, everything open to the sky gets wet: it darkens, and roads, roofs and car roofs reflect the scene in real time with puddles and ripples, then dry off after the rain.

Also on every level: a sky dome with sun, moon and stars; pixel textures that span 2×2 blocks so bricks, planks and tiles run continuously; swaying grass tufts; and seasonal ambience (ash and dust, fireflies, falling leaves, snow and rain that stop at roofs, embers and flies).

Performance: chunk streaming, packed vertices (16 bytes instead of 44, about 60% less GPU memory), typed-array meshing, merged furniture, frozen static meshes, only large parts casting shadows, shadow maps refreshed every few frames, and dynamic render scale that only drops if frames get slow.

## Surviving

- **Zombies** are slow by day and fast at night. They notice you only within range (22 m by day, 34 m at night) and in line of sight, give up once you're well out of range, and come to investigate gunshots. They break blocks hit by hit: a window in one hit, a wooden door in about 10 s, a brick wall only with a crowd. Metal holds longest. Some wear hard hats, helmets, vests or jackets that soak up damage.
- **Aiming:** hold right-click (pistol) to aim down sights, which is more accurate but slower. There's a light aim assist toward visible targets, a bit stronger on touch and gamepad.
- **Shooting:** bullets leave holes where they hit. Shoot off arms and legs: legless zombies crawl, armless ones bite weaker, and a headshot pops the head off. Cars and tripwire bombs tear limbs off too.
- **Loot:** crates in houses, basements, sewers and caves. Dead zombies drop loot bags, sometimes with the clothing they wore.
- **Wild animals:** deer and rabbits flee, wolves hunt in packs (worse at night), and boars charge if you get close. Kill them for raw meat, hide and bone. Cook meat at a campfire, because raw meat can make you sick.
- **Clothing and armor:** hard hat, metal helmet, leather jacket, police vest, hide coat, scrap armor, padded pants, riot pants. Each blocks part of the incoming damage, up to 70%. Wear them from the backpack.
- **Crafting** at the workbench in the backpack:
  - Materials: planks, metal plates, ammo (from scrap or bone), bandages, repair kits, fuel.
  - Placeables: spike traps, bear traps, tripwire bombs, beds, campfires.
  - Wearables: helmets, armor, coats, pants.
- **Building and digging:** place plank, stone, dirt, metal or stair blocks (stairs face the way you're looking) and dig anything except bedrock. Build walls 3 high in stone or metal.
- **Seasons:** spring, summer, autumn and winter turn every 3 days.
  - Seasonal grass and leaves, and in winter snow on the ground, roads, roofs and trees.
  - Rain, storms and snowfall; winter days are shorter.
  - Cold drains your warmth unless you're indoors, by a fire, in a car or wearing a coat.
- **People:** survivors in the towns shoot zombies and trade with you. Bandits in the wilds shoot on sight.
- **Beds:** sleep through the night (in co-op, both players lie down). A bed also sets your respawn point.
- **Vehicles:** sedans, pickups, vans, police cruisers, ambulances, city buses and motorcycles. They need fuel and repairs, and they collide with each other, with people and with animals (you can stand on the roofs).
  - First-person cabin at real seat height: you see your own body at the wheel and most of the road.
  - Turning steering wheel, working gauges and a **live rear-view mirror**; many vehicles have a **backup camera** screen with guide lines when reversing.
  - Or switch to the outside view.
  - Run zombies over and carry a passenger.
- Health, hunger, stamina, day/night cycle and flashlight. The light turns on by itself underground.

## Saving

The world is rebuilt from its seed, so a save only stores the seed plus the blocks you changed (delta + varint packed), your inventories, clothing, beds, fires, traps, cars, opened doors and looted crates, then deflated. A whole game fits in a short **save code** (about 1–2 KB). The game also autosaves in your browser every 90 seconds. Use **Continue**, or paste a code into **Load a save code**.

## Controls

**Player 1:** WASD move · mouse look · click act · right-click place block · 1–5 / wheel tools (bat, pistol, pickaxe, build, place) · R block material or item to place · E use / doors / loot / sleep / cook / enter car · V driver or outside view · Space jump (brake in car) · Shift sprint · Tab backpack · G eat · X bandage · T flashlight

**Player 2:** I K / J L move & turn · U / O look · H act · Y use · N jump · P sprint · B tool · M material or item · , car view · [ eat · ] bandage · \ backpack · or a gamepad

**Touch:** drag the left side to move, drag the right side to look · Act, Jump, Use, Place buttons bottom right · Bag, Tool, Type, View, Run along the top
