from tortoise import fields, models


class UrlModel(models.Model):
    sc = fields.CharField(pk=True, max_length=10)
    redirect_url = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "urls"
