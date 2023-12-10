from fastapi import FastAPI


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
)


@app.get('/')
def get_root():
    return {'message': 'Hello World!'}



