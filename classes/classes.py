from pydantic import BaseModel


class TokenCash(BaseModel):
    token_type: str
    access_token: str


class Applications(BaseModel):
    subdomain: str
    account_id: int
    token_cash: TokenCash


class Subscription(BaseModel):
    enabled: bool
    generations_limit: int


class Response(BaseModel):
    tmp: str

