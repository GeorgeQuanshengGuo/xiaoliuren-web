from __future__ import annotations


class DivinationInputError(ValueError):
    """Base error for user-facing divination input problems."""


class InvalidLunarDateError(DivinationInputError):
    """Raised when lunar month or day is outside the supported range."""


class InvalidTimezoneError(DivinationInputError):
    """Raised when a timezone name cannot be resolved by ZoneInfo."""


class CalendarConversionError(DivinationInputError):
    """Raised when solar-to-lunar conversion cannot be completed."""
