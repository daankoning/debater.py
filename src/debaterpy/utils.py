"""Various utilities to aid in the manipulation and analysis of the objects in ``debaterpy.structures``."""
from .structures import *
from typing import Generator, Callable
import io
import csv


def get_all_rounds(record: Record, function: Callable[[Tournament, Round], bool] = lambda x, y: True)\
		-> Generator[Round, None, None]:
	"""Gets all the rounds ``record`` for which ``function`` returns ``True``.

	This allows easier access to all the data such as for analysis of speaks or winrates. The ``function`` argument
	behaves similarly to Python's built-in ``filter``, it only allows entries for which ``function(x, y)`` is ``True``. For
	example, the following code will get all rounds in BP (which might be useful for splitting up analyses by format):

		>>> get_all_rounds(record, lambda x, y: x.format == "BP")
		<generator object get_all_rounds at 0x102861e40>

	Args:
		record: An instance of ``structures.Record`` from which the rounds will be extracted.
		function:  A callable returning a boolean which needs to be true for a record to be included. Receives instances
			of ``structures.Tournament`` and ``structures.Round``as arguments. Will default to including all rounds."""
	for tournament in record.tournaments:
		for round in tournament.rounds:
			if function(tournament, round):
				yield round


def merge_records(*args: Record) -> Record:
	"""Merges all the records passed, tournament-wise.

	Combines multiple records by their tournaments, creating one new ``Record`` object containing all the tournaments in
	the original records. Duplicate tournaments are identified by ``Tournament.tournament_name``, meaning the same name
	will never show up twice in the record.

	If a tournament is in multiple records only the version of the tournament in the record that is passed first will
	be preserved (so if both the first and the second argument define a tournament called "WUDC 2022" only the one in
	the first argument will be used). Note that this could lead to the more complete record being discarded.
	"""
	if not args:
		raise TypeError("merge_records() needs at least one argument but 0 were provided.")

	working_record = args[0]
	attended_tournament_names = [tournament.tournament_name for tournament in working_record.tournaments]
	for record in args:
		for tournament in record.tournaments:
			if tournament.tournament_name not in attended_tournament_names:
				working_record.tournaments.append(tournament)
				attended_tournament_names.append(tournament.tournament_name)

	return working_record


def generate_csv(record: Record, target: io.TextIOWrapper):
	"""Writes a CSV representation of ``record`` to ``target``."""
	writer = csv.writer(target, delimiter=",")
	writer.writerow(["tournament_name", "format", "broke", "break_categories", "name", "outround",
					 "outround_category", "prepped", "date", "date_string", "topics", "motion", "infoslide", "side", "half",
					 "teammates", "speech", "result", "speak", "advanced"])
	for tournament in record.tournaments:
		for round in tournament.rounds:
			for speech in round.speeches:
				writer.writerow(map(str, [
					tournament.tournament_name,
					tournament.format,
					tournament.broke,
					tournament.break_categories,
					round.name,
					round.outround,
					round.outround_category,
					round.prepped,
					str(round.date.timestamp()),
					round.date.strftime("%d-%m-%Y"),
					round.topics,
					round.motion,
					round.infoslide,
					round.side,
					round.half,
					round.teammates,
					speech.speech,
					round.result,
					speech.speak,
					round.advanced
				]))
