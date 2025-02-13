"""
Function and class decorators for enhanced functionality.

This module provides decorators for type checking, timing, and dataclass enhancements.
"""

from __future__ import annotations

__all__ = [
    "semistaticmethod",
    "hybridproperty",
    "cls_method_timer",
    "timer",
    "type_check",
    "strongdataclass"
]

import inspect
import time
import sys
from dataclasses import dataclass, fields, MISSING
from collections import OrderedDict
from functools import partial, wraps
from typing import (
    Any, Callable, Optional, Type, TypeVar, Union,
    get_type_hints, cast, Generic
)

from .type_validation import check_type, get_type_hint_str
from .typing import NOTSET

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


class semistaticmethod(Generic[F]):
    """
    Descriptor for static methods that can access instance when called from instance.
    
    Parameters
    ----------
    func : Callable
        The function to be converted into a semi-static method
        
    Examples
    --------
    >>> class MyClass:
    ...     @semistaticmethod
    ...     def my_method(self_or_cls):
    ...         return self_or_cls
    ...
    >>> MyClass.my_method()  # Returns class
    >>> obj = MyClass()
    >>> obj.my_method()  # Returns instance
    """

    def __init__(self, func: F) -> None:
        self.func = func

    def __get__(
        self,
        obj: Optional[Any],
        cls: Optional[Type[Any]] = None
    ) -> Callable[..., Any]:
        if obj is None and cls is not None:
            return partial(self.func, cls)
        if obj is not None:
            return partial(self.func, obj)
        return self.func

    @property
    def __func__(self) -> F:
        """Get the original function."""
        return self.func


class hybridproperty(Generic[T]):
    """
    Decorator for properties that work at both class and instance level.
    
    This decorator allows defining different behaviors for when the property
    is accessed at the class level versus the instance level.

    Parameters
    ----------
    fcls : Callable
        Function to call for class-level access
    finst : Optional[Callable]
        Function to call for instance-level access
        If None, uses class-level implementation
    """
    
    def __init__(
        self,
        fcls: Callable[..., T],
        finst: Optional[Callable[..., T]] = None
    ) -> None:
        self.fcls = fcls
        self.finst = finst or fcls

    def __get__(
        self,
        instance: Optional[Any],
        cls: Optional[Type] = None
    ) -> T:
        if instance is None and cls is not None:
            return self.fcls(cls)
        if instance is not None:
            return self.finst(instance)
        raise TypeError("Cannot access property from neither instance nor class")

    def instance(self, finst: Callable[..., T]) -> hybridproperty[T]:
        """Decorator to set the instance-level implementation."""
        return type(self)(self.fcls, finst)


def cls_method_timer(func: F) -> F:
    """
    Time execution of class methods.
    
    Parameters
    ----------
    func : Callable
        The class method to time
        
    Returns
    -------
    Callable
        Wrapped method that prints execution time
        
    Examples
    --------
    >>> class MyClass:
    ...     @cls_method_timer
    ...     def my_method(self):
    ...         time.sleep(1)
    """
    
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        t1 = time.time()
        result = func(self, *args, **kwargs)
        t2 = time.time()
        
        method_name = f"{type(self).__name__}::{func.__name__}"
        self.stdout.info(
            f'Task {method_name!r} executed in {(t2 - t1):.3f} s'
        )
        return result

    return cast(F, wrapper)


