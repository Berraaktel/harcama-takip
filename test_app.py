from app import Expense, ExpenseTracker, kdv_ekle


def test_add_expense():
    tracker = ExpenseTracker()
    tracker.add_expense(Expense("kalem", 100, "kirtasiye"))
    assert len(tracker.harcamalar) == 1


def test_total_normal_durum():
    tracker = ExpenseTracker()
    tracker.add_expense(Expense("kalem", 100, "kirtasiye"))
    tracker.add_expense(Expense("defter", 50, "kirtasiye"))
    assert tracker.total() == 150


def test_total_bos_liste():
    tracker = ExpenseTracker()
    assert tracker.total() == 0


def test_kdv_ekle_gida():
    assert kdv_ekle(100, "gıda") == 101.0


def test_kdv_ekle_bilinmeyen_kategori():
    assert kdv_ekle(100, "kozmetik") == 120.0


def test_en_ucuz():
    tracker = ExpenseTracker()
    tracker.add_expense(Expense("kalem", 100, "kirtasiye"))
    tracker.add_expense(Expense("defter", 50, "kirtasiye"))
    tracker.add_expense(Expense("silgi", 20, "kirtasiye"))
    assert tracker.en_ucuz().isim == "silgi"