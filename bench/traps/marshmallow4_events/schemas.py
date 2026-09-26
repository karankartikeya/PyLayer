from marshmallow import EXCLUDE, Schema, fields, post_load


class EventSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    tags = fields.List(fields.String(), missing=list)
    status = fields.String(default="draft")
    starts_at = fields.DateTime()

    @post_load(pass_many=True)
    def sort_events(self, data, many, **kwargs):
        if many:
            return sorted(data, key=lambda e: e["starts_at"])
        return data


def load_events(payload: list[dict]) -> list[dict]:
    return EventSchema(many=True).load(payload)


def dump_event(obj) -> dict:
    return EventSchema().dump(obj)
