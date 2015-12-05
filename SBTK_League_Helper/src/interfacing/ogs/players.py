from .abstract import OGSElement, OGSBetaElement
from ..players import Player


class OGSPlayer(OGSElement, Player):
    ...
    # TO BE IMPLEMENTED PRETTY SOON


class OGSBetaPlayer(OGSBetaElement, Player):
    ...
    # TO BE IMPLEMENTED PRETTY SOON

#Both classes could be essentially the same
# if that is the case, we could consider a different approach
# (some sort of macro)
