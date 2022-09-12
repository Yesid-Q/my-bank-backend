from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        allow_population_by_field_name = True
        fields = {
            'access_token': 'accessToken',
            'token_type': 'tokenType'
        }
