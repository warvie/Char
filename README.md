# Dead Ground

A 3D zombie-apocalypse survival game that runs in the browser. Raid ruined towns, hunt in the wilds, dig into caves, build walls before nightfall, and get an old car running.







## v17.4 — no real circles

- Round meshes replaced with pixel geometry (`pxRound` stepped discs/rings extruded in whole pixels, `pxCone` stepped cones, merged into one box mesh with metre UVs): wheels, hubs, steering wheel, gauges, manholes, flames, spikes, pipe bombs.
- Sky sun/moon on an angular pixel grid with stepped glow; lens flare, halos (one texel per block pixel) and NVG eyepiece pixelated with hard edges.
- Furniture yaw squared to 90 degrees and every axis-aligned furniture box snapped to the 1/16 m grid (min 1 px); `part()` sizes/offsets snapped to whole pixels.

## v17.3 — lights in the dark

- **Dynamic lights:** 12 per-pixel lights (omni, spot, interior-box) injected into every shader; outdoor lights skip fragments under a roof (height map), interior lights stay in their building box; inverse-square falloff with smooth cut-off; wet-ground specular glints.
- **Sources:** wired lamps, campfires, street lamps after dark, vehicle head/tail/brake lights, occupied homes at night (windows glow via the glass shader), garrisoned-base floodlights, flares, muzzle flashes, explosions, lightning.
- **Post:** eye adaptation (exposure), night-vision mode; pixel halo sprites around light sources.
- **Items:** road flare (loot; lights and attracts zombies for 2 min), night-vision goggles (head slot; auto-on in the dark, uses flashlight batteries).
- **Pixel standard corrected to 16 px/m** (the block atlas is reduced in 2x2 steps): doors 16x32 and 2 px thick, signs 14 px tall, blood/grass reduced in 2x2 steps, glass layers 16 px/m, road paint sampled in 2x2 steps, 16 px tiles span 1 m, shader grids at 1/16 m.

## v17.2 — one pixel size

- Global pixel standard: 32 texels per metre on a world grid aligned with the blocks.
- A background sweep gives every opaque untextured mesh a kind texture (paint, metal, plastic, rubber, wood, fabric) and metre-based UVs: local frame for moving entities (vehicles, zombies, animals, NPCs, players, doors, bags), world-space for static objects so texels line up with blocks. 16 px tiles repeat twice a metre.
- Fitted textures resized to 32 px/m: signs (28 px faces, bitmap text, grid-snapped), car glass cracks and windshield blood, blood decals (1 m, grid-snapped), grass sprites (16x24).
- Shader grids moved from 1/16 m to 1/32 m: furniture grain, flashlight, pixel shadows, rain ripples.

## v17.1 — blocks to the horizon

- **Far view** rebuilt as blocks: per-cell top block (id, height), colours averaged from the real texture tiles, greedy-merged tops and side runs; 2-block cells to ~100 m, 4-block cells beyond; built and meshed in 2.5 ms slices. Far terrain samples are cached.
- **Doors:** 32x64 pixel-art textures (32 px/m, block density), six styles across nine variants.
- **Hotbar:** limit 12 (keys 1–9, 0, −, =); Tactical pants (10) and Utility overalls (12).

## v17 — far view

- **Far view:** a low-detail terrain mesh beyond the loaded chunks extends sight to 4x the render distance (toggle next to Render distance). It samples real blocks inside the loaded window and the generator's height function and town plans beyond it, and builds in 2.5 ms slices.
- **Flashlight** lights blocks (the block shader now has the beam) and every Lambert material in the scene.
- **Road paint** is rasterised at 16 px per block into deduplicated tiles in a paint atlas; the block shader draws it on road tops. No paint geometry.
- **Grass** bends away from players, their trail, nearby zombies/animals/people and moving cars (vertex shader, 10 pushers).
- **Window trim** isn't drawn on chipped/rubble blocks.
- **Inventory:** Close button top right; tap outside to close (also trade/campfire panels).
- **Performance:** ray-trace volume shifts instead of full rescans (and rescans only edited columns); HUD writes only on change; flashlight rays cut by a third.
- **Memory:** chunk/glass/grass/furniture/far-view geometry releases its CPU copy after GPU upload; per-region generation scratch is dropped after generation.
- **QoL:** auto-pickup of loot bags (menu setting), pickup pop-ups, hit/kill crosshair markers, compass strip (waypoint, nearest base, death spot), map marks bases and death spot.
- **Fix:** soldiers are saved and loaded correctly.

