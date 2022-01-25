import functools
import inspect
import typing
from typing import Any, Callable, List, Tuple, Type

from flask import Blueprint, Request, Response, request

from manager.schemas import model
from manager.utils.http import json_response

request: Request = request


class ModelValidator(object):
    def __init__(self, name: str, _type: Any, source: model.Source):
        self.name = name
        self._type = _type
        self.source = source
        self.data_from = self.source.data_from
        assert self.data_from in (
            "PATH",
            "QUERY",
            "HEADER",
            "COOKIE",
            "FORM",
            "FILE",
            "JSON",
        )
        self.alias = self.source.alias or self.name

    def __call__(self):
        if self.data_from == "PATH":
            paths = request.view_args or {}
            if self.source.embed or not model.is_dict_type(self._type):
                return model.validate(
                    value=paths.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("path", self.alias),
                )
            return model.validate(
                value=paths,
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("path",),
            )
        if self.data_from == "QUERY":
            if self.source.embed or not model.is_dict_type(self._type):
                if model.is_list_type(self._type):
                    return model.validate(
                        value=request.args.getlist(self.alias),
                        name=self.name,
                        source=self.source,
                        _type=self._type,
                        loc=("query", self.alias),
                    )
                return model.validate(
                    value=request.args.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("query", self.alias),
                )
            data = request.args.to_dict()
            if isinstance(self._type, type) and issubclass(self._type, model.Model):
                for name, _type in self._type.__fields__.items():
                    name = _type.alias or _type.name or name
                    if model.is_list_type(_type.outer_type_):
                        data[name] = request.args.getlist(name)
            return model.validate(
                value=data,
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("query",),
            )
        if self.data_from == "HEADER":
            if self.source.embed or not model.is_dict_type(self._type):
                if model.is_list_type(self._type):
                    return model.validate(
                        value=request.headers.getlist(self.alias),
                        name=self.name,
                        source=self.source,
                        _type=self._type,
                        loc=("header", self.alias),
                    )
                return model.validate(
                    value=request.headers.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("header", self.alias),
                )
            return model.validate(
                value=dict(request.headers),
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("header",),
            )
        if self.data_from == "COOKIE":
            if self.source.embed or not model.is_dict_type(self._type):
                return model.validate(
                    value=request.cookies.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("cookie", self.alias),
                )
            return model.validate(
                value=dict(request.cookies),
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("cookie",),
            )
        if self.data_from == "FORM":
            if self.source.embed or not model.is_dict_type(self._type):
                if model.is_list_type(self._type):
                    return model.validate(
                        value=request.form.getlist(self.alias),
                        name=self.name,
                        source=self.source,
                        _type=self._type,
                        loc=("form", self.alias),
                    )
                return model.validate(
                    value=request.form.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("form", self.alias),
                )
            data = dict(request.form)
            if isinstance(self._type, type) and issubclass(self._type, model.Model):
                for name, _type in self._type.__fields__.items():
                    name = _type.alias or _type.name or name
                    if model.is_list_type(_type.outer_type_):
                        data[name] = request.form.getlist(name)
            return model.validate(
                value=data,
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("form",),
            )
        if self.data_from == "FILE":
            if self.source.embed or not model.is_dict_type(self._type):
                if model.is_list_type(self._type):
                    return model.validate(
                        value=request.files.getlist(self.alias),
                        name=self.name,
                        source=self.source,
                        _type=self._type,
                        loc=("form", self.alias),
                    )
                return model.validate(
                    value=request.files.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("form",),
                )
            data = dict(request.files)
            if isinstance(self._type, type) and issubclass(self._type, model.Model):
                for name, _type in self._type.__fields__.items():
                    name = _type.alias or _type.name or name
                    if model.is_list_type(_type.outer_type_):
                        data[name] = request.files.getlist(name)
            return model.validate(
                value=data,
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("form",),
            )
        if self.data_from == "JSON":
            if self.source.embed:
                data = model.JSON(request.data)
                if model.is_list_type(self._type):
                    return model.validate(
                        value=data.get(self.alias),
                        name=self.name,
                        source=self.source,
                        _type=self._type,
                        loc=("body", self.alias),
                    )
                return model.validate(
                    value=data.get(self.alias),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("body", self.alias),
                )
            if model.is_list_type(self._type):
                return model.validate(
                    value=model.LIST(request.data),
                    name=self.name,
                    source=self.source,
                    _type=self._type,
                    loc=("body", self.alias),
                )
            return model.validate(
                value=model.JSON(request.data),
                name=self.name,
                source=self.source,
                _type=self._type,
                loc=("body", self.alias),
            )


