from .test_cases.written_by_CPIO_written_for_APH import written_by_CPIO_written_for_APH
from .test_cases.written_by_APH import written_by_APH
from .test_cases.written_by_APH_written_for_APH import written_by_APH_written_for_APH
from .test_cases.fifty_written_by_APH import fifty_written_by_APH

# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    # written_by_APH()
    # written_by_CPIO_written_for_APH()
    [x for x in fifty_written_by_APH()]