## v16 — the compounds

- **Military bases:** walled corporate compounds in the wilds (watchtowers, HQ, barracks, armory, helipad, trucks) with military-grade loot. Garrisoned ones warn you off and shoot anyone inside the wall; overrun ones are full of zombies.
- **NPCs:** survivors drive cars (Use on their car drags them out), raid empty houses, and path around walls, cars and furniture, opening doors as they go. Bandit gangs build log palisades round their camps.
- **Cars:** Q / Bomb in a car toggles the wipers, which clear blood from the windshield. Every window cracks where it's hit: bullets, bat swings, side and rear impacts.
- **Porches** sit on the block texture-pixel grid.
- **Creative:** pick the weather in the menu.
- **Developer mode:** F2 heal · F3 +3 h · F4 weather · F6 spawn zombie · F7 clear zombies · F8 teleport to crosshair · F9 god mode · F10 freeze time, plus menu buttons (go to base, spawn car/survivor, perf overlay, copy debug info) and a richer readout.

## Play

Open `index.html` in a modern browser (Chrome, Edge, Firefox, Safari). It needs an internet connection the first time to load Three.js from cdnjs.

To play from a link, turn on GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**. The game will be at `https://warvie.github.io/char/`.

## The world

- **An endless world** built from half-metre pixel-textured blocks, with quarter-height grass caps that smooth hills and slopes. It's split into 112 m regions, generated from the **seed** whenever you get near them, so the same seed always builds the same world and you can walk in any direction forever. A big town sits at the start; about 3 in 4 regions elsewhere have a small town (sometimes two), with rolling hills, forests and caves between.
- **Compression, in three tiers:**
  - The 3 × 3 regions around you (336 m square) are raw blocks in a ring buffer: what you can see and touch. Walk far enough and the window slides; nothing ever moves in memory except the region coming in.
  - Regions you just left are compressed in memory. Every cell is compared with the bare terrain the seed would grow there (heights, layers, even ore positions, which come from a hash), so only buildings, caves, trees and your changes survive. An LZ4-style pass then squeezes that, from 3.4 MB to about 100 KB per region (about 33×), losslessly. Coming back is instant.
  - Everything else is stored as nothing but the seed plus your edits. It is rebuilt exactly when you return.
- **No hitches at region borders:** crossing into a new 112 m region swaps regions one at a time over several frames instead of all at once. Each region keeps its terrain heights cached, and regions you didn't change aren't re-compressed when you leave.
- **Chunk streaming:** only the 8 × 8 m chunks around the players are meshed; the rest load in as you move and unload behind you. Pick a render distance from 32 to 80 m. Fog and camera range follow it.
- **Realistic towns:** 6 m two-lane roads, 1.5 m sidewalks, 15 m lots, and houses 11–15 m across (level with the sidewalks) with 3 m storeys (2.5 m ceilings), 1–3 storeys, painted drywall in a different colour per room with baseboards and crown moulding, switchback staircases with landings (two steps per block) and wooden or iron railings, framed windows (some smashed or boarded), front and back doors, stairs and roof access.
- **Land:** rolling hills, mountain ranges (ridged peaks of bare stone, far from towns), winding rivers and ponds you can swim in, boulders and scattered pebbles, and dirt off-road trails wandering through the wilds.
- **Roads between towns** leave each town straight out of one of its streets at the full 6 m street width, level with it, then narrow to a 4 m country road that curves and wiggles across the land, cut and filled to an even grade, with yellow centre dashes. Where they cross water or a deep dip they become bridges: an asphalt deck on concrete, with parapets and piers. Road paint only sits on solid road, and disappears where the road is dug out.
- **Town houses** sit back from the street in their own yards: swimming pools with loungers, vegetable patches, hedges, back-yard trees and side driveways (often with the family car). City buildings still fill their lots.
- **Town names:** every town is named ("Millfield", "City of Ashbrook"…), with green entrance signs showing the population, and the names appear on the map. Country roads have white edge lines as well as yellow centre dashes; rivers and ponds have reeds, cattails and lily pads.
- **Settlements of every size:** single-block hamlets at lonely crossroads, ordinary towns, and big cities (about 1 region in 10) with 3–6 storey buildings, a mall and far more abandoned traffic.
  - **Gas stations:** a lit canopy over two pump islands (Use a pump to siphon the last of its fuel), a price-sign pole, and a little shop with a till, coolers, shelves and fuel cans in the back.
  - **Parks:** grass, gravel paths, a stone fountain, park benches, a swing set, a slide, picnic tables, lamp posts and old trees.
  - **Malls:** a tall hall under a skylight, a row of shops (clothes, snacks, tools) with glass fronts and their own signs, a food court and benches.
  - **Airports** out on the flats: a marked runway, taxiway and apron, a glass terminal with check-in desks and gate seating, a control tower with a ladder up to the glass cab, a hangar with a light plane, airliners at the gates and a burned-out wreck on the runway. Now and then an airliner crosses the sky overhead with its long roar.
