
# Internal modules
from app.models.dto import NewUserRequest
from app.models import User
from app.error import BadRequestError

def create_user(user: NewUserRequest):
	validate_password(user)
	new_user = User(id=_new_id(), username=user.username, password=user.password, salt="")
	
	pass


def validate_password(user: NewUserRequest) -> None:
	if len(user.password) < 8:
		raise BadRequestError("Password too short")
	elif user.password is not user.rep_password:
		raise BadRequestError("Passwords don't match")


#####

def _new_id() -> str:
	return str(uuid4()).lower()
