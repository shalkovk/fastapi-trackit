from pydantic import BaseModel


class TokenResponse(BaseModel):
    acces_token: str
    token_type: str
