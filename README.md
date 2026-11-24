# Dead Ground

A 3D zombie-apocalypse survival game that runs in the browser. Raid ruined towns, hunt in the wilds, dig into caves, build walls before nightfall, and get an old car running.

## Play

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). It needs an internet connection the first time to load Three.js from cdnjs.

To play from a link, turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**. The game will be at `https://warvie.github.io/char/`.

## The world

- **An endless world** built from half-metre pixel-textured blocks, with quarter-height grass caps that smooth hills and slopes. It's split into 112 m regions, generated from the **seed** whenever you get near them, so the same seed always builds the same world and you can walk in any direction forever. A big town sits at the start; about 3 in 4 regions elsewhere have a small town (sometimes two), with rolling hills, forests and caves between.
- **Compression, in three tiers:**
  - The 3 × 3 regions around you (336 m square) are raw blocks in a ring buffer: what you can see and touch. Walk far enough and the window slides; nothing ever moves in memory except the region coming in.
  - Regions you just left are compressed in memory. Every cell is compared with the bare terrain the seed would grow there (heights, layers, even ore positions, which come from a hash), so only buildings, caves, trees and your changes survive. An LZ4-style pass then squeezes that, from 3.4 MB to about 100 KB per region (about 33×), losslessly. Coming back is instant.
  - Everything else is stored as nothing but the seed plus your edits. It is rebuilt exactly when you return.
- **Chunk streaming:** only the 8 × 8 m chunks around the players are meshed; the rest load in as you move and unload behind you. Pick a render distance from 32 to 80 m. Fog and camera range follow it.
- **Realistic towns:** 6 m two-lane roads, 1.5 m sidewalks, 15 m lots, and houses 11–15 m across (level with the sidewalks) with 3 m storeys (2.5 m ceilings), 1–3 storeys, painted drywall in a different colour per room with baseboards and crown moulding, switchback staircases with landings (two steps per block) and wooden or iron railings, framed windows (some smashed or boarded), front and back doors, stairs and roof access.
- **Public buildings:** each town has some of these, under faded signs over the doors.
  - **Hospitals** (2–3 storeys): reception, waiting chairs, wards with hospital beds and IV stands, medicine cabinets and a pharmacy full of bandages.
  - **Grocery stores:** a plate-glass storefront, stocked aisles, checkouts, drinks coolers and a stockroom. Mostly food.
  - **Hardware stores:** tool aisles, lumber racks and pegboard walls. Scrap, metal, planks, fuel, repair kits and traps.
  - **Schools** (2 storeys): classrooms with chalkboards and rows of desks, lockers along the corridors and a cafeteria.
- **Battle damage:** most buildings came through intact, with whole windows. About 3 in 10 took real damage, and those are mostly chipped rather than holed. Walls and roofs have chunks bitten out of blocks, with the broken pieces lying in rubble piles below. Only a few blocks are knocked clean through, and roofs have ragged holes with debris on the floor underneath. 
- **Every block breaks in stages:** dirt, grass, stone, ore, concrete, brick, drywall, roof, asphalt, planks, logs, metal, tile and window frames all go through three broken stages (chipped, heavily damaged, crumbled stub) before they give way. That happens under your pickaxe, zombie claws and explosions, and the broken pieces land as rubble. A block that is already damaged breaks faster.
- **Doors** get the same treatment: the jambs and head are the surrounding wall, with side casings, plinth blocks and a head casing of trim on both faces.
- **Windows** sit in ordinary wall (brick or concrete outside, painted drywall inside) with a proper casing of trim round the opening on both faces: side and head casings, a deeper sill and an apron under it.
- **Blood that coats things:** every droplet falls, and where it lands it leaves a stain on the face it hit, one texture-pixel square (6 cm) at a time. That covers tops of blocks, walls, ceilings and the sides of things, and it runs down over edges. Your bat and chainsaw get bloodier with every hit, and cars that run zombies down get stained across the body.
- **Blood:** pixel-art splatters with flung droplets where things die, spatter on nearby walls, and old dark pools in the streets where people fell months ago. No more red-tinted blocks.
- **Overgrowth:** about 1 in 5 houses (more of the damaged ones) is being taken back by nature: ivy climbing the outside walls and in through open windows, trailing down inside, weeds across the floors, and sometimes a sapling breaking through the boards.
- **Trees** have thin branches and twigs (14 cm and 8 cm thick) reaching off the trunk, ending in leaf clusters, or bare on dead trees.
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

**8 × 8 pixels per block:** every block face shows an 8 × 8 texture (point-sampled so mortar lines and board joints stay crisp).

**Pixel shadows everywhere:** every shadow (on blocks, furniture, grass, people and cars) is looked up on the same 1/16 m texture-pixel grid, so all shadow edges are pixelated.

**Rain:** wet, sky-exposed ground turns into a pixelated mirror. Reflections, ripples and glints are snapped to the texture-pixel grid, and anything under a roof stays dry.

