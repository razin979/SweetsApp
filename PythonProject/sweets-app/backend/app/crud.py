from . import database
from bson import ObjectId

async def create_user(email, hashed_password, is_admin=False):
    doc = {"email": email, "hashed_password": hashed_password, "is_admin": is_admin}
    res = await database.db.users.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

async def get_user_by_email(email):
    return await database.db.users.find_one({"email": email})

async def get_user_by_id(user_id):
    return await database.db.users.find_one({"_id": ObjectId(user_id)})

async def create_sweet(sweet):
    sweet_dict = sweet.model_dump()
    res = await database.db.sweets.insert_one(sweet_dict)
    sweet_dict["_id"] = res.inserted_id
    return {**sweet_dict, "id": str(res.inserted_id)}

async def list_sweets():
    sweets = await database.db.sweets.find().to_list(100)
    for s in sweets:
        s["id"] = str(s["_id"])
    return sweets

async def get_sweet_by_id(sweet_id):
    sweet = await database.db.sweets.find_one({"_id": ObjectId(sweet_id)})
    if sweet:
        sweet["id"] = str(sweet["_id"])
    return sweet

async def search_sweets(name=None, category=None, min_price=None, max_price=None):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if min_price or max_price:
        query["price"] = {}
        if min_price:
            query["price"]["$gte"] = min_price
        if max_price:
            query["price"]["$lte"] = max_price
    sweets = await database.db.sweets.find(query).to_list(100)
    for s in sweets:
        s["id"] = str(s["_id"])
    return sweets

async def update_sweet(sweet_id, sweet):
    update = {"$set": sweet.model_dump()}
    result = await database.db.sweets.update_one({"_id": ObjectId(sweet_id)}, update)
    if result.modified_count == 0:
        return None
    return await get_sweet_by_id(sweet_id)

async def delete_sweet(sweet_id):
    result = await database.db.sweets.delete_one({"_id": ObjectId(sweet_id)})
    return result.deleted_count > 0

async def purchase_sweet(sweet_id, quantity):
    await database.db.sweets.update_one({"_id": ObjectId(sweet_id)}, {"$inc": {"quantity": -quantity}})

async def restock_sweet(sweet_id, quantity):
    await database.db.sweets.update_one({"_id": ObjectId(sweet_id)}, {"$inc": {"quantity": quantity}})
