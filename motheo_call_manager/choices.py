from edc_constants.constants import OTHER
from edc_call_manager.constants import NO_CONTACT

from .constants import CONTACTED

TEST_TYPES = (
    ('elisa', 'Elisa'),
    ('rapid_test', 'Rapid Test'),
    ('dna_pcr', 'DNA PCR'),
    ('rna_pcr', 'RNA PCR'),
    (OTHER, 'Other')
)

OFF_STUDY_REASON = (
    ('completion_of_followup',
     'Completion of follow-up, as specified in protocol (see Study-specific MOP for definition of Completion)'),
    ('death', 'Death'),
    ('refused_further_contact',
     'Participant refused further contact (explain in Comments below)'),
    ('moved_away', 'Participant moved out of Study area'),
    ('unable_to_contact',
     'Unable to contact participant despite repeated attempts (see protocol for definition of Lost to Follow-up)'),
    (OTHER, 'Other'),
)

CALL_OUTCOME = (
    (CONTACTED, 'Contact Made'),
    (NO_CONTACT, 'Contact Made'),
)
