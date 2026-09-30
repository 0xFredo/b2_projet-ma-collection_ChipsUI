from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/", include_in_schema=False)
def read_root():
    return {"message": "API Ma Collection en ligne"}