class timer:
    """
    Context manager for timing code blocks.
    
    Measures both real time and CPU time elapsed.
    
    Examples
    --------
    >>> with timer() as t:
    ...     time.sleep(1)
    >>> print(f"{t.real_time_elapsed:.1f}s")
    1.0s
    """

    def __init__(self) -> None:
        self.start_real: float = 0.0
        self.start_cpu: float = 0.0
        self.end_real: float = 0.0
        self.end_cpu: float = 0.0
        self.interval: float = 0.0
        self.real_time_elapsed: float = 0.0
        self.cpu_time_elapsed: float = 0.0

    def __enter__(self) -> timer:
        """Start timing."""
        self.start_real = time.time()
        self.start_cpu = time.process_time()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop timing and compute intervals."""
        self.end_cpu = time.process_time()
        self.end_real = time.time()
        self.interval = self.end_real - self.start_real
        self.real_time_elapsed = self.interval
        self.cpu_time_elapsed = self.end_cpu - self.start_cpu


def type_check(func: F) -> F:
    """
    Decorator for runtime type checking of function arguments.
    
    Parameters
    ----------
    func : Callable
        Function to add type checking to
        
    Returns
    -------
    Callable
        Wrapped function that validates argument types
        
    Raises
    ------
    TypeError
        If an argument's type doesn't match its annotation
        
    Examples
    --------
    >>> @type_check
    ... def greet(name: str, count: int) -> str:
    ...     return name * count
    >>> greet("hi", 3)
    'hihihi'
    >>> greet("hi", "3")  # Raises TypeError
    """
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
		# Check each argument against its type hint
        for name, value in bound.arguments.items():
            param = sig.parameters.get(name)
            if param is None or param.annotation is param.empty:
                continue
            
            if not check_type(value, param.annotation):
                type_hint_str = get_type_hint_str(param.annotation)
                raise TypeError(
                    f'Type check failed for function "{func.__qualname__}". '
                    f'Argument "{name}" must be of type {type_hint_str}, '
                    f'got {type(value).__name__}'
                )
                
        return func(*args, **kwargs)
        
    return cast(F, wrapper)


def strongdataclass(
    cls: Optional[Type[T]] = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> Union[Callable[[Type[T]], Type[T]], Type[T]]:
    """
    Create a dataclass with runtime type checking.
    
    Parameters
    ----------
    cls : Optional[Type]
        Class to decorate
    init, repr, eq, order, unsafe_hash, frozen : bool
        Standard dataclass parameters
        
    Returns
    -------
    Union[Callable[[Type], Type], Type]
        Decorated class with type checking
        
    Examples
    --------
    >>> @strongdataclass
    ... class Person:
    ...     name: str
    ...     age: int
    >>> p = Person("Alice", 30)  # OK
    >>> p = Person("Alice", "30")  # Raises TypeError
    """
    
    def wrap(cls: Type[T]) -> Type[T]:
        cls = dataclass(
            cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen
        )
        
        type_hints = get_type_hints(cls)
        
        for field in fields(cls):
            private_name = f"_{field.name}"
            public_name = field.name
            type_hint = type_hints.get(field.name, NOTSET)

            def getter(
                self: Any,
                private_name: str = private_name
            ) -> Any:
                return getattr(self, private_name)

            def setter(
                self: Any,
                value: Any,
                private_name: str = private_name,
                type_hint: Any = type_hint
            ) -> None:
                if (
                    type_hint is not NOTSET and
                    not check_type(value, type_hint)
                ):
                    public_name = private_name.lstrip('_')
                    type_hint_str = get_type_hint_str(type_hint)
                    raise TypeError(
                        f'`{public_name}` expects type {type_hint_str}, '
                        f'got {type(value).__name__}'
                    )
                setattr(self, private_name, value)
            
            setattr(cls, public_name, property(getter, setter))
            
        return cls

    if cls is None:
        return wrap
        
    return wrap(cls)



def _reorder_fields_for_kw_only(cls: Type[Any]) -> Type[Any]:
    """
    Reorder the __dataclass_fields__ so that fields with no default (i.e. required)
    appear before fields with a default value. This helps mimic Python 3.10's kw_only
    behavior by moving fields that should be keyword-only to the end of the __init__
    signature.
    """
    fields = cls.__dataclass_fields__

    # A field is considered required if its default is MISSING and it has no default_factory.
    def is_required(item):
        field_obj = item[1]
        return field_obj.default is MISSING and field_obj.default_factory is MISSING

    # Sort so that required fields come first.
    sorted_fields = sorted(fields.items(), key=lambda item: not is_required(item))
    cls.__dataclass_fields__ = OrderedDict(sorted_fields)
    return cls

def dataclass_ex(
    _cls: T = None, *, kw_only: bool = False, **kwargs: Any
) -> Callable[[T], T]:
    """
    A decorator that wraps Python's built-in dataclass.

    Parameters
    ----------
    kw_only : bool
        If True, the generated __init__ will be arranged so that fields with defaults
        (i.e. optional fields) come after the required fields. In Python 3.10 and later,
        this is done via the built-in 'kw_only' parameter. For Python 3.7–3.9, the
        field ordering is adjusted to emulate keyword-only fields.
    **kwargs
        Other keyword arguments passed to the built-in dataclass decorator.

    Returns
    -------
    The decorated class.
    """
    def wrap(cls: T) -> T:
        # For Python 3.10 and later, pass kw_only to the built-in dataclass.
        if sys.version_info >= (3, 10):
            new_cls = dataclass(cls, kw_only=kw_only, **kwargs)
        else:
            # For Python 3.7–3.9, remove kw_only from kwargs (if present)
            # and then adjust the field ordering if needed.
            new_cls = dataclass(cls, **kwargs)
            if kw_only:
                new_cls = _reorder_fields_for_kw_only(new_cls)
        return new_cls

    # Support both decorator-with-arguments and decorator-without-arguments usage.
    if _cls is not None:
        return wrap(_cls)
    else:
        return wrap