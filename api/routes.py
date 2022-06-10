from flask_restx import Namespace, Resource, fields


api = Namespace("api", description="Example API")


message = api.model("Example", {
    "message": fields.String,
})


@api.route("/hello-world", doc={
    "description": "Returns a hello world message",
})
class HelloWorld(Resource):
    @api.doc(responses={200: "OK"}, model=message)
    def get(self):
        api.logger.debug("Hello World!")
        return {"message": "Hello World!"}
