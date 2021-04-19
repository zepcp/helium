from datetime import datetime
import calendar

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.database import Database
from settings import settings
from apis.helium import rewards

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Database = Depends(settings.database),
               month: int = datetime.today().month - 1):
    if month < 1 or month > 12:
        raise ValueError

    min_time = "2021-{}-01".format(month) if month > 9 \
        else "2021-0{}-01".format(month)

    max_time = "2021-{}-01".format(month + 1) if month > 8 \
        else "2021-0{}-01".format(month + 1)

    my_rewards = await rewards(min_time, max_time, db)
    res = {"z": 0, "v": 0, "j": 0, "m": 0, "g": 0,
           "month": calendar.month_abbr[month]}

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
            res["g"] += reward.get("owner")
            res["v"] += reward.get("referral")

    res["v"], res["z"] = round(res["v"], 2), round(res["z"], 2)
    return templates.TemplateResponse("index.html", {"request": request, **res})
