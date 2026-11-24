# Dead Ground

A 3D zombie-apocalypse survival game that runs in the browser. Raid ruined towns, hunt in the wilds, dig into caves, build walls before nightfall, and get an old car running.

## Play

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). It needs an internet connection the first time to load Three.js from cdnjs.

To play from a link, turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**. The game will be at `https://warvie.github.io/char/`.

## The world

- **320 × 320 m world** built from half-metre pixel-textured blocks, with quarter-height grass caps that smooth hills and slopes, a large central town plus several smaller towns, rolling hills and mountains, forests and caves. Every world comes from a **seed**, so the same seed always builds the same world.
- **Chunk streaming:** only the 8 × 8 m chunks around the players are meshed; the rest load in as you move and unload behind you. Pick a render distance from 32 to 128 m. Fog and camera range follow it.
- **Realistic towns:** 6 m two-lane roads, 1.5 m sidewalks, 15 m lots, and houses 11–15 m across (level with the sidewalks) with 3 m storeys (2.5 m ceilings), 1–3 storeys, painted drywall in a different colour per room with baseboards and crown moulding, switchback staircases with landings (two steps per block) and wooden or iron railings, framed windows (some smashed or boarded), front and back doors, stairs and roof access.
- **Public buildings:** each town has some of these, under faded signs over the doors.
  - **Hospitals** (2–3 storeys): reception, waiting chairs, wards with hospital beds and IV stands, medicine cabinets and a pharmacy full of bandages.
  - **Grocery stores:** a plate-glass storefront, stocked aisles, checkouts, drinks coolers and a stockroom. Mostly food.
  - **Hardware stores:** tool aisles, lumber racks and pegboard walls. Scrap, metal, planks, fuel, repair kits and traps.
  - **Schools** (2 storeys): classrooms with chalkboards and rows of desks, lockers along the corridors and a cafeteria.
- **Battle damage:** most buildings came through intact, with whole windows. About 3 in 10 took real damage, and those are mostly chipped rather than holed. Walls and roofs have chunks bitten out of blocks, with the broken pieces lying in rubble piles below. Only a few blocks are knocked clean through, and roofs have ragged holes with debris on the floor underneath. 
- **Every block breaks in stages:** dirt, grass, stone, ore, concrete, brick, drywall, roof, asphalt, planks, logs, metal, tile and window frames all go through three broken stages (chipped, heavily damaged, crumbled stub) before they give way. That happens under your pickaxe, zombie claws and explosions, and the broken pieces land as rubble. A block that is already damaged breaks faster.
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

**Pixel size** (start screen or case): the 3D view renders at ½, ⅓ or ¼ of the screen resolution and is scaled up with hard pixel edges (×2 by default), or *Smooth* for full resolution. The UI is pixelated to match, with pixel fonts, hard bevels and hand-drawn 16×16 pixel-art icons.

Four quality levels (start screen or case). They change effects only:
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
- **Loot:** crates in houses (each public building stocks its own kind of loot), basements, sewers and caves. Dead zombies drop loot bags, sometimes with the clothing they wore.
- **Wild animals:** deer and rabbits flee, wolves hunt in packs (worse at night), and boars charge if you get close. Kill them for raw meat, hide and bone. Cook meat at a campfire, because raw meat can make you sick.
- **Clothing and armor:** hard hat, metal helmet, leather jacket, police vest, hide coat, scrap armor, padded pants, riot pants. Each blocks part of the incoming damage, up to 70%. Wear them from the case.
- **Crafting** at the workbench in the case:
  - Materials: planks, metal plates, ammo (from scrap or bone), bandages, repair kits, fuel.
  - Placeables: spike traps, bear traps, tripwire bombs, beds, campfires.
  - Wearables: helmets, armor, coats, pants.
- **Building and digging:** place plank, stone, dirt, metal or stair blocks (stairs face the way you're looking) and dig anything except bedrock. Build walls 3 high in stone or metal.
- **Seasons:** spring, summer, autumn and winter turn every 3 days.
  - Seasonal grass and leaves, and in winter snow on the ground, roads, roofs and trees.
  - Rain, storms and snowfall; winter days are shorter.
  - Cold drains your warmth unless you're indoors, by a fire, in a car or wearing a coat.
- **People:** a fixed cast of named survivors and bandits with realistic names. Nobody respawns: when someone dies, they're gone for good and drop off the leaderboard. Out of sight, they keep fighting each night, and now and then one doesn't make it (you'll hear it on the radio).
  - About half the houses still have a survivor living in them. By day they forage (raid crates, hunt, pick up carcasses) and carry food back to a stash. They board up open windows and set spike traps at the door.
  - At night they go home, open the door, close it behind them and sleep. About 1 in 4 are night owls who keep scavenging.
  - They shoot zombies and trade with you. Raid a stash while its owner sees you and they turn hostile.
  - Bandit gangs of 2–4 camp around fires and tents in the wilds and shoot on sight.
- **Leaderboard:** hold **Z** (or open your case) to see zombies killed, people killed and nights survived for you and everyone still alive. Click a column to sort. Your nights count resets when you die.
- **Attaché case (Tab):** a grid inventory like Resident Evil 4. Every item has a size (a fuel can is 2×2, a jacket 2×3, the bat 4×1) and stacks up to a limit. Drag items to arrange them, rotate them with R or right-click while dragging, or tap *Organize*. Select an item to use, wear, rotate or drop it. If you pick up more than fits, the extra drops in a bag at your feet.
- **Tents:** abandoned campsites dot the countryside, bandits camp in them, and you can sew your own (5 cloth + 3 wood). Sleep in one like a bed.
- **Respawn:** when you die, choose your bed, the crossroads or a random town. The case also has a *Respawn (stuck?)* button.
- **Beds:** sleep through the night (in co-op, both players lie down). A bed also sets your respawn point.
- **Bicycles:** left by front doors and along the roads. No fuel needed, just pedalling (which makes you hungrier); about 30 km/h, quiet, and they bounce off zombies instead of running them down. One rider only.
- **Vehicles:** sedans, pickups, vans, police cruisers, ambulances, city buses and motorcycles. They need fuel and repairs, and they collide with each other, with people and with animals (you can stand on the roofs).
  - First-person cabin at real seat height: you see your own body at the wheel and most of the road.
  - Turning steering wheel, working gauges and a **live rear-view mirror**; many vehicles have a **backup camera** screen with guide lines when reversing.
  - Or switch to the outside view.
  - Run zombies over and carry a passenger.
- Health, hunger, stamina, day/night cycle and flashlight. The light turns on by itself underground.

## Saving

The world is rebuilt from its seed, so a save only stores the seed plus the blocks you changed (delta + varint packed), your inventories, clothing, beds, fires, traps, cars, opened doors and looted crates, then deflated. A whole game fits in a short **save code** (about 1–2 KB). The game also autosaves in your browser every 90 seconds. Use **Continue**, or paste a code into **Load a save code**.

## Controls

**Player 1:** WASD move · mouse look · click act · right-click place block · 1–5 / wheel tools (bat, pistol, pickaxe, build, place) · R block material or item to place · E use / doors / loot / sleep / cook / enter car · V driver or outside view · Space jump (brake in car) · Shift sprint · Tab attaché case · Z (hold) leaderboard · G eat · X bandage · T flashlight

**Player 2:** I K / J L move & turn · U / O look · H act · Y use · N jump · P sprint · B tool · M material or item · , car view · [ eat · ] bandage · \ case · or a gamepad

**Touch:** drag the left side to move, drag the right side to look · Act, Jump, Use, Place buttons bottom right · Bag, Tool, Type, View, Run along the top
