from fastapi import FastAPI, Query

app = FastAPI()

# ── Sample Data (Database) ─────────────────────

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499},
    {"id": 2, "name": "Notebook", "price": 99},
    {"id": 3, "name": "Pen Set", "price": 49},
    {"id": 4, "name": "USB Hub", "price": 799}
]

# ── Search Endpoint ───────────────────────────

@app.get("/products/search")
def search_products(keyword: str = Query(...)):

    results = [p for p in products if keyword.lower() in p["name"].lower()]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "results": results,
        "total_found": len(results)
    }


# ── Sort Endpoint ─────────────────────────────

@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = (order == "desc")

    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# ── Pagination Endpoint (NEW) ─────────────────

@app.get("/products/page")
def paginate_products(
    page: int = Query(1),
    limit: int = Query(2)
):

    # Calculate start and end index
    start = (page - 1) * limit
    end = start + limit

    # Slice products
    paginated = products[start:end]

    # Calculate total pages (ceiling division)
    total_pages = -(-len(products) // limit)

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paginated
    }