
CONTEST_TYPE_CHOICES = (
    ('ioi', 'ioi'),
    ('icpc', 'icpc')
)

CHECKING_STATUS_CHOICES = (
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