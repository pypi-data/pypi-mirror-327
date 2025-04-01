# houseteli_administrator

## Usage

- Add as submodule

```bash
git submodule add git@github.com:houseteli/houseteli_administrator.git houseteli_administrator
```

- Add to installed apps

```python
INSTALLED_APPS = [
    # ...
    'houseteli_administrator',
]

AUTHENTICATION_BACKENDS = [
    'houseteli_administrator.backends.SessionEnhancingAuthBackend',
    # ...
]

MIDDLEWARE = [
    # ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "houseteli_administrator.middleware.SharedSessionMiddleware",
]


### for auth services, you will not need to have houseteli_administrator.middleware.SharedSessionMiddleware in the main auth service
HAS_ADMIN_LOGIN_PAGE = config('HAS_ADMIN_LOGIN_PAGE', default='False', cast=bool)
if not HAS_ADMIN_LOGIN_PAGE:
    MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1, 'houseteli_administrator.middleware.SharedSessionMiddleware')


```

- Add urls entry

```python
urlpatterns = [
    #...
    path('', include('houseteli_administrator.urls')),
]
```

- Whitelabeling admin


```python
from houseteli_administrator import utils as admin_utils
admin_utils.set_site_id()
```