- **City blocks of different sizes:** in cities, some neighbouring blocks merge into superblocks with 6–10 storey office towers (glass curtain walls, a lobby, open-plan floors of desks). Cities also have a **college**.
- **Kitchens** are set for dinner: plates, bowls, cups, glasses, forks and knives, and stacks of dishes and mugs on the counters. **Bathroom mirrors** show a live reflection of you and the room.
- **Sky and sound:** chunky pixel clouds (always visible overhead whatever the render distance) drift with the wind (grey in storms), flocks of birds cross the sky by day, and the wind carries far-off moans, groaning metal, banging doors, howling dogs and whistling through broken windows. More often at night.
- **Roads on hills:** country roads climb and dip with the land in quarter-metre steps rather than half-metre ledges.
- **Lights:** every room has a wall switch for its ceiling light (Use to flip it). Craft wire, lamps and switches and lay your own: wire pieces join when side by side, and a switch turns on every lamp its wire reaches.
- **Public buildings:** each town has some of these, under faded signs over the doors.
  - **Hospitals** (2–3 storeys): reception, waiting chairs, wards with hospital beds and IV stands, medicine cabinets and a pharmacy full of bandages.
  - **Grocery stores:** a plate-glass storefront, stocked aisles, checkouts, drinks coolers and a stockroom. Mostly food.
  - **Hardware stores:** tool aisles, lumber racks and pegboard walls. Scrap, metal, planks, fuel, repair kits and traps.
  - **Schools** (2 storeys): classrooms with chalkboards and rows of desks, lockers along the corridors and a cafeteria.
- **Battle damage:** most buildings came through intact, with whole windows. About 3 in 10 took real damage, and those are mostly chipped rather than holed. Walls and roofs have chunks bitten out of blocks, with the broken pieces lying in rubble piles below. Only a few blocks are knocked clean through, and roofs have ragged holes with debris on the floor underneath. 
- **Every block breaks in stages:** dirt, grass, stone, ore, concrete, brick, drywall, roof, asphalt, planks, logs, metal, tile and window frames all go through three broken stages (chipped, heavily damaged, crumbled stub) before they give way. That happens under your pickaxe, zombie claws and explosions, and the broken pieces land as rubble. A block that is already damaged breaks faster.
- **Doors** sit on a proper floor threshold (planks or tile), and get the same treatment: the jambs and head are the surrounding wall, with side casings, plinth blocks and a head casing of trim on both faces.
- **Windows** sit in ordinary wall (brick or concrete outside, painted drywall inside) with a proper casing of trim round the opening on both faces: side and head casings, a deeper sill and an apron under it.
- **Blood that coats things:** every droplet falls, and where it lands it leaves a stain on the face it hit, one texture-pixel square (6 cm) at a time. That covers tops of blocks, walls, ceilings and the sides of things, and it runs down over edges. Your bat and chainsaw get bloodier with every hit, and cars that run zombies down get stained across the body.
- **Blood:** pixel-art splatters with flung droplets where things die, spatter on nearby walls, and old dark pools in the streets where people fell months ago. No more red-tinted blocks.
- **Overgrowth:** about 1 in 5 houses (more of the damaged ones) is being taken back by nature: ivy climbing the outside walls and in through open windows, trailing down inside, weeds across the floors, and sometimes a sapling breaking through the boards.
- **Trees** have thin branches and twigs (14 cm and 8 cm thick) reaching off the trunk, ending in leaf clusters, or bare on dead trees. Curved bend pieces join every turn, so a limb can rise, dip or swing sideways and still reads as one unbroken branch from the trunk to its tip.
- **Windows stay clear:** nothing taller than half a metre is placed in front of a window (it goes elsewhere in the room), and ivy never fills a window or hangs over the glass.
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

