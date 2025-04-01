import csv
from typing import TypeVar, Generic, List, Union, Generator, Callable, Annotated, Any

from pydantic import ValidationError, Field, StringConstraints
from pydantic.v1.fields import ModelField

from ul_api_utils.const import CRON_EXPRESSION_VALIDATION_REGEX, MIN_UTC_OFFSET_SECONDS, MAX_UTC_OFFSET_SECONDS

NotEmptyListAnnotation = Annotated[list[Any], Field(min_length=1)]
CronScheduleAnnotation = Annotated[str, StringConstraints(pattern=CRON_EXPRESSION_VALIDATION_REGEX)]
WhiteSpaceStrippedStrAnnotation = Annotated[str, StringConstraints(strip_whitespace=True)]
UTCOffsetSecondsAnnotation = Annotated[int, Field(ge=MIN_UTC_OFFSET_SECONDS, le=MAX_UTC_OFFSET_SECONDS)]
PgTypePasswordStrAnnotation = Annotated[str, StringConstraints(min_length=6, max_length=72)]
PgTypeShortStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=255)]
PgTypeLongStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=1000)]
PgTypeInt16Annotation = Annotated[int, Field(ge=-32768, le=32768)]
PgTypePositiveInt16Annotation = Annotated[int, Field(ge=0, le=32768)]
PgTypeInt32Annotation = Annotated[int, Field(ge=-2147483648, le=2147483648)]
PgTypePositiveInt32Annotation = Annotated[int, Field(ge=0, le=2147483648)]
PgTypeInt64Annotation = Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775808)]
PgTypePositiveInt64Annotation = Annotated[int, Field(ge=0, le=9223372036854775808)]


QueryParamsSeparatedListValueType = TypeVar('QueryParamsSeparatedListValueType')


class QueryParamsSeparatedList(Generic[QueryParamsSeparatedListValueType]):
    """
    Supports cases when query parameters are being sent as a string, but you have to assume
    that it is a list.

    F.E. Query string is ?foo=1,2

    Note:
        Sent as a string, but interpreted as List.
    """

    def __init__(self, contains_type: QueryParamsSeparatedListValueType) -> None:
        self.contains_type = contains_type

    def __repr__(self) -> str:
        return f'QueryParamsSeparatedList({super().__repr__()})'

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Union[List[str], str], ModelField], Union[List[QueryParamsSeparatedListValueType], List[str]]], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, query_param: Union[List[str], str], field: ModelField) -> Union[List[QueryParamsSeparatedListValueType], List[str]]:
        if not isinstance(query_param, List):
            query_param = [query_param]
        reader = csv.reader(query_param, skipinitialspace=True)
        splitted = next(reader)
        if not field.sub_fields:
            return splitted
        list_item = field.sub_fields[0]  # retrieving info about data type of the list
        errors = []
        for value in splitted:
            validated_list_item, error = list_item.validate(value, {}, loc="separated query param")
            if error:
                errors.append(error)
        if errors:
            raise ValidationError(errors, cls)
        # Validation passed without errors, modify string to a list and cast the right type for every element
        return [list_item.type_(value) for value in splitted]
