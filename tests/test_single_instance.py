from dcmd.integrations.single_instance import SingleInstanceGuard


class FakeMutex:
    def __init__(self, acquired: bool) -> None:
        self.acquired = acquired
        self.released = False

    def acquire(self) -> bool:
        return self.acquired

    def release(self) -> None:
        self.released = True


def test_single_instance_guard_returns_mutex_result() -> None:
    mutex = FakeMutex(acquired=True)
    guard = SingleInstanceGuard(mutex)
    assert guard.acquire() is True


def test_single_instance_guard_releases_mutex() -> None:
    mutex = FakeMutex(acquired=True)
    guard = SingleInstanceGuard(mutex)
    guard.release()
    assert mutex.released is True
