CONTEST_TYPE_CHOICES = (
    ('ioi', 'ioi'),
    ('icpc', 'icpc')
)

CHECKING_STATUS_CHOICES = (
    ('NOT_STARTED', 'Pending start'),
    ('CHECKING', 'Started checking'),
    ('NOT_SEEN', 'Checked, but not seen'),
    ('CHEATED', 'This attempts was cheated'),
    ('NOT_CHEATED', 'This attempts was not cheated')
)

OUTCOME_CHOICES = (
    ('undefined', "undefined"),
    ('fl', 'fail'),
    ('unknown', 'unknown'),
    ('accepted', 'accepted'),
    ('partially-correct', 'partially-correct'),
    ('relative-scoring', 'relative-scoring'),
    ('compilation-error', 'compilation-error'),
    ('wrong-answer', 'wrong-answer'),
    ('presentation-error', 'presentation-error'),
    ('runtime-error', 'runtime-error'),
    ('time-limit-exceeded', 'time-limit-exceeded'),
    ('memory-limit-exceeded', 'memory-limit-exceeded'),
    ('output-limit-exceeded', 'output-limit-exceeded'),
    ('idleness-limit-exceeded', 'idleness-limit-exceeded'),
    ('security-violation', 'security-violation'),
    ('cancelled', 'cancelled')
)

AUTH_TYPE_CHOICES = (
    ('p', 'pcms auth'),
    ('b', 'builtin auth')
)

CODEMIRROR_LANG_PARAMS = {
    'py': 'text/x-python',
    'cpp': 'text/x-c++src',
    'pas': 'text/x-pascal',
    'java': 'text/x-java'
}

TYPES_OF_PAGES = {
    'default': {'reverse': 'checker:pending_manual_check', 'statuses': ['NOT_SEEN']},
    'checking_in_progress': {'reverse': 'checker:checking_in_progress', 'statuses': ['NOT_STARTED', 'CHECKING']},
    'pending_manual_check': {'reverse': 'checker:pending_manual_check', 'statuses': ['NOT_SEEN']},
    'all_cheaters': {'reverse': 'checker:all_cheaters', 'statuses': ['CHEATED']}
}
