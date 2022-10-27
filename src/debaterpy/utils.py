"""Various utilities to aid in the manipulation and analysis of the objects in `debaterpy.structures`."""
from .structures import *
from typing import Generator, Callable
import io
import csv


def get_all_rounds(record: Record, function: Callable[[Tournament, Round], bool] = lambda x, y: True)\
		-> Generator[Round, None, None]:
	"""Gets all the rounds `record` for which `function` returns `True`.

	This allows easier access to all the data such as for analysis of speaks or winrates. The `function` argument
	behaves similarly to Python's built-in `filter`, it only allows entries for which `function(x, y)` is `True`. For
	example, the following code will get all rounds in BP (which might be useful for splitting up analyses by format):

		>>> get_all_rounds(record, lambda x, y: x.format == "BP")
		<generator object get_all_rounds at 0x102861e40>

	Args:
		record: An instance of `structures.Record` from which the rounds will be extracted.
		function:  A callable returning a boolean which needs to be true for a record to be included. Receives instances
			of `structures.Tournament` and `structures.Round`as arguments. Will default to including all rounds."""
	for tournament in record.tournaments:
		for round in tournament.rounds:
			if function(tournament, round):
				yield round


def generate_csv(record: Record, target: io.TextIOWrapper):
	"""Writes a CSV representation of `record` to `target`."""
	writer = csv.writer(target, delimiter=",")
	writer.writerow(["tournament_name", "format", "broke", "break_categories", "round_name", "outround",
					 "outround_category", "prepped", "date", "topics", "motion", "infoslide", "side", "half",
					 "teammates", "speech", "result", "speak"])
	for tournament in record.tournaments:
		for round in tournament.rounds:
			for speech in round.speeches:
				writer.writerow(map(str, [
					tournament.tournament_name,
					tournament.format,
					tournament.broke,
					tournament.break_categories,
					round.round_name,
					round.outround,
					round.outround_category,
					round.prepped,
					round.date.isoformat(),
					round.topics,
					round.motion,
					round.infoslide,
					round.side,
					round.half,
					round.teammates,
					speech.number,
					round.result,
					speech.speak
				]))
