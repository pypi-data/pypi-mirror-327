from jupyterhub.apihandlers import default_handlers
from jupyterhub.apihandlers.base import APIHandler
from jupyterhub.scopes import needs_scope
from tornado import web

from .utils import EncryptJSONBody


class SpawnOptionsUpdateAPIHandler(EncryptJSONBody, APIHandler):
    @needs_scope("access:servers")
    async def post(self, user_name, server_name=""):
        user = self.find_user(user_name)
        if user is None:
            # no such user
            self.log.error(
                f"{user_name}:{server_name} - APICall: SpawnOptionsUpdate - No user found",
                extra={"user": user_name, "log_name": f"{user_name}:{server_name}"},
            )
            raise web.HTTPError(404)
        orm_user = user.orm_user

        if server_name not in orm_user.orm_spawners:
            # user has no such server
            self.log.error(
                f"{user_name}:{server_name} - APICall: SpawnOptionsUpdate - No spawner found",
                extra={
                    "user": user,
                    "spawner": server_name,
                    "log_name": f"{user_name}:{server_name}",
                },
            )
            raise web.HTTPError(404)
        spawner = orm_user.orm_spawners[server_name]
        # Save new options
        formdata = self.get_json_body()
        spawner.user_options = formdata
        self.db.commit()
        self.set_status(204)


default_handlers.append(
    (r"/api/users/([^/]+)/server/update", SpawnOptionsUpdateAPIHandler)
)
default_handlers.append(
    (r"/api/users/([^/]+)/servers/([^/]*)/update", SpawnOptionsUpdateAPIHandler)
)
