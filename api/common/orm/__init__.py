"""Common ORM."""

from api.common.orm.base import Base

# Import ORMs to initialize base.
from api.common.orm.feedbacks import Feedbacks
from api.common.orm.users import Users
from api.sample.orm.access_rights import ProductAccessRights
from api.sample.orm.products import Products