class Router(object):
    OPTION_NAME = "_route_option"
    PREFIX_NAME = "_route_prefix"
    PUBLIC_MIDDLEWARE_VALIDATORS = "_router_middleware_validators"
    ROUTER_FUNCS = "_route_funcs"
    RESPONSE_SCHEMAS = "_route_response_schemas"

    class Option(object):
        def __init__(
            self,
            method: str,
            rule: str,
            endpoint: str,
            summary: str,
        ):
            self.method = method
            self.rule = rule.lstrip("/")
            self.endpoint = endpoint
            self.summary = summary

    class Prefix(object):
        def __init__(self, prefix: str, summary: str):
            self.prefix = prefix.lstrip("/")
            self.summary = summary

    @classmethod
    def route(
        cls,
        method: str,
        rule: str,
        endpoint: str = None,
        summary: str = None,
    ):
        def decorator(func):
            funcs: set = getattr(cls, Router.ROUTER_FUNCS, set())
            if func.__qualname__ in funcs:
                raise RuntimeError(f"router func {func.__qualname__} already declared")
            funcs.add(func.__qualname__)
            setattr(cls, Router.ROUTER_FUNCS, funcs)

            option: Router.Option = Router.Option(
                method=method,
                rule=rule,
                endpoint=endpoint or func.__name__,
                summary=summary,
            )

            signature = inspect.signature(func)
            validators = []

            for name, param in signature.parameters.items():
                if isinstance(param.default, model.Source):
                    validators.append(
                        ModelValidator(
                            name=name, _type=param.annotation, source=param.default
                        )
                    )
                elif name == "self":
                    continue
                else:
                    raise RuntimeError("parameter type undefined")

            @functools.wraps(func)
            def inner(self, **paths):

                data = {}
                for validator in validators:
                    data[validator.name] = validator()

                response: Any = func(self, **data)
                if isinstance(response, Response):
                    return response
                if isinstance(response, model.BaseModel):
                    return json_response(response.dict())
                return json_response(response)

            setattr(inner, Router.OPTION_NAME, option)
            return inner

        return decorator

    @classmethod
    def get(
        cls,
        rule: str,
        endpoint: str = None,
        summary: str = None,
    ):
        return cls.route(
            "GET",
            rule=rule,
            endpoint=endpoint,
            summary=summary,
        )

    @classmethod
    def post(
        cls,
        rule: str,
        endpoint: str = None,
        summary: str = None,
    ):
        return cls.route(
            "POST",
            rule=rule,
            endpoint=endpoint,
            summary=summary,
        )

    @classmethod
    def put(
        cls,
        rule: str,
        endpoint: str = None,
        summary: str = None,
    ):
        return cls.route(
            "PUT",
            rule=rule,
            endpoint=endpoint,
            summary=summary,
        )

    @classmethod
    def delete(
        cls,
        rule: str,
        endpoint: str = None,
        summary: str = None,
    ):
        return cls.route(
            "DELETE",
            rule=rule,
            endpoint=endpoint,
            summary=summary,
        )

    @classmethod
    def prefix(cls, prefix: str, summary: str):
        def decorator(class_cls):
            setattr(
                class_cls,
                Router.PREFIX_NAME,
                Router.Prefix(prefix=prefix, summary=summary),
            )
            return class_cls

        return decorator

    @classmethod
    def response(
        cls,
        model_schema: typing.Union[
            typing.Type[model.Model], typing.Type[typing.List[model.Model]]
        ],
        summary: str,
        status: int = 200,
    ):
        def decorator(func):
            response_schemas: list = getattr(func, Router.RESPONSE_SCHEMAS, [])
            response_schemas.append((status, summary, model_schema))
            setattr(func, Router.RESPONSE_SCHEMAS, response_schemas)
            return func

        return decorator


