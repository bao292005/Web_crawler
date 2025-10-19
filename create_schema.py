import requests
import dotenv

dotenv.load_dotenv()

BASE_URL = "http://localhost:8055"  # Đổi thành URL Directus của bạn
TOKEN = os.getenv("DIRECTUS_API_KEY")    # Đổi thành token admin Directus

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


# ========================
#  FUNCTIONS
# ========================

def create_collection(name, note=""):
    payload = {
        "collection": name,
        "meta": {
            "icon": "table_chart",
            "note": note
        },
        "schema": {
            "name": name,
            "is_primary_key": True,
            "default_value": "gen_random_uuid()"
        }
    }
    r = requests.post(f"{BASE_URL}/collections", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"⚠️ Collection {name} already exists or error: {r.text}")
    else:
        print(f"✅ Created collection {name}")


def create_field(collection, field, ftype, pk=False, nullable=True, default=None):
    # Directus tự tạo id khi create collection, skip để tránh lỗi trùng
    if field == "id":
        return

    payload = {
        "field": field,
        "type": ftype,
        "schema": {
            "is_nullable": nullable,
            "is_primary_key": True,
            "default_value": "gen_random_uuid()"
        },
        "meta": {
            "interface": "text-input",
            "note": field
        }
    }

    r = requests.post(f"{BASE_URL}/fields/{collection}", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"⚠️ Field {field} in {collection} error: {r.text}")
    else:
        print(f"   ➕ Field {field} in {collection}")


def create_relation(collection, field, related_collection, on_delete="CASCADE"):
    payload = {
        "collection": collection,
        "field": field,
        "related_collection": related_collection,
        "schema": {
            "on_delete": on_delete
        },
        "meta": {
            "many_collection": collection,
            "many_field": field,
            "one_collection": related_collection,
            "one_field": "id"
        }
    }
    r = requests.post(f"{BASE_URL}/relations", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"⚠️ Relation {collection}.{field} -> {related_collection} error: {r.text}")
    else:
        print(f"🔗 Relation {collection}.{field} -> {related_collection}")


# ========================
#  DEFINE COLLECTIONS + FIELDS
# ========================
collections = {
    "Sites": [
        ("id", "uuid", True),
        ("name", "string", False),
        ("url", "string", False),
        ("tagline", "string", True),
        ("description", "string", True),
        ("logo", "string", True),
        ("favicon", "string", True),
    ],
    "Contents": [
        ("id", "uuid", True),
        ("type", "string", False),
        ("title", "string", False),
        ("slug", "string", False),
        ("status", "string", False),
        ("content", "text", True),
        ("blocks", "json", True),
        ("published_at", "dateTime", True),
        ("site_id", "uuid", False),
        ("author_id", "uuid", False),
        ("category_id", "uuid", True),
        ("featured_image", "uuid", True),
    ],
    "Forms": [
        ("id", "uuid", True),
        ("title", "string", False),
        ("fields", "json", True),
        ("site_id", "uuid", False),
    ],
    "Navigation": [
        ("id", "uuid", True),
        ("key", "string", False),
        ("is_active", "boolean", False),
        ("site_id", "uuid", False),
    ],
    "NavigationItems": [
        ("id", "uuid", True),
        ("title", "string", False),
        ("link", "string", False),
        ("sort", "integer", False),
        ("type", "string", False),
        ("navigation_id", "uuid", False),
        ("parent_id", "uuid", True),
    ],
    "Categories": [
        ("id", "uuid", True),
        ("name", "string", False),
        ("slug", "string", False),
        ("description", "string", True),
        ("parent_id", "uuid", True),
    ],
    "Tags": [
        ("id", "uuid", True),
        ("name", "string", False),
        ("slug", "string", False),
    ],
    "Comments": [
        ("id", "uuid", True),
        ("content_id", "uuid", False),
        ("user_id", "uuid", True),
        ("guest_name", "string", True),
        ("content", "text", False),
        ("created_at", "dateTime", False),
        ("status", "string", False),
    ]
}

# ========================
#  DEFINE RELATIONS
# ========================
relations = [
    ("Contents", "site_id", "Sites"),
    ("Forms", "site_id", "Sites"),
    ("Navigation", "site_id", "Sites"),
    ("SiteUsers", "site_id", "Sites"),

    ("NavigationItems", "navigation_id", "Navigation"),
    ("NavigationItems", "parent_id", "NavigationItems"),

    ("Contents", "author_id", "Users"),
    ("SiteUsers", "user_id", "Users"),
    ("Comments", "user_id", "Users"),

    ("Contents", "category_id", "Categories"),
    ("Categories", "parent_id", "Categories"),

    ("PostTags", "content_id", "Contents"),
    ("PostTags", "tag_id", "Tags"),

    ("Comments", "content_id", "Contents"),
]

# ========================
#  RUN ALL
# ========================
for coll, fields in collections.items():
    create_collection(coll)
    for f in fields:
        create_field(coll, f[0], f[1], pk=f[2] if len(f) > 2 else False)

for rel in relations:
    create_relation(rel[0], rel[1], rel[2])
# Create a standalone collection with only id and title
# create_collection("SimpleItems", "A minimal collection with id and title")
# create_field("SimpleItems", "id", "uuid", pk=True, nullable=False)
# create_field("SimpleItems", "title", "string", nullable=False)
