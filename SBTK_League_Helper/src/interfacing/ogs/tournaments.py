from .abstract import OGSElement, OGSBetaElement
from ..tournaments import Tournament


class OGSTournament(OGSElement, Tournament):
    ...
    # TO BE IMPLEMENTED PRETTY SOON


class OGSBetaTournament(OGSBetaElement, Tournament):
    ...
    # TO BE IMPLEMENTED PRETTY SOON

#Both classes could be essentially the same
# if that is the case, we could consider a different approach
# (some sort of macro)
