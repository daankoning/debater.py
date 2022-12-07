"""A collection of simple classes that store information. This is mostly a pythonic, class-based wrapper around
DebaterJSON."""
from __future__ import annotations
import json
from typing import Optional
from datetime import datetime, date
from dataclasses import dataclass


class Item:
	"""A single item that is being stored, mostly used so that some default behaviour doesn't need to be repeated as
	much."""
	def __iter__(self):  # just using this as a workaround to make json serialization easier
		def is_valid(key):
			return not callable(self.__getattribute__(key)) \
				   and self.__getattribute__(key) is not None \
				   and key[:2] != "__"

		for key in filter(is_valid, dir(self)):
			value = self.__getattribute__(key)
			if isinstance(value, list) and len(value) > 0 and isinstance(value[0], Item):
				value = [dict(sub_value) for sub_value in value]
			elif isinstance(value, date):
				value = value.isoformat()

			yield key, value

	def to_json(self) -> str:
		"""Converts the object to a DebaterJSON string."""
		return json.dumps(dict(self))

	@classmethod
	def from_json(cls, data: str) -> Item:
		"""Instantiates a new object based on the data contained in the json string ``data``."""
		return cls.from_dict(json.loads(data))

	@classmethod
	def from_dict(self, data: dict) -> Item:
		"""instantiate a new object based on the dictionary ``data``. """
		raise NotImplementedError


@dataclass(unsafe_hash=True)
class Record(Item):
	"""The base class for one entire account of tournaments."""
	tournaments: list[Tournament]
	"""The tournaments to include in this account"""
	speaker_name: Optional[str] = None
	"""The name of the speaker in this account."""

	@classmethod
	def from_dict(cls, data: dict) -> Record:
		return cls(
			tournaments=[Tournament.from_dict(tournament) for tournament in data["tournaments"]],
			speaker_name=data.get("speaker_name")
		)


@dataclass(unsafe_hash=True)
class Tournament(Item):
	"""A single tournament's data. This is the primary object you will interact with the majority of the time."""
	tournament_name: str
	"""The name of the tournament."""
	format: Optional[str] = None
	"""The debating format used at this tournament (e.g. BP)."""
	broke: Optional[bool] = None
	"""Whether the debater broke at this tournament."""
	break_categories: Optional[list[str]] = None
	"""The category or categories the speaker broke in."""
	rounds: Optional[list[Round]] = None
	"""All the rounds the debater participated in in this tournament."""

	@classmethod
	def from_dict(cls, data: dict) -> Tournament:
		return cls(
			tournament_name=data["tournament_name"],
			format=data.get("format"),
			broke=data.get("broke"),
			break_categories=data.get("break_categories"),
			rounds=[Round.from_dict(round) for round in data.get("rounds", [])]
		)


@dataclass(unsafe_hash=True)
class Round(Item):
	"""A single round that is associated with a tournament."""
	name: Optional[str] = None
	"""The name of the round (e.g. 'round 1' or 'grand finals')."""
	outround: Optional[bool] = None
	"""If this round was an outround."""
	outround_category: Optional[str] = None
	"""What speaker category this outround belongs to (e.g. open or ESL). Should only be used if the round is an 
	outround."""
	prepped: Optional[bool] = None
	"""Whether the round was a prepped round (if applicable)."""
	date: Optional[datetime] = None
	"""The date at which this round took place."""
	topics: Optional[list[str]] = None
	"""Keywords relating to the topic of the debate (e.g. 'Politics')."""
	motion: Optional[str] = None
	"""The motion of the round."""
	infoslide: Optional[str] = None
	"""The infoslide attached to the motion."""
	side: Optional[str] = None
	"""The side of the motion the debater was on."""
	half: Optional[str] = None
	"""The half of the debate the debater was on. Only applies to BP."""
	teammates: Optional[list[str]] = None
	"""The teammate or teammates the speaker was debating with this round."""
	speeches: Optional[list[Speech]] = None
	"""The speeches the speaker gave in this round."""
	result: Optional[int] = None
	"""How many points the debater's team got from this round. In two-team formats, a 1 or 0 simply mean a win or loss,
	 respectively. For more complex formats, such as BP, please refer to the format's manuals for how many points a 
	 certain result yields."""
	advanced: Optional[bool] = None
	"""If the speaker advanced to the next phase of the tournament (if this round is an outround)."""

	@classmethod
	def from_dict(cls, data: dict) -> Round:
		if "speech" in data.keys() or "speak" in data.keys():  # neccesary due to these attributes' deprecation
			speeches = [Speech(data.get("speech"), data.get("speak"))]
		else:
			speeches = [Speech.from_dict(speech) for speech in data.get("speeches", [])]

		return cls(
			name=data.get("name"),
			outround=data.get("outround"),
			outround_category=data.get("outround_category"),
			prepped=data.get("prepped"),
			date=datetime.fromisoformat(data.get("date", "1970-01-01")),
			topics=data.get("topics"),
			motion=data.get("motion"),
			infoslide=data.get("infoslide"),
			side=data.get("side"),
			half=data.get("half"),
			teammates=data.get("teammates"),
			speeches=speeches,
			result=data.get("result"),
			advanced=data.get("advanced")
		)


@dataclass(unsafe_hash=True)
class Speech(Item):
	"""A speech in a round."""
	speech: Optional[int] = None
	"""The speech of this speech. Only counts speeches on the debater's side (e.g. in BP an opposition whip would be
	 speech 4, not 8)."""
	speak: Optional[float] = None
	"""The speak this speech received."""

	@classmethod
	def from_dict(cls, data: dict) -> Speech:
		return cls(
			speech=data.get("speech"),
			speak=data.get("speak")
		)
