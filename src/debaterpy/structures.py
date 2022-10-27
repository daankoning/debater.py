"""A collection of simple classes that store information. This is mostly a pythonic, class-based wrapper around DebaterJSON."""
from __future__ import annotations
import json
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Record:
	"""The base class for one entire account of tournaments."""
	tournaments: list[Tournament]
	"""The tournaments to include in this account"""
	speaker_name: Optional[str] = None
	"""The name of the speaker in this account."""

	@classmethod
	def from_json(cls, data: str) -> Record:
		return cls.from_dict(json.loads(data))

	@classmethod
	def from_dict(cls, data: dict) -> Record:
		return cls(
			tournaments=[Tournament.from_dict(tournament) for tournament in data["tournaments"]],
			speaker_name=data.get("speaker_name")
		)


@dataclass(unsafe_hash=True)
class Tournament:
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
	def from_json(cls, data: str) -> Tournament:
		return cls.from_dict(json.loads(data))

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
class Round:
	"""A single round that is associated with a tournament."""
	round_name: Optional[str] = None
	"""The name of the round (e.g. 'round 1' or 'grand finals')."""
	outround: Optional[bool] = None
	"""If this round was an outround."""
	outround_category: Optional[str] = None
	"""What speaker category this outround belongs to (e.g. open or ESL). Should only be used if the round is an outround."""
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
	"""How many points the debater's team got from this round. In two-team formats, a 1 or 0 simply mean a win or loss, respectively. For more complex formats, such as BP, please refer to the format's manuals for how many points a certain result yields."""

	@classmethod
	def from_json(cls, data: str) -> Round:
		return cls.from_dict(json.loads(data))

	@classmethod
	def from_dict(cls, data: dict) -> Round:
		if "speech" in data.keys() or "speak" in data.keys():  # neccesary due to these attributes' deprecation
			speeches = [Speech(data.get("speech"), data.get("speak"))]
		else:
			speeches = [Speech.from_dict(speech) for speech in data.get("speeches", [])]

		return cls(
			round_name=data.get("name"),
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
			result=data.get("result")
		)


@dataclass(unsafe_hash=True)
class Speech:
	"""A speech in a round."""
	number: Optional[int] = None
	"""The number of this speech. Only counts speeches on the debater's side (e.g. in BP an opposition whip would be speech 4, not 8)."""
	speak: Optional[float] = None
	"""The speak this speech received."""

	@classmethod
	def from_json(cls, data: str) -> Speech:
		return cls.from_dict(json.loads(data))

	@classmethod
	def from_dict(cls, data: dict) -> Speech:
		return cls(
			number=data.get("speech"),
			speak=data.get("speak")
		)