- **One pixel size everywhere:** every texture — blocks, vehicles and their parts, furniture, tents, grass, paintings — is drawn at 16 pixels per metre, so nothing looks stretched. (Shop signs are the one exception: their lettering is drawn at sign resolution.)
- **Zombies differ at a glance:** heights from short to tall, thin to heavy builds, and outfits from tees, hoodies, flannel and overalls to suits, dresses, hospital gowns and police uniforms, with jeans, slacks or shorts, different shoes, and hair from bald and buzzed to long, ponytails, mohawks and patchy, plus beards.
- **Tents** are pixel-built: a stepped ridge, a door flap, a rainfly with guy lines and stakes, and gear inside.
- **Rain ripples:** wet ground and puddles ripple with rings spreading out from falling drops (each landing at its own moment) and a slow wind swell, drawn on the same pixel grid as everything else. The ripples bend the ray-traced reflections, so street lights and buildings wobble and smear in the puddles.
- **Flashlight:** a perfect circle of light, ray-traced against the blocks each frame and painted in chunky pixel steps, so walls cut it off with crisp shadows
- **Metal sheen:** signs, posts, pumps, lamps and car bodies carry a soft, blurry sky reflection that follows the time of day
- **Red blood:** blood particles are bright red and ignore fog, so they never turn black
- **Rain you can place:** the rain's volume follows the distance from your head to the nearest surface it's landing on (sampled in rings out to 15 m), so it's loud in the open, softer and muffled when there's a roof over you, quieter deep inside big buildings and silent underground.
- **3D sound:** every sound in the world is placed where it happens. Volume falls off with distance, distant sounds lose their high end and pick up more echo, sounds pan as you turn your head, and sounds behind you are muffled. Zombie groans and their shuffling feet, doors, breaking glass, bandit gunfire, explosions, car alarms, campfire crackle and birds all come from their source; the eerie ambience comes from somewhere off in the dark.
- **Sound** is all synthesized but modelled on the real thing: footsteps that change with the ground, a gunshot crack with room echo, an engine whose note follows its revs, rolling thunder, rain and gusting wind, and the roar of passing airliners.
- **Update log:** the start screen lists what changed in each update.

**Pixel size** (start screen or case): the 3D view renders at full resolution by default (*Smooth*), with no pixelated upscaling. Pick ×2, ×3 or ×4 for a chunky retro look, where the view is drawn at a fraction of the resolution and blown up with hard pixel edges.

**60 fps governor:** on the higher graphics settings, a governor watches frame time. If frames take longer than 16.7 ms it steps down one rung at a time: fewer sun-ray and reflection samples, then motion blur, then shorter ray-traced shadow rays and no ray-traced AO, then render scale. When there's headroom it steps back up. On 60 Hz screens it probes one rung up after a calm stretch, since those screens never show spare time.

**Buried blocks are skipped:** about 89% of solid blocks are completely boxed in. The mesh builder now skips them per column, starting just below the lowest see-through cell in each column and its neighbours. It produces exactly the same meshes about 27% faster (466 → 342 ms per region in tests). I also tested not deciding hidden blocks at all during generation: ore rolls for buried cells cost about 4 ms per region, so it isn't worth complicating saves for.

**8 × 8 pixels per block:** every block face shows an 8 × 8 texture (point-sampled so mortar lines and board joints stay crisp).

**Ground that blends:** where grass meets bare dirt, the two fade into each other over about two blocks on each side. The fade is dithered one texture pixel at a time in clumpy noise, so there is no hard line between them and it stays pixelated.

**Meadows:** grassy ground grows daisies, poppies, dandelions, bluebells, lavender and clover, mostly in patches of one kind, with stray flowers elsewhere. They dry to seed heads in autumn. Grass shifts across lush, yellow-green, blue-green, olive and pale patches, and the blades cast pixel shadows that sway with them.