class ResourceMetaclass(type):
    def __new__(cls, name, bases, attrs):
        routes = {}
        for func_name, value in attrs.items():
            option = getattr(value, Router.OPTION_NAME, None)
            if option and isinstance(option, Router.Option):
                routes[func_name] = value
        attrs["__routes__"] = routes
        return type.__new__(cls, name, bases, attrs)


class BaseResource(metaclass=ResourceMetaclass):
    @classmethod
    def json_response(cls, data: dict, status_code: int = 200, headers: dict = None):
        return json_response(data=data, status=status_code, headers=headers)

    @classmethod
    def pagination_response(
        cls, items: list, pagination: dict, status_code: int = 200, headers: dict = None
    ):
        return json_response(
            dict(
                results=items,
                page=pagination["page"],
                total_pages=pagination["total_pages"],
                total_results=pagination["total_results"],
            ),
            status=status_code,
            headers=headers,
        )

    @classmethod
    def request_params(cls) -> dict:
        params: dict = request.args.to_dict()
        return params

    @classmethod
    def request_cookies(cls):
        return request.cookies

    @classmethod
    def request_headers(cls):
        return request.headers

    @classmethod
    def request_json(cls) -> dict:
        return model.JSON(request.data)

    @classmethod
    def request_content(cls) -> bytes:
        return request.data

    @classmethod
    def request_form(cls) -> dict:
        return dict(request.form)

    def __str__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}"


class BaseBlueprint(Blueprint):
    def __init__(self, name, import_name: str):
        super(BaseBlueprint, self).__init__(name=name, import_name=import_name)
        self._route_rules = {}
        self._groups = {}

    def add_url_rule(
        self, rule, endpoint=None, view_func=None, methods=None, **options
    ):
        rule_identifier = rule, ", ".join(methods or [])
        if rule_identifier in self._route_rules:
            previous = self._route_rules[rule_identifier]
            raise RuntimeError(
                f"route {methods} {rule} already declared. previous={previous}, redeclare at {endpoint}"
            )
        self._route_rules[rule_identifier] = endpoint
        return super(BaseBlueprint, self).add_url_rule(
            rule=rule,
            endpoint=endpoint,
            view_func=view_func,
            methods=methods,
            **options,
        )

    def register_resource(self, resource: BaseResource):
        resource_name = resource.__class__.__name__
        prefix: Router.Prefix = getattr(resource, Router.PREFIX_NAME, None)
        if prefix.summary in self._groups:
            previous = self._groups[prefix.summary]
            raise RuntimeError(
                f"Resource Group {prefix.summary} already declared. "
                f"previous={previous}, redeclare at {resource}"
            )
        self._groups[prefix.summary] = resource

        for name in getattr(resource, "__routes__").keys():
            func = getattr(resource, name, None)
            option: Router.Option = getattr(func, Router.OPTION_NAME, None)

            method: str = option.method
            endpoint: str = f"{resource_name}:{option.endpoint}"
            rule: str = option.rule
            if prefix and prefix.prefix:
                rule = f"/{prefix.prefix}/{rule}" if rule else f"/{prefix.prefix}"

            self.add_url_rule(
                rule=rule, endpoint=endpoint, view_func=func, methods=[method]
            )
