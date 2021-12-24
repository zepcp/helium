from calendar import month_abbr

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiocache import cached

from database.database import Database
from settings import settings
from apis.helium import rewards

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
@cached(ttl=60 * 15, key_builder=(lambda _, *args, **kwargs: kwargs['month']))
async def root(request: Request, db: Database = Depends(settings.database),
               month: int = 0, year: int = 2021):
    if month < 0 or month > 12 or year < 2021 or year > 2030:
        raise ValueError

    min_time = f"{year}-{month}-01" if month > 9 \
        else f"{year}-0{month}-01" if month > 0 \
        else "2021-01-01"

    max_time = f"{year + 1}-01-01" if month == 12 \
        else f"{year}-{month + 1}-01" if month > 8 \
        else f"{year}-0{month + 1}-01" if month > 0 \
        else "2030-01-01"

    my_rewards = await rewards(min_time, max_time, db)
    res = {"z": 0, "v": 0, "j": 0, "m": 0, "gu": 0, "gr": 0, "d": 0,
           "year": year, "month": month_abbr[month] if month > 0 else "Total"}

    for x in my_rewards:
        owner = x.get("hotspot").owner
        reward = x.get("reward")
        if owner == "vasco":
            res["v"] += reward.get("owner")
            res["z"] += reward.get("referral")
        elif owner == "jorge":
            res["j"] += reward.get("owner")
            res["z"] += reward.get("referral")
        elif owner == "marcia":
            res["m"] += reward.get("owner")
            res["v"] += reward.get("referral")
        elif owner == "guilherme":
            res["gu"] += reward.get("owner")
            res["v"] += reward.get("referral")
        elif owner == "graca":
            res["gr"] += reward.get("owner")
            res["z"] += reward.get("referral")
        elif owner == "dani":
            res["d"] += reward.get("owner")
            res["v"] += reward.get("referral")

    res["v"], res["z"] = round(res["v"], 2), round(res["z"], 2)
    return templates.TemplateResponse("index.html", {"request": request, **res})
