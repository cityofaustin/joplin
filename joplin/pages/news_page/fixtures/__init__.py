from .test_cases.written_by_CPIO_written_for_APH import written_by_CPIO_written_for_APH
from .test_cases.written_by_APH import written_by_APH


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    written_by_APH()
    written_by_CPIO_written_for_APH()