**Trees** come in three sizes. Young ones have a 25 cm stem and a small crown. Normal ones have a log trunk and limbs that taper from thick to thin. Old ones have a 1 m trunk of 2 × 2 logs, flared roots, a big crown, and heavy 25 cm limbs that taper to branches, then twigs.

**Pixel shadows everywhere:** every shadow (on blocks, furniture, grass, people and cars) is looked up on the same 1/16 m texture-pixel grid, so all shadow edges are pixelated.

**Rain:** wet, sky-exposed ground turns into a pixelated mirror. Reflections, ripples and glints are snapped to the texture-pixel grid, and anything under a roof stays dry.

**Realism:** the block textures got a pass for depth: bevelled bricks with burnt and pale ones mixed in, soot and grime, concrete pores and stains, wood grain and knots, rust running from rivets, shingle rows, leaf clusters and mottling everywhere, at the same pixel count. On High and Ultra the image gets **ambient occlusion** from the depth buffer (corners, creases and contact shadows) and a soft **glow** around bright light. Every level gets a **filmic tone curve**.

**Pause menu (Esc):** resume, *Respawn (unstuck)*, *Main menu* (saves, then back to the title screen to Continue or start another mode), or **teleport** to your bed, the crossroads, the nearest town, a random town or your co-op partner.

