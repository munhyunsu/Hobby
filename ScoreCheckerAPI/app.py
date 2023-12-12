from typing import Annotated

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager


import schemas
from secret import load_data, check_user_agent


USERS = None
DATA = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global USERS
    global DATA
    USERS, DATA = load_data()
    yield


app = FastAPI(
  title='Score checker',
  version='1.0.0',
  description='''성적 확인을 위한 API
  ''',
  contact={
    'name': 'Data Networks Laboratory',
    'url': 'https://dnlab.cs-cnu.org/',
    'email': 'munhyunsu@cs-cnu.org',
  },
  license_info={
    'name': 'The GNU General Public License v3.0',
    'url': 'https://www.gnu.org/licenses/gpl-3.0.en.html#license-text',
  },
  lifespan=lifespan,
)


@app.get('/', include_in_schema=False)
def get_root():
    return {'message': 'Hello World!'}


@app.post('/score', response_model=schemas.UserScore)
def post_score(user: schemas.User, request: Request):
    global USERS
    global DATA
    score = dict()
    name = user.name
    identifier = user.identifier
    number = None

    if check_user_agent(request.headers.get('User-Agent')):
        finder = USERS[(USERS['이름'] == user.name) & (USERS['식별자'] == user.identifier)]
        if len(finder) > 0:
            number = finder['학번'].to_numpy()[0]
            for key, value in DATA.items():
                part = dict()
                for c1, c2 in value.columns:
                    subpart = part.get(c1, dict())
                    subpart[c2] = value[value[('사용자', '학번')] == number][(c1, c2)].to_list()[0]
                    part[c1] = subpart
                score[key] = part

    user_score = schemas.UserScore(name=user.name,
                                   number=number,
                                   identifier=identifier,
                                   score=score)

    return user_score
