class King():
	def __init__(self, name, preference=None, choice_number=0, is_accepted=False, best_queen=None):
		self.name = name
		self.preference = preference
		self.choice_number = choice_number
		self.is_accepted = is_accepted
		self.best_queen = best_queen

	def __str__(self):
		return f"King of {self.name}"

	def __repr__(self):
		return f"King of {self.name}"

	def propose_to_queen(self):
		queen = self.preference[self.choice_number]
		return queen


class Queen():
	def __init__(self, name, preference=None, candidates=None, best_candidate=None, chosen=False):
		self.name = name
		self.preference = preference
		if candidates is None:
			self.candidates = []
		else:
			self.candidates = candidates
		self.best_candidate = best_candidate
		self.chosen = chosen

	def __str__(self):
		return f"Queen of {self.name}"

	def __repr__(self):
		return f"Queen of {self.name}"

	def choose_best_candidate(self):
		ranked_candidates = []
		for candidate in self.candidates:
			rank = self.preference.index(candidate)
			ranked_candidate = (rank, candidate)
			ranked_candidates.append(ranked_candidate)
		ranked_best_candidate = min(ranked_candidates, key = lambda x: x[0])
		best_candidate = ranked_best_candidate[1]

		## Every other king is rejected and have to propose again Sadly
		ranked_candidates.remove(ranked_best_candidate)
		rejected_candidates = [candidate for (rank, candidate) in ranked_candidates]

		print(self, " chooses ", best_candidate)
		return best_candidate, rejected_candidates

	def add_candidate(self, king):
		self.candidates.append(king)



#### for just 2 kings and 2 queens
# faces = ["heart", "diamond" ] #, "spades", "clubs"]

# king_preferences = [
#     (1, 2),
#     (2, 1)
# ]

# queen_preferences = [
#     (2, 1),
#     (2, 1)
# ]

##### for 3 kings and 3 queens
# faces = ["heart", "diamond", "clubs"]
#
# king_preferences = [
#     (3, 1, 2),
#     (1, 3, 3),
#     (1, 3, 2)
# ]
#
# queen_preferences = [
#     (1, 2, 3),
#     (1, 3, 2),
#     (2, 3, 1)
# ]




def have_all_queens_chosen_their_kings(queens_list):
	for queen in queens_list:
		if not queen.chosen:
			return False
	return True







def begin_King_and_Queen_Match(faces, king_preferences, queen_preferences):
	kings_list = []
	queens_list = []

	for face in faces:
		king = King(name=face)
		queen = Queen(name=face)
		kings_list.append(king)
		queens_list.append(queen)

	for i, preference in enumerate(king_preferences):
		kings_list[i].preference = [queens_list[x] for x in preference]

	for i, preference in enumerate(queen_preferences):
		queens_list[i].preference = [kings_list[y] for y in preference]


	print("Main Algorithm Here")
	NUM = 1
	while have_all_queens_chosen_their_kings(queens_list) == False:
		print(".............................................")
		print("Match Making Step", NUM)
		print(".............................................")
		NUM = NUM + 1
		# STep 1: all kings propose to their fancy queen
		# print("_______________________")
		# print("Begin Proposing Kings")
		# print("_______________________")
		for king in kings_list:
			if not king.is_accepted:                                        ### tHE kINGS's who didn't get anyone choose again next time.
				queen = king.propose_to_queen()
				queen.add_candidate(king)
				# print(king, " proposes to ", queen)

		#### The queens will choose like this
		#### From all the ones who've proposed to the queen, she'll chose the number one among them.
		#### even though he might not be mr. perfect. he might be mr. goood enough
		# step 2: all queens accept/keep in list or reject the kings
		# print("_______________________")
		# print("Begin Choosing Queens")
		# print("_______________________")
		for queen in queens_list:
			# print(queen)
			# print("candidates for the queen: ", queen.candidates)
			# if len(queen.candidates) == 0:
			#     # print("Sorry no kings proposed to you ", queen)
			if len(queen.candidates) == 1:
				best_candidate = queen.candidates[0]
				best_candidate.is_accepted = True
				best_candidate.best_queen = queen
				# print("Best candidate ", best_candidate)
				queen.best_candidate = best_candidate
				queen.chosen = True
			elif len(queen.candidates) >= 2:
				best, rejected = queen.choose_best_candidate()

				best.is_accepted = True
				best.best_queen = queen
				# print("Best candidate ", best)
				# print("Rejected ",rejected)
				queen.best_candidate = best
				queen.chosen = True
				queen.candidates = [best]
				for r in rejected:
					r.is_accepted = False
					r.best_queen = None
					r.choice_number = r.choice_number + 1

	matches = [(king, king.best_queen) for king in kings_list]
	matches = [(k.name, q.name) for (k, q) in matches]
	return matches

####################################################################################

# king_and_queen_matches = begin_King_and_Queen_Match	(faces=faces, king_preferences=king_preferences,
# 									queen_preferences=queen_preferences)
#
# print("Final Matches")
# print(">>>>>--------------------------------------------------------------------->>>>>>>>>")
# print("Match Maker Does it again")
# print(">>>>>--------------------------------------------------------------------->>>>>>>>>")
# for (king, queen) in king_and_queen_matches:
#     print(king, " matched to ", queen)