**Unstuck:** a *Respawn* button is always on screen (and the ` key; = for player 2; *Unstuck* on phones). It puts you back at your respawn point with everything you're carrying, for when you glitch into something.

**No overlapping UI:** the HUD is laid out (and checked by script) for desktop, laptop, split-screen, phones in portrait and landscape, and tablets, so nothing sits on top of anything else.

**Small phones:** on screens smaller than a typical phone, the whole touch layout (buttons, stick, hotbar and HUD) shrinks in proportion, so no button overlaps another in portrait or landscape. This is checked on 18 phone and tablet sizes.

**Touch buttons:** the right edge has *Crawl* in the bottom corner, *Jump* the same size above it, and *Run* above that. The red action button (*Swing*, *Shoot*, *Dig*, *Build*, *Set trap*, *Eat*, *Punch*…) sits beside *Crawl*, with *Use* and the second-function button stacked above it. *Bag* sits at the end of the hotbar, and you tap a hotbar slot to switch to it. Each button has its own colour and pixel icon.

**Crawl:** double-tap C (or tap *Crawl*) to go flat on your belly. You're 45 cm tall, slow, and fit through half-metre gaps. You only stand back up when there's room.

**Hotbar (Minecraft-style):** six slots, each holding anything you carry: the bat or chainsaw, pistol, pickaxe, any building block, any trap or placeable, food, bandages, pipe bombs, or nothing (bare hands). In the case, select an item and click a slot (or press 1–6) to put it there. Clicking a slot with nothing selected clears it. R on a block or trap slot changes what's in that slot. The layout is saved with your game.

**Never stuck in blocks:** waking up, respawning, teleporting and getting out of a car always put you in the nearest free spot with a floor under you. If a block ever ends up inside you (placed, loaded or fallen in), you duck if that frees you, otherwise you're moved out within a quarter second.

**Emotes and dances** (J, or *Emote* on phones): Wave, Cheer, Point, Thumbs up, Facepalm, Laugh, Salute, Sit, plus looping dances (Groove, Robot, Disco, Headbang, Spin, Shuffle). Pick one with its number key or a click. The camera swings round so you can watch, and moving cancels it. Other players see your emotes.

**Creative palette:** in creative mode, R (or *Pick* on phones) opens a palette with every block, all 8 vehicles, zombies, deer, rabbits, wolves, boars, survivors, bandits, friendly drifters, parents and children, traps, beds, tents, campfires, crates, all furniture, and street signs and traffic lights. Pick one, then place it with the Build tool (4). Placed furniture is saved with the world.

**Main menu button:** *Main menu* sits under *Respawn* on desktop, and there's a *Menu* button on phones. Both save, then take you to the start screen.

## Online

When the game is opened in Claude (the published artifact), the start screen's **Online & profile** panel signs you in with your Claude account.

- **Username:** claim a name (3–16 letters, numbers or _). Each name can belong to only one account: it's reserved in a shared list under a short lock, so two people can't grab it at once. Other players' names show a ✓ when they really own them.
- **Profile picture:** draw a 16 × 16 picture in a 16-colour palette, or squeeze a photo down to one. It's run-length packed and base64-encoded, usually 40–180 characters.
- **Playing together:** everyone in the same world seed shares a live room. The players list shows who's online and who's in a world, with a *Join* button that loads their seed. In a world you see each other walking, crouching, driving, sleeping and dancing, with name tags and pictures. Block edits and explosions are synced, and the top bar counts players online. Each player's state is one presence update of about 140 bytes (position, look, tool, flags, emote, health, plus the last 48 block edits).
- **Who can join:** only people the game artifact is shared with, signed in to Claude. To reserve a username they need Contributor or Editor access; view-only players can still play together under an unreserved name. Zombies, animals and loot are simulated on each device, so they won't be in identical places for everyone.
- **Phone numbers:** not used. Sign-in comes from the player's Claude account, so the game never collects phone numbers or passwords.

Outside Claude (for example, this repo opened as a plain file), the game still works offline, and your name and picture are saved in that browser.

**Rotating your phone:** the picture is resized to the new screen shape every frame and again just after a rotation, so turning between portrait and landscape never leaves the view stretched or squashed.

**All-pixel UI:** a pixel font is built into the game (hand-drawn 5×7 glyphs turned into a real font at startup), so every label, menu, sign and button is crisp pixel type even offline. Touch buttons and the joystick are square too.

Four quality levels (start screen or case). They change effects only:
- **Ultra:** everything in High, plus **pixel ray tracing**. A 3D copy of the nearby blocks lives on the GPU, and for every texture pixel (16 per block side, the same as the textures) a ray is traced to the sun for shadow, with short rays for corner shading. Sunlight falls through windows in pixel-exact patches. Needs WebGL2, and is the default on desktop.
- **High:** pixelated sun shadows, crepuscular rays, lens flare that hides when the sun is blocked, motion blur, real-time rain reflections, edge smoothing, drifting ground fog, distance haze, vignette and color grading.
- **Medium:** lighter shadows and effects, no motion blur.
- **Low:** fastest, the default on phones.

Shadows are snapped to texture pixels on every level that has them. When it rains, everything open to the sky gets wet: it darkens, and roads, roofs and car roofs reflect the scene in real time with puddles and ripples, then dry off after the rain.

Also on every level: a sky dome with sun, moon and stars; pixel textures that span 2×2 blocks so bricks, planks and tiles run continuously; swaying grass tufts; and seasonal ambience (ash and dust, fireflies, falling leaves, snow and rain that stop at roofs, embers and flies).

Performance: chunk streaming, packed vertices (16 bytes instead of 44, about 60% less GPU memory), typed-array meshing, merged furniture, frozen static meshes, only large parts casting shadows, shadow maps refreshed every few frames, and dynamic render scale that only drops if frames get slow.

## Pockets, backpacks and how you died

- **Pockets are your hotbar:** the pants you wear decide how many hotbar slots you get — shorts 2, slacks 3, jeans 4, riot pants 4, cargo pants 8. You start with random pants.
- **Creative mode** can sleep any time and anywhere; the menu has a *Sleep until morning* button that skips to dawn.
- **Creative mode** has a bottomless case: 14 wide, it grows by rows as you pick things up and shrinks back when you empty it.
- **Backpacks are your case:** no pack gives an 8 × 5 case; a school backpack 10 × 6; a hiking pack 12 × 8; a military rucksack 14 × 9. Schools are full of backpacks. Sew one from cloth, then upgrade the one you're wearing in the crafting list. Every recipe shows pictures of what it makes and needs.
- **Death:** when you die, the game says how (eaten, shot by a named bandit, run over, starved, frozen, blown up…), to you, the other split-screen player and everyone online.
- **Cigarettes** bring your stamina back at a small cost to health. **Marijuana** slows and softens everything for a while, eases pain a little, and makes you very hungry.

## Vehicles, crashes and the map

- **Blood** splashes onto the windshield and the exact front panels that hit a zombie, and streaks back along the hood.
- **Visible damage:** dents push panels back and bend them, scuffs show bare metal and rust, the windshield cracks in spider-webs, and hard hits tear off bumpers and lights, which stay lying in the road. Abandoned wrecks already show their damage.
- **Damage where you're hit:** front-end hits take out the headlights first, then crack the radiator and wreck the engine (a sick engine is slower, smokes and stalls; a dead one must be replaced), and hard hits crush the battery. Rear-end hits split the fuel tank, which then leaks. Side hits bend wheels. The windshield only cracks when something actually strikes the glass: a wall tall enough to reach it, a taller vehicle, or a zombie thrown onto it at speed. A repair kit fixes the radiator, tank, battery and lights.
- **Crashing through things:** hit a wall fast enough and glass, drywall, planks and doors give way, and at higher speed brick and concrete too. Furniture in the way goes flying.
- **Construction machines:** bulldozers push slowly through anything; excavators dig a bucket of ground in front of them when you hold attack; dump trucks are fast and heavy.
- **Self-driving cars** (the rare Volta S): press M (or Map in the pause menu) and click anywhere. The car steers itself there, keeping to paved roads and backing out of dead ends. Touching the controls takes over.
- **Driver view:** mostly windshield, with the top of the dash and a sliver of hood.
- **Creative mode:** using a vehicle repairs and refuels it, and it never runs dry.

## Realism

- **Thirst:** a water bar beside food. Bottled water and soda are in stores and gas stations. Use at a river or pond to drink (risky) or fill an empty bottle; boil dirty water at a campfire; stand in the rain with empty bottles and they fill with clean water. Dehydration kills.
- **Injuries:** zombie bites, animal attacks and gunshots can make you bleed (you drip blood and lose health until you bandage it), hurt an arm (weaker swings, shakier aim) or hurt a leg (a limp, no sprinting). Wounds left unbandaged too long can get infected: a fever that slowly drains you until you take antibiotics. Splints make limbs heal four times faster. A status line under the bars shows BLEEDING, INFECTED, HURT LEG and so on.
- **Fatigue:** you need to sleep about once a day. Exhausted, your view blurs, your aim shakes, stamina drains and eventually you black out for a moment.
- **Sickness:** bad water or raw meat can make you sick: retching, lost stamina and faster hunger.
- **Noise:** gunshots carry about 90 m; explosions 120 m; breaking glass, running engines, car alarms and lit windows at night all draw zombies to the source.
- **Weapon wear:** the bat loses condition with every hit and finally splinters (repair it with a plank and scrap). The pistol holds 12 rounds; reload with R (or it reloads itself when empty), and now and then it jams and needs clearing.
- **Food spoils:** fresh meat, cooked meat, vegetables and stews partly rot overnight. Canned food keeps.
- **Darkness:** nights are truly dark, with a moon that waxes and wanes over eight days. Your flashlight (T) is the only light you carry, and it runs on batteries.
- **Weather:** rain soaks you, and wet clothes make you colder until you dry off by a fire. Snow slows you down and shows your footprints. Fog shrinks how far you can see to a few metres.
- **Decay:** each day weeds creep further onto the roads, and abandoned cars rust and their tyres go flat.
- **Cars:** about 3 in 10 parked cars have an alarm that wails when bumped or stripped, calling every zombie nearby. Rubble and spike traps blow out tyres (slower, pulls to one side; fit a spare wheel). Leave the headlights on at night and the battery goes flat (fit a car battery).

## Developer mode

Turn it on from the start screen or the in-game menu. A panel at the top shows what's under the crosshair: a block (name, id, coordinates, chipped or not), a zombie (outfit, health, chasing or wandering, which body part), an animal, a person, a vehicle (health, fuel, engine/battery/tank/lights condition, flat tyres) or furniture, plus your position, cell, region, the town you're in, frame rate and zombie count.

## Fishing

Craft a fishing rod (2 planks, 1 cloth, 1 scrap) or find one in a hardware store. Put it in a pocket, stand at the edge of a river or pond facing the water and Use to cast. The bobber floats where it lands. When it dips (you'll hear a splash), Use again within a couple of seconds to reel in: usually a bass, trout or catfish, sometimes junk. Grill fish at a campfire; raw fish is risky, and both spoil overnight.

## Combat feel

- **Knockback:** a bat hit throws a zombie back about 2 m with a small hop and a short stagger, so it can't walk straight back in; a pistol round shoves it about half a metre. Animals and people are knocked back too (big animals less).
- **Reach, not overlap:** anything attacking you walks up to arm's length (about 0.8 m) and swings from there, never into your body.
- **Bodies collide:** zombies, animals, survivors and players push each other apart instead of passing through, without being pushed into walls. Players are heavy, so a crowd jostles you rather than shoving you around, but you can't walk through a horde.

## Surviving

- **A limited number of zombies:** each region starts with so many walkers (towns hold the most). Kill them and they're gone; the top bar shows how many are still out there. New ones only come from people who turn.
- **Infection:** zombies bite people who can't fight back (unarmed family members). The bitten fall sick and turn within a minute or so, and anyone the dead kill gets back up. A bandage buys them time, not a cure.
- **Streets:** roads have double yellow centre lines, white edge lines, zebra crosswalks with stop bars, and stone curbs with red or yellow painted ends. Big towns have traffic lights on mast arms (with walk signals and street-name signs), and smaller towns have four-way stops. Speed limit, no parking, one way and yield signs line the streets.
- **Houses:**
  - **Stairs:** they stop at the top floor, so no house has an open stairway onto the roof.
  - **Outside:** a parapet around the roof, a brick chimney, roof vents and AC units, a porch with a canopy, step, doormat and light, a mailbox, and sometimes a picket fence across the front yard.
  - **Inside:** curtains at most windows, a light in every ceiling, paintings on the walls (landscapes, sunsets, abstracts, portraits, flowers), and candles and lava lamps on tables, nightstands and dressers.
- **Stores you can loot:** grocery aisles and drinks coolers hold canned food, vegetables, jerky and more. *Use* takes some off the shelf, and each shelf visibly empties over three takes (saved with the world). Hardware aisles give scrap, planks, fuel and the odd repair kit. All furniture has a pixel grain at the same texel size as blocks.
- **Manholes:** three in four are covered by a round lid sitting in an iron collar, so the opening is round. *Use* drags the lid aside.
- **Zombies** are slow by day and fast at night. They notice you only within range (22 m by day, 34 m at night) and in line of sight, give up once you're well out of range, and come to investigate gunshots. They break blocks hit by hit: a window in one hit, a wooden door in about 10 s, a brick wall only with a crowd. Metal holds longest. Some wear hard hats, helmets, vests or jackets that soak up damage.
- **Zombie looks:** rotting pixel skin with veins, mottling and open sores, torn and blood-soaked clothes, bared teeth, and sometimes a torn cheek or bare skull. Some show ribs through a hole in the shirt or a spine down the back, or have bones snapped through a forearm or shin. Some have already lost an arm, both arms, a leg or half a forearm, with a bloody stump and bone.
- **Running zombies down:** a slow bump shoves a zombie. Hit one at speed and it's thrown through the air, limbs flailing, bounces, then flops and twitches on the ground. Impact damage grows with speed, and harder hits tear limbs off, snap them in half (the lower half flies off), take the head, or cut the zombie in two. Survivors get back up, or crawl if they lost a leg.
- **Car parts:** hit a parked car with the pickaxe to pry off its wheels, engine, battery and radio (plus scrap), until it's a stripped shell. With a wrench (2 scrap + 1 metal plate, or from hardware stores), *Use* fits a missing part from your case, so you can swap parts between cars. A car missing wheels, its engine or its battery won't go.
- **Dashboard:** every car has RPM, speed and fuel gauges and warning lights on a bezel standing proud of the dash. They used to sit just behind the dash face, which hid them. The RPM needle idles, climbs with throttle and drops through gears.
- **Vehicle textures:** every part of every vehicle has a 16 × 16 pixel texture chosen by what it is (paint with rust and scratches, tyre tread, brushed metal, seat fabric, dash plastic). Textures are point-sampled and scaled so the pixels are the same size as on blocks.
- **Car radio:** press R in a car (or tap *Radio*) to cycle the stations: KDRG oldies (chords, walking bass, brushed drums and a melody), WRCK rock (overdriven power chords, kick and snare), an emergency broadcast, and off. It plays through a small speaker chain (compressor, cabin reverb, band-limited speaker) and goes quiet the moment you get out.
- **Windshield blood:** zombies you hit splatter the windshield with drops, spatters and streaks that run down the glass, visible from the driver's seat and outside. It dries off over a minute or so, and faster in the rain.
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
- **Scrip:** hand-stamped trade tokens, the new currency. Find it in crates, on dead zombies and people, and from grateful families. Survivors and drifters each run a little shop: **buy** from their stock or **sell** them your goods (they pay about 60% of value and charge about 130%).
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
