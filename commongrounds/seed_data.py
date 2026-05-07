"""
Seed script for Common Grounds project.

Run with:
    python manage.py shell < seed_data.py

This will populate:
- Roles (6 roles for the Profile model)
- Sample users (with profiles + roles assigned)
- Bookclub: Genres + Books
- Merchstore: ProductTypes + Products
- Localevents: EventTypes + Events
- DIY Projects: ProjectCategories + Projects
- Commissions: CommissionTypes + Commissions + Jobs

Idempotent — safe to run multiple times. Uses get_or_create everywhere.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from accounts.models import Profile, Role
from bookclub.models import Genre, Book
from merchstore.models import ProductType, Product
from localevents.models import EventType, Event
from diyprojects.models import ProjectCategory, Project
from commissions.models import CommissionType, Commission, Job


print("=" * 60)
print("SEEDING COMMON GROUNDS")
print("=" * 60)


# ============================================================
# 1. ROLES
# ============================================================
print("\n[1/7] Creating Roles...")

ROLE_NAMES = [
    "Reader",
    "Market Seller",
    "Event Organizer",
    "Book Contributor",
    "Project Creator",
    "Commission Maker",
]

roles = {}
for name in ROLE_NAMES:
    role, _ = Role.objects.get_or_create(name=name)
    roles[name] = role
print(f"  -> {len(roles)} roles ready")


# ============================================================
# 2. SAMPLE USERS + PROFILES
# ============================================================
print("\n[2/7] Creating Users + Profiles...")

USERS_DATA = [
    {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "displayName": "Alice Reader",
        "roles": ["Reader"],
    },
    {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123",
        "displayName": "Bob Seller",
        "roles": ["Reader", "Market Seller"],
    },
    {
        "username": "carol",
        "email": "carol@example.com",
        "password": "password123",
        "displayName": "Carol Organizer",
        "roles": ["Reader", "Event Organizer"],
    },
    {
        "username": "dave",
        "email": "dave@example.com",
        "password": "password123",
        "displayName": "Dave Contributor",
        "roles": ["Reader", "Book Contributor"],
    },
    {
        "username": "eve",
        "email": "eve@example.com",
        "password": "password123",
        "displayName": "Eve Maker",
        "roles": ["Reader", "Project Creator", "Commission Maker"],
    },
    {
        "username": "frank",
        "email": "frank@example.com",
        "password": "password123",
        "displayName": "Frank Everything",
        "roles": ROLE_NAMES,  # all roles
    },
]

profiles = {}
for u in USERS_DATA:
    user, created = User.objects.get_or_create(
        username=u["username"],
        defaults={"email": u["email"]},
    )
    if created:
        user.set_password(u["password"])
        user.save()

    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "displayName": u["displayName"],
            "emailAddress": u["email"],
        },
    )
    # Assign roles
    profile.roles.set([roles[r] for r in u["roles"]])
    profiles[u["username"]] = profile

print(f"  -> {len(profiles)} users created (password for all: 'password123')")


# ============================================================
# 3. BOOKCLUB: Genres + Books
# ============================================================
print("\n[3/7] Creating Genres + Books...")

GENRES_DATA = [
    ("Fantasy", "Magical worlds, mythical creatures, and epic quests."),
    ("Science Fiction", "Futuristic concepts, space exploration, advanced technology."),
    ("Mystery", "Suspenseful stories of crime, detection, and hidden truths."),
    ("Romance", "Stories centered on love and relationships."),
    ("Historical Fiction", "Fictional stories set in real historical periods."),
    ("Horror", "Tales designed to frighten and unsettle."),
    ("Non-fiction", "Factual works including biographies and essays."),
    ("Young Adult", "Coming-of-age stories aimed at teen readers."),
]

genres = {}
for name, desc in GENRES_DATA:
    g, _ = Genre.objects.get_or_create(name=name, defaults={"description": desc})
    genres[name] = g

BOOKS_DATA = [
    ("The Name of the Wind", "Fantasy", "Patrick Rothfuss",
     "A gifted young man tells the story of his life at the famed University.", 2007, True, "dave"),
    ("Project Hail Mary", "Science Fiction", "Andy Weir",
     "A lone astronaut must save humanity but cannot remember his mission.", 2021, True, "dave"),
    ("The Silent Patient", "Mystery", "Alex Michaelides",
     "A woman shoots her husband and never speaks another word.", 2019, True, "frank"),
    ("Beach Read", "Romance", "Emily Henry",
     "Two rival writers swap genres for the summer.", 2020, True, "dave"),
    ("The Book Thief", "Historical Fiction", "Markus Zusak",
     "Narrated by Death, a young girl in Nazi Germany steals books.", 2005, False, "frank"),
    ("The Haunting of Hill House", "Horror", "Shirley Jackson",
     "Four seekers investigate a notoriously haunted house.", 1959, True, "dave"),
    ("Educated", "Non-fiction", "Tara Westover",
     "A memoir about escaping a survivalist family to earn a PhD at Cambridge.", 2018, True, "frank"),
    ("The Hunger Games", "Young Adult", "Suzanne Collins",
     "A young woman volunteers for a televised fight to the death.", 2008, True, "dave"),
    ("Mistborn: The Final Empire", "Fantasy", "Brandon Sanderson",
     "A street urchin discovers magical powers and joins a heist crew.", 2006, True, "frank"),
    ("Dune", "Science Fiction", "Frank Herbert",
     "On a desert planet, a young noble navigates intrigue and destiny.", 1965, False, "dave"),
]

book_count = 0
for title, genre_name, author, synopsis, year, available, contributor_username in BOOKS_DATA:
    _, created = Book.objects.get_or_create(
        title=title,
        defaults={
            "genre": genres[genre_name],
            "author": author,
            "synopsis": synopsis,
            "publication_year": year,
            "available_to_borrow": available,
            "contributor": profiles[contributor_username],
        },
    )
    if created:
        book_count += 1

print(f"  -> {len(genres)} genres, {Book.objects.count()} books ({book_count} new)")


# ============================================================
# 4. MERCHSTORE: ProductTypes + Products
# ============================================================
print("\n[4/7] Creating ProductTypes + Products...")

PRODUCT_TYPES_DATA = [
    ("Apparel", "T-shirts, hoodies, and other clothing items."),
    ("Accessories", "Bags, hats, jewelry, and small wearables."),
    ("Stationery", "Notebooks, pens, stickers, and paper goods."),
    ("Home Goods", "Mugs, posters, candles, and decor items."),
    ("Books & Zines", "Independent publications, zines, and printed material."),
]

product_types = {}
for name, desc in PRODUCT_TYPES_DATA:
    pt, _ = ProductType.objects.get_or_create(name=name, defaults={"description": desc})
    product_types[name] = pt

PRODUCTS_DATA = [
    ("Common Grounds Tee", "Apparel", "Soft cotton tee with the CG logo.", "499.00", 25, "Available", "bob"),
    ("Hoodie - Earth Tones", "Apparel", "Cozy fleece-lined hoodie in cream and brown.", "1299.00", 12, "Available", "bob"),
    ("Canvas Tote Bag", "Accessories", "Durable cotton tote, perfect for groceries or books.", "299.00", 40, "On sale", "frank"),
    ("Enamel Pin Set", "Accessories", "Set of 3 enamel pins with hobby-themed designs.", "199.00", 0, "Out of stock", "bob"),
    ("Hardcover Notebook", "Stationery", "A5 lined notebook with elastic closure, 240 pages.", "349.00", 30, "Available", "frank"),
    ("Sticker Pack", "Stationery", "12 vinyl stickers featuring app icons and quotes.", "99.00", 100, "On sale", "bob"),
    ("Ceramic Mug", "Home Goods", "11oz mug with subtle CG branding.", "249.00", 20, "Available", "frank"),
    ("Wall Poster A2", "Home Goods", "Minimalist art print, A2 size, matte finish.", "399.00", 15, "Available", "bob"),
    ("Zine Issue #1", "Books & Zines", "First issue of the community zine, 32 pages.", "149.00", 50, "Available", "frank"),
    ("Recipe Book", "Books & Zines", "Reader-submitted recipes from the community.", "599.00", 8, "Available", "bob"),
]

product_count = 0
for name, type_name, desc, price, stock, status, owner_username in PRODUCTS_DATA:
    _, created = Product.objects.get_or_create(
        name=name,
        defaults={
            "product_type": product_types[type_name],
            "description": desc,
            "price": Decimal(price),
            "stock": stock,
            "status": status,
            "owner": profiles[owner_username],
        },
    )
    if created:
        product_count += 1

print(f"  -> {len(product_types)} product types, {Product.objects.count()} products ({product_count} new)")


# ============================================================
# 5. LOCALEVENTS: EventTypes + Events
# ============================================================
print("\n[5/7] Creating EventTypes + Events...")

EVENT_TYPES_DATA = [
    ("Workshop", "Hands-on learning sessions led by experts."),
    ("Meetup", "Casual gatherings for community members."),
    ("Talk", "Lectures and presentations on various topics."),
    ("Festival", "Larger celebratory events with multiple activities."),
    ("Open Mic", "Community performance and sharing nights."),
]

event_types = {}
for name, desc in EVENT_TYPES_DATA:
    et, _ = EventType.objects.get_or_create(name=name, defaults={"description": desc})
    event_types[name] = et

now = timezone.now()
EVENTS_DATA = [
    ("Beginner Pottery Workshop", "Workshop", "Learn the basics of wheel throwing in this 3-hour intro session.",
     "Quezon City Community Studio", now + timedelta(days=7), now + timedelta(days=7, hours=3), 12, "Available", "carol"),
    ("Sunday Coffee Meetup", "Meetup", "Casual coffee chat with the community. All welcome.",
     "Local Cafe, Cubao", now + timedelta(days=3, hours=10), now + timedelta(days=3, hours=12), 30, "Available", "frank"),
    ("Climate & Cities Talk", "Talk", "An evening lecture on urban sustainability.",
     "City Library Auditorium", now + timedelta(days=14), now + timedelta(days=14, hours=2), 100, "Available", "carol"),
    ("Spring Arts Festival", "Festival", "Three-day celebration of local artists, food, and music.",
     "Park Plaza", now + timedelta(days=21), now + timedelta(days=23), 500, "Available", "frank"),
    ("Open Mic Night", "Open Mic", "Bring your songs, poems, or stories. 5-min slots.",
     "The Loft Bar", now + timedelta(days=5, hours=20), now + timedelta(days=5, hours=23), 40, "Available", "carol"),
    ("Watercolor for Beginners", "Workshop", "Two-hour intro to watercolor techniques.",
     "Art Studio One", now - timedelta(days=14), now - timedelta(days=14) + timedelta(hours=2), 15, "Done", "carol"),
    ("Book Swap Sunday", "Meetup", "Bring books you're done with, take some you haven't read.",
     "Community Center", now + timedelta(days=10), now + timedelta(days=10, hours=4), 50, "Available", "frank"),
]

event_count = 0
for title, type_name, desc, location, start, end, capacity, status, organizer_username in EVENTS_DATA:
    event, created = Event.objects.get_or_create(
        title=title,
        defaults={
            "category": event_types[type_name],
            "description": desc,
            "location": location,
            "start_time": start,
            "end_time": end,
            "event_capacity": capacity,
            "status": status,
        },
    )
    if created:
        event.organizer.add(profiles[organizer_username])
        event_count += 1

print(f"  -> {len(event_types)} event types, {Event.objects.count()} events ({event_count} new)")


# ============================================================
# 6. DIY PROJECTS: Categories + Projects
# ============================================================
print("\n[6/7] Creating ProjectCategories + Projects...")

CATEGORIES_DATA = [
    ("Woodworking", "Projects involving wood, carpentry, and joinery."),
    ("Electronics", "Hobby electronics, microcontrollers, and circuits."),
    ("Crafts", "Paper crafts, sewing, knitting, and general crafting."),
    ("Home Improvement", "Repairs, renovations, and home upgrades."),
    ("Garden", "Outdoor planting, landscaping, and garden builds."),
]

categories = {}
for name, desc in CATEGORIES_DATA:
    c, _ = ProjectCategory.objects.get_or_create(name=name, defaults={"description": desc})
    categories[name] = c

PROJECTS_DATA = [
    ("Floating Bookshelf",
     "Woodworking",
     "Make a sleek floating bookshelf with hidden brackets.",
     "1x4 pine board, hidden shelf brackets, wood screws, sandpaper, stain.",
     "1. Cut board to length.\n2. Sand all surfaces.\n3. Stain and let dry.\n4. Mount brackets to wall.\n5. Slide shelf onto brackets.",
     "eve"),
    ("LED Strip Desk Lighting",
     "Electronics",
     "Add ambient LED lighting under your desk with an Arduino.",
     "Arduino Nano, WS2812B LED strip, 5V power supply, jumper wires.",
     "1. Wire LED strip to Arduino.\n2. Upload FastLED sketch.\n3. Mount strip under desk.\n4. Adjust patterns in code.",
     "frank"),
    ("Macrame Wall Hanging",
     "Crafts",
     "Beginner-friendly macrame project for a textured wall piece.",
     "Cotton macrame cord, wooden dowel, scissors.",
     "1. Cut 16 cords of equal length.\n2. Attach to dowel using lark's head knots.\n3. Create square knot pattern.\n4. Trim ends.",
     "eve"),
    ("Painted Accent Wall",
     "Home Improvement",
     "Transform a room with a geometric painted accent wall.",
     "Painter's tape, paint (2 colors), rollers, drop cloth.",
     "1. Tape geometric pattern.\n2. Apply primer.\n3. Paint base color and let dry.\n4. Tape and paint accent shapes.\n5. Remove tape carefully.",
     "frank"),
    ("Raised Vegetable Bed",
     "Garden",
     "Build a 4x8 raised garden bed for vegetables.",
     "Cedar boards, deck screws, soil, compost.",
     "1. Cut boards to size.\n2. Assemble box with screws.\n3. Place in chosen spot.\n4. Fill with soil mix.\n5. Plant your veggies.",
     "eve"),
    ("Pegboard Tool Wall",
     "Home Improvement",
     "Organize your tools with a wall-mounted pegboard.",
     "Pegboard panel, mounting hardware, pegboard hooks.",
     "1. Mark stud locations.\n2. Install spacers.\n3. Mount pegboard.\n4. Add hooks and arrange tools.",
     "frank"),
]

project_count = 0
for title, cat_name, desc, materials, steps, creator_username in PROJECTS_DATA:
    _, created = Project.objects.get_or_create(
        title=title,
        defaults={
            "category": categories[cat_name],
            "description": desc,
            "materials": materials,
            "steps": steps,
            "creator": profiles[creator_username],
        },
    )
    if created:
        project_count += 1

print(f"  -> {len(categories)} categories, {Project.objects.count()} projects ({project_count} new)")


# ============================================================
# 7. COMMISSIONS: Types + Commissions + Jobs
# ============================================================
print("\n[7/7] Creating CommissionTypes + Commissions + Jobs...")

COMMISSION_TYPES_DATA = [
    ("Event Production", "Commissions for organizing and running events."),
    ("Content Creation", "Writing, video, and creative content commissions."),
    ("Design", "Graphic, web, and product design commissions."),
    ("Development", "Software and web development commissions."),
    ("Photography", "Photo and video shoot commissions."),
]

commission_types = {}
for name, desc in COMMISSION_TYPES_DATA:
    ct, _ = CommissionType.objects.get_or_create(name=name, defaults={"description": desc})
    commission_types[name] = ct

# (title, type, description, people_required, status, maker_username, [(role, manpower), ...])
COMMISSIONS_DATA = [
    ("Summer Festival Crew",
     "Event Production",
     "Looking for a crew to help run our 3-day summer festival.",
     8, "Open", "eve",
     [("Stage Manager", 1), ("Sound Tech", 2), ("Volunteer Coordinator", 1), ("Social Media", 2), ("Logistics", 2)]),
    ("Community Newsletter Team",
     "Content Creation",
     "Building a team to launch a monthly community newsletter.",
     5, "Open", "frank",
     [("Editor", 1), ("Writer", 3), ("Layout Designer", 1)]),
    ("Brand Refresh for Cafe",
     "Design",
     "Local cafe needs a new visual identity package.",
     3, "Open", "eve",
     [("Lead Designer", 1), ("Brand Strategist", 1), ("Illustrator", 1)]),
    ("Volunteer Portal MVP",
     "Development",
     "Build a basic web app for volunteer signups.",
     4, "Open", "frank",
     [("Frontend Dev", 2), ("Backend Dev", 1), ("Project Manager", 1)]),
    ("Wedding Photography",
     "Photography",
     "Two-day wedding shoot with reception coverage.",
     3, "Open", "eve",
     [("Lead Photographer", 1), ("Second Shooter", 1), ("Editor", 1)]),
]

commission_count = 0
job_count = 0
for title, type_name, desc, people, status, maker_username, jobs_data in COMMISSIONS_DATA:
    commission, created = Commission.objects.get_or_create(
        title=title,
        defaults={
            "commission_type": commission_types[type_name],
            "description": desc,
            "people_required": people,
            "status": status,
            "maker": profiles[maker_username],
        },
    )
    if created:
        commission_count += 1
        for role, manpower in jobs_data:
            Job.objects.create(
                commission=commission,
                role=role,
                manpower_required=manpower,
                status="Open",
            )
            job_count += 1

print(f"  -> {len(commission_types)} commission types, {Commission.objects.count()} commissions, {Job.objects.count()} jobs")


# ============================================================
# DONE
# ============================================================
print("\n" + "=" * 60)
print("SEEDING COMPLETE")
print("=" * 60)
print("\nLogin credentials (all users):")
print("  Password: password123")
print("\nUsers and their roles:")
for u in USERS_DATA:
    print(f"  {u['username']:8s} -> {', '.join(u['roles'])}")
print("\nDone! Run 'python manage.py runserver' to view the site.")
