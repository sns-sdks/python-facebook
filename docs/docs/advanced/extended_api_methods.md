# Extended API

For this library only packaged the common page api methods for facebook api.

And sometimes you need some more methods. So you can just extend this with your custom code.

Now we provide an example [Extend API](https://github.com/sns-sdks/python-facebook/tree/master/examples/extend_api.py).

As for our structure. Need two parts of extends.

## make data model

We use [attrs](https://github.com/python-attrs/attrs) to build data model.

```python
from typing import Optional
from attr import attrs, attrib
from pyfacebook import BaseModel

@attrs
class People(BaseModel):
    """
    Refer: https://developers.facebook.com/docs/graph-api/reference/v6.0/conversation
    """
    id = attrib(default=None, type=Optional[str])
    name = attrib(default=None, type=Optional[str])
    email = attrib(default=None, type=Optional[str], repr=False)
```


## Create API Method

We will use the core method `_request` to build api method.

```python
from pyfacebook import Api

class ExtApi(Api):
    def page_by_next(self,
                     target,  # type: str
                     resource,  # type: str
                     args,  # type: Dict
                     next_page,  # type: str
                     ):
        # type: (...) -> (str, Dict)
        """
        :param target: target id
        :param resource: target resource field
        :param args: fields for this resource
        :param next_page: next page url
        :return:
        """
        if next_page is not None:
            resp = self._request(
                path=next_page
            )
        else:
            resp = self._request(
                path="{version}/{target}/{resource}".format(
                    version=self.version, target=target, resource=resource
                ),
                args=args
            )
        next_page = None
        data = self._parse_response(resp)
        if "paging" in data:
            next_page = data["paging"].get("next")
        return next_page, data
```

## Use the custom Api

Now we can use our custom api.

```python
api = ExtApi(long_term_token="long-term-token")

con = api.get_page_conversations(
    page_id="2121008874780932",
    access_token="page access token",
    limit=10,
)
print(con)
```