**Realism:** the block textures got a pass for depth: bevelled bricks with burnt and pale ones mixed in, soot and grime, concrete pores and stains, wood grain and knots, rust running from rivets, shingle rows, leaf clusters and mottling everywhere, at the same pixel count. On High and Ultra the image gets **ambient occlusion** from the depth buffer (corners, creases and contact shadows) and a soft **glow** around bright light. Every level gets a **filmic tone curve**.

**Pause menu (Esc):** resume, *Respawn (unstuck)*, or **teleport** to your bed, the crossroads, the nearest town, a random town or your co-op partner.

**Unstuck:** a *Respawn* button is always on screen (and the ` key; = for player 2; *Unstuck* on phones). It puts you back at your respawn point with everything you're carrying, for when you glitch into something.

**No overlapping UI:** the HUD is laid out (and checked by script) for desktop, laptop, split-screen, phones in portrait and landscape, and tablets, so nothing sits on top of anything else.

**All-pixel UI:** a pixel font is built into the game (hand-drawn 5×7 glyphs turned into a real font at startup), so every label, menu, sign and button is crisp pixel type even offline. Touch buttons and the joystick are square too.

Four quality levels (start screen or case). They change effects only:
- **Ultra:** everything in High, plus **pixel ray tracing**. A 3D copy of the nearby blocks lives on the GPU, and for every texture pixel (16 per block side, the same as the textures) a ray is traced to the sun for shadow, with short rays for corner shading. Sunlight falls through windows in pixel-exact patches. Needs WebGL2, and is the default on desktop.
- **High:** pixelated sun shadows, crepuscular rays, lens flare that hides when the sun is blocked, motion blur, real-time rain reflections, edge smoothing, drifting ground fog, distance haze, vignette and color grading.
- **Medium:** lighter shadows and effects, no motion blur.
- **Low:** fastest, the default on phones.

Shadows are snapped to texture pixels on every level that has them. When it rains, everything open to the sky gets wet: it darkens, and roads, roofs and car roofs reflect the scene in real time with puddles and ripples, then dry off after the rain.

Also on every level: a sky dome with sun, moon and stars; pixel textures that span 2×2 blocks so bricks, planks and tiles run continuously; swaying grass tufts; and seasonal ambience (ash and dust, fireflies, falling leaves, snow and rain that stop at roofs, embers and flies).

Performance: chunk streaming, packed vertices (16 bytes instead of 44, about 60% less GPU memory), typed-array meshing, merged furniture, frozen static meshes, only large parts casting shadows, shadow maps refreshed every few frames, and dynamic render scale that only drops if frames get slow.

## Surviving

- **A limited number of zombies:** each region starts with so many walkers (towns hold the most). Kill them and they're gone; the top bar shows how many are still out there. New ones only come from people who turn.
- **Infection:** zombies bite people who can't fight back (unarmed family members). The bitten fall sick and turn within a minute or so, and anyone the dead kill gets back up. A bandage buys them time, not a cure.
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
- **Break the decor:** hit furniture with the bat, pickaxe or chainsaw: TVs, couches, tables, fridges, shelves, school desks, hospital beds, shop aisles, stair rails, plants, ivy, weeds, saplings, beds, bunks and tents. Small things go in a hit or two, big ones take more. Wood breaks into planks, metal into scrap, upholstery into cloth. Hitting a wall pries off its trim first (baseboards, crown moulding, window and door casings). Explosions wreck furniture nearby. What you break stays broken, even after saving.
- **Pick up what you break:** blocks you dig or cut, doors you smash and explosion debris drop as small spinning items. Walk near them and they're pulled into your case, unless it's full.
- **Building and digging:** place plank, stone, dirt, metal or stair blocks (stairs face the way you're looking) and dig anything except bedrock. Build walls 3 high in stone or metal.
- **Seasons:** spring, summer, autumn and winter turn every 3 days.
  - Seasonal grass and leaves, and in winter snow on the ground, roads, roofs and trees.
  - Rain, snowfall and **thunderstorms** (most likely in summer): pixel lightning bolts, a flash, then thunder that arrives late depending on how far away the strike was. Strikes scorch blocks, start fires and hurt anyone standing close. Get under cover.
  - Winter days are shorter.
  - Cold drains your warmth unless you're indoors, by a fire, in a car or wearing a coat.
- **Families:** about 1 in 4 houses shelters a family: a father, a mother and one to three kids. They're unarmed and helpless; when zombies come they run and scream for help. Most need something (food or bandages); help them and they'll give you what they can spare and remember you. Kids can't be hurt or infected by anyone.
- **Talking to people (E / Talk):** a conversation menu. Trade with survivors, ask them to come with you (they follow and fight), wait or go home, give food or bandages, ask about the area (nearby towns, bandit camps, stocked shops), or tell a family to lock up.
- **People:** a fixed cast of named survivors and bandits with realistic names. Nobody respawns: when someone dies, they're gone for good and drop off the leaderboard. Out of sight, they keep fighting each night, and now and then one doesn't make it (you'll hear it on the radio).
  - About half the houses still have a survivor living in them. By day they forage (raid crates, hunt, pick up carcasses) and carry food back to a stash. They board up open windows and set spike traps at the door.
  - At night they go home, open the door, close it behind them and sleep. About 1 in 4 are night owls who keep scavenging.
  - They shoot zombies and trade with you. Raid a stash while its owner sees you and they turn hostile.
  - About 4 in 10 armed groups camping in the wilds are **drifters**: they carry guns but are friendly unless you attack them, and will trade or travel with you. The rest are bandit gangs of 2–4 who camp around fires and tents in the wilds and shoot on sight.
- **Leaderboard:** hold **Z** (or open your case) to see zombies killed, people killed and nights survived for you and everyone still alive. Click a column to sort. Your nights count resets when you die.
- **Attaché case (Tab):** a grid inventory like Resident Evil 4. Every item has a size (a fuel can is 2×2, a jacket 2×3, the bat 4×1) and stacks up to a limit. Drag items to arrange them, rotate them with R or right-click while dragging, or tap *Organize*. Select an item to use, wear, rotate or drop it. If you pick up more than fits, the extra drops in a bag at your feet.
- **Tents:** abandoned campsites dot the countryside, bandits camp in them, and you can sew your own (5 cloth + 3 wood). Sleep in one like a bed.
- **Respawn:** when you die, choose your bed, the crossroads or a random town. The case also has a *Respawn (stuck?)* button.
- **Bunk beds** in some bedrooms, and you can build one (12 planks + 4 cloth).
- **Chainsaw:** craft one (2 metal + 4 scrap + 1 fuel can) or find it in hardware stores. Press 1 again (or tap Tool) to swap between bat and saw, then hold attack. A few tenths of a second on an arm, leg or neck takes it off; hold it on the torso and the zombie comes apart at the waist, the top half tumbling away. It burns fuel (tops itself up from your fuel cans) and cuts through logs, planks and leaves.
- **Explosives:** throw **pipe bombs** (Q; craft from 2 scrap + 2 coal) or place **dynamite** (5-second fuse, a much bigger blast that tears through walls; craft from 3 coal + 1 cloth + 1 scrap). Hardware stores stock both. Blasts shake the screen.
- **Cooking:** at a campfire, pick a recipe: grilled meat, hot beans, roast vegetables, meat stew (food, health and warmth), bone broth (warms you right up) or smoked jerky. It simmers in a pot on the flames for a few seconds, then goes in your case. Vegetables turn up in grocery stores and kitchens.
- **Crouch (C / Ctrl / Duck):** 1 m tall and slow, enough to climb through a window once the glass is out.
- **Creative mode** (start screen, or toggle in the case): every block type, unlimited, instant digging, free explosives, no damage, hunger or cold, and zombies leave you alone. Double-tap jump to fly.
- **Beds:** sleep through the night (in co-op, both players lie down). A bed also sets your respawn point.
- **Bicycles:** left by front doors and along the roads. No fuel needed, just pedalling (which makes you hungrier); about 30 km/h, quiet, and they bounce off zombies instead of running them down. One rider only.
- **Vehicles:** sedans, pickups, vans, police cruisers, ambulances, city buses and motorcycles. They need fuel and repairs, and they collide with each other, with people and with animals (you can stand on the roofs).
  - First-person cabin at real seat height: you see your own body at the wheel and most of the road.
  - Turning steering wheel, working gauges and a **live rear-view mirror**; many vehicles have a **backup camera** screen with guide lines when reversing.
  - Or switch to the outside view.
  - Run zombies over and carry a passenger.
- Health, hunger, stamina, day/night cycle and flashlight. The light turns on by itself underground.

## Saving

The world is rebuilt from its seed, so a save only stores the seed plus, for each region you've touched, the blocks you changed (delta + varint packed), looted crates, door states, parked cars, things you built and how many zombies are left there, plus everyone's stats, then deflated. A whole game fits in a short **save code** (a few KB, even after travelling far). The game also autosaves in your browser every 90 seconds. Use **Continue**, or paste a code into **Load a save code**.

## Controls

**Player 1:** WASD move · mouse look · click act · right-click place block · 1–5 / wheel tools (bat, pistol, pickaxe, build, place) · R block material or item to place · E use / doors / loot / sleep / cook / enter car · V driver or outside view · Space jump (brake in car) · Shift sprint · C / Ctrl crouch · Q throw pipe bomb · Space ×2 fly (creative) · Tab attaché case · Z (hold) leaderboard · G eat · X bandage · T flashlight

**Player 2:** I K / J L move & turn · U / O look · H act · Y use · N jump · P sprint · B tool · M material or item · , car view · [ eat · ] bandage · \ case · ; crouch · . pipe bomb · or a gamepad

**Touch:** drag the left side to move, drag the right side to look · Act, Jump, Use, Place buttons bottom right · Bag, Tool, Type, View, Run, Duck, Bomb, Talk along the side
