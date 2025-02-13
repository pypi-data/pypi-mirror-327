"""Main code for 'buildeasy' Python package which allows the user to make files into classes."""
import sys
import inspect

class FileAsClass:
    def __init_subclass__(cls, **init_kwargs):
        super().__init_subclass__(**init_kwargs)
        # Retrieve the caller’s module.
        caller_frame = sys._getframe(1)
        module_name = caller_frame.f_globals.get('__name__')
        if module_name is None:
            raise RuntimeError("Cannot determine module name from caller's frame.")
        module = sys.modules[module_name]

        # Prepare kwargs for the __init__ method.
        init_signature = inspect.signature(cls.__init__)
        parameters = list(init_signature.parameters.values())[1:]  # skip 'self'
        init_args = {}
        for param in parameters:
            if param.name in init_kwargs:
                init_args[param.name] = init_kwargs[param.name]
            elif param.default is not param.empty:
                init_args[param.name] = param.default
            else:
                init_args[param.name] = None

        # Create an instance.
        try:
            instance = cls(**init_args)
        except TypeError as e:
            raise TypeError(f"Error instantiating {cls.__name__}: {e}") from e

        # (Optional) If you want to “copy” public methods (this is not needed if the
        # module is literally replaced by the instance, since the instance already has them.)
        public_methods = []
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("_"):
                public_methods.append(attr_name)
        instance.__all__ = public_methods + ['instance']

        # For backwards compatibility, expose `instance` on itself.
        instance.instance = instance

        # Copy key module attributes to the instance.
        for attr in ("__name__", "__package__", "__loader__", "__spec__", "__file__"):
            setattr(instance, attr, getattr(module, attr, None))

        # Replace the module object in sys.modules with the instance.
        sys.modules[module_name] = instance

        # (Optional) Return value is ignored.