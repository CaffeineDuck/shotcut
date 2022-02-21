from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.exceptions import IntegrityError

from models import UrlModel
from tortoise_config import db_uri

url_pydantic = pydantic_model_creator(UrlModel)
app = FastAPI()

register_tortoise(
    app,
    db_url=db_uri,
    modules={"models": ["models"]},
    add_exception_handlers=True,
)


@app.get("/{url_slug}")
async def get_sc(url_slug: str):
    url_model = await UrlModel.get_or_none(sc=url_slug)
    if not url_model:
        return {"error": "URL not found"}

    return RedirectResponse(url_model.redirect_url)


@app.post("/{url_slug}")
async def create_sc(url_slug: str, redirect_url=Form(...), password=Form(...)):
    try:
        url_model = await UrlModel.create(
            sc=url_slug, redirect_url=redirect_url, password=password
        )
    except IntegrityError:
        return {"error": "URL already exists"}

    return url_pydantic.from_orm(url_model)


@app.delete("/{url_slug}")
async def delete_sc(url_slug: str, password: str):
    if model := (await UrlModel.get_or_none(sc=url_slug, password=password)):
        await model.delete()
        return {"message": "URL deleted"}
    return {"error": "URL not found"}
