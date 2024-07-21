from enum import Enum


class BaseChoicesEnum(Enum):
    """
    Base class for choices enums.
    """

    @classmethod
    def choices(cls):
        """
        Function to return tuple of choices in the enum.
        """
        return tuple((data_source.value, data_source.name) for data_source in cls)

    @classmethod
    def values(cls):
        """
        Function to return a list of values in the enum.
        """
        return [data_source.value for data_source in cls]

    @classmethod
    def names(cls):
        """
        Function to return a list of names in the enum.
        """
        return [data_source.name for data_source in cls]

    @classmethod
    def name_exists(cls, name):
        """
        Function to check if the name exists in the enum.
        """
        return name in cls.__members__

    @classmethod
    def get_value(cls, name):
        """
        Function to get the value of a name in the enum.
        """
        return cls.__members__.get(name